"""Idempotent importer for weekly external market-data exports (Doc 329/C17-A).

Accepts a folder of messy weekly exports (GSC ``.csv.zip.zip``, AI-Overview
zips, GA4 "Performance on Search" dumps, Ubersuggest KBT/backlink/top-page
CSVs, call-tracking CSVs, a leads summary txt, and Ubersuggest PDF reports
exported as markdown), classifies each file by name, parses it in-memory
(nested zips included, no shell unzip needed), and bulk-inserts rows under an
``external_exports`` registry row keyed by file sha256 so a re-run is a no-op.

Every file is imported in its own transaction: one bad file never blocks the
rest of the folder.
"""
import csv
import datetime as dt
import hashlib
import io
import logging
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import insert

from app.models.external import (
    ExternalExport,
    SearchConsoleDim,
    SearchConsoleDaily,
    AIOverviewImpressions,
    KeywordEstimate,
    Backlink,
    TopPage,
    CallTracking,
    LeadSummary,
    GA4Event,
    DomainReport,
    DomainMetric,
)

logger = logging.getLogger(__name__)

# Every detail table hanging off external_exports (FK export_id, ON DELETE CASCADE).
DETAIL_MODELS = (
    SearchConsoleDim,
    SearchConsoleDaily,
    AIOverviewImpressions,
    KeywordEstimate,
    Backlink,
    TopPage,
    CallTracking,
    LeadSummary,
    GA4Event,
    DomainReport,
    DomainMetric,
)

# Canonical brands for the three money sites; everything else is a competitor
# (domain preserved, brand left null).
BRAND_DOMAINS = {
    "kleangutter.com": "kleangutter",
    "mastershield.com": "mastershield",
    "micromeshgutterguards.com": "mmgg",
}

DOMAIN_ALIASES = {
    "kleangutter": "kleangutter.com",
    "klean": "kleangutter.com",
    "klean gutter": "kleangutter.com",
    "mastershield": "mastershield.com",
    "micromeshgutterguards": "micromeshgutterguards.com",
    "micromeshgg": "micromeshgutterguards.com",
    "micromesh": "micromeshgutterguards.com",
}

# inner GSC zip csv -> (kind, dim_type). "daily" goes to search_console_daily,
# everything else to search_console_dims.
GSC_PROFILE = {
    "chart.csv": ("daily", None),
    "queries.csv": ("dims", "query"),
    "pages.csv": ("dims", "page"),
    "countries.csv": ("dims", "country"),
    "devices.csv": ("dims", "device"),
    "search appearance.csv": ("dims", "appearance"),
}

MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"])}


# ---------------------------------------------------------------- coercers

def parse_int(value) -> int | None:
    if value is None:
        return None
    v = str(value).strip().replace(",", "")
    if not v or v in {"-", "n/a", "N/A"}:
        return None
    try:
        return int(round(float(v)))
    except ValueError:
        return None


def parse_float(value) -> float | None:
    if value is None:
        return None
    v = str(value).strip().replace(",", "").rstrip("%")
    if not v or v.lower() in {"-", "n/a"}:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def parse_duration_seconds(value) -> int | None:
    """'00:03:40' (H:M:S), '03:40' (M:S) or bare seconds -> seconds."""
    if value is None:
        return None
    v = str(value).strip()
    if not v or v == "-":
        return None
    parts = v.split(":")
    if len(parts) == 1:
        return parse_int(parts[0])
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return None
    total = 0
    for p in nums:
        total = total * 60 + p
    return total


def parse_iso_date(value) -> dt.date | None:
    if not value:
        return None
    v = str(value).strip()
    try:
        return dt.date.fromisoformat(v)
    except ValueError:
        return None


def parse_mdy(value) -> dt.date | None:
    m = re.search(r"([A-Za-z]{3,9}) (\d{1,2}), (\d{4})", value or "")
    if not m:
        return None
    mon = MONTHS.get(m.group(1).lower()[:3])
    if not mon:
        return None
    try:
        return dt.date(int(m.group(3)), mon, int(m.group(2)))
    except ValueError:
        return None


def parse_compact_date(value) -> dt.date | None:
    v = (value or "").strip()
    if not re.fullmatch(r"\d{8}", v):
        return None
    try:
        return dt.datetime.strptime(v, "%Y%m%d").date()
    except ValueError:
        return None


def parse_date(value) -> dt.date | None:
    return parse_iso_date(value) or parse_mdy(value) or parse_compact_date(value)


def normalize_domain(value: str) -> str:
    d = (value or "").strip().lower().replace(" ", "")
    d = re.sub(r"^https?://", "", d)
    d = re.sub(r"^www\.", "", d)
    d = re.sub(r"[()\[\]]", "", d)
    for k, v in DOMAIN_ALIASES.items():
        if d == k:
            return v
    return d


def brand_for(domain: str) -> str | None:
    return BRAND_DOMAINS.get(normalize_domain(domain))


def file_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def extract_domain_token(name: str) -> str | None:
    """Pull a domain-shaped token (.com or -com) out of a filename fragment."""
    m = re.search(r"([a-z0-9]+(?:-[a-z0-9]+)*\.com|[a-z0-9]+(?:-[a-z0-9]+)*-com)", name.lower())
    if not m:
        return None
    return m.group(1).replace("-com", ".com")


def _first_real_line(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.lstrip("\ufeff").strip()
            if line and not line.startswith("#"):
                return line
    return ""


# ---------------------------------------------------------------- classifier

def classify(path: Path) -> tuple[str, str | None, str | None]:
    """(source_type, domain, brand). source_type may carry report_type via '_'."""
    name = path.name
    low = name.lower()

    if low.endswith(".zip"):
        if "gsc_export" in low:
            token = re.split(r"_gsc_export", low)[0].strip(" _")
            domain = DOMAIN_ALIASES.get(token, token) or None
            domain = normalize_domain(domain)
            return "search_console", domain, brand_for(domain)
        if "-ai-features" in low:
            prefix = re.split(r"-ai-features", low)[0]
            domain = normalize_domain(prefix)
            return "ai_overview", domain or None, brand_for(domain)
        raise ValueError(f"Unrecognized archive: {name}")

    if "backlinks_overview" in low:
        token = re.sub(r"_(backlinks|traffic)_overview.*$", "", low)
        domain = extract_domain_token(token) or normalize_domain(token)
        return "domain_report:backlinks", domain, brand_for(domain)
    if "traffic_overview" in low or low.startswith("traffic-overview"):
        token = re.sub(r"_(backlinks|traffic)_overview.*$", "", low)
        token = re.sub(r"^traffic-overview[_-]?", "", token)
        token = re.split(r"-\d{4}-\d{2}-\d{2}$", token)[0]
        domain = extract_domain_token(token) or normalize_domain(token)
        return "domain_report:traffic", domain, brand_for(domain)
    if "calls export from" in low:
        prefix = re.split(r"\s*calls export from", low)[0].strip().rstrip("-").strip()
        if prefix.lower().startswith("micromeshgg"):
            prefix = "micromeshgg"
        domain = DOMAIN_ALIASES.get(prefix) or normalize_domain(prefix)
        return "call_tracking", domain or None, brand_for(domain)
    if low.startswith("leads_summary"):
        return "lead_summary", "all", None
    if "_kbt" in low:
        token = re.split(r"_kbt", low)[0]
        domain = extract_domain_token(token) or normalize_domain(token)
        if "url,title" in _first_real_line(path).lower():
            return "top_page", domain, brand_for(domain)
        return "keyword_estimate", domain, brand_for(domain)
    if re.search(r"_backlinks\.csv", low):
        token = re.split(r"_backlinks\.csv", low)[0]
        domain = extract_domain_token(token) or normalize_domain(token)
        return "backlink", domain, brand_for(domain)
    if "performance-on-search" in low:
        prefix = re.split(r"-performance-on-search", low)[0]
        if re.match(r"^kleangutter", prefix, re.I):
            prefix = "kleangutter"
        domain = DOMAIN_ALIASES.get(prefix) or normalize_domain(prefix)
        return "ga4_event", domain or None, brand_for(domain)

    if low.endswith(".csv"):
        header = _first_real_line(path).lower()
        token = re.split(r"\.csv", name, flags=re.IGNORECASE)[0]
        domain = extract_domain_token(token) or normalize_domain(token)
        has_keywords = "keywords,volume" in header
        is_top_page_name = bool(re.search(r"(^|[\s_])top pages?", low)) or \
            bool(re.search(r"ubersuggest[_\s]|\(selected\)", low))
        if "url,title" in header or (is_top_page_name and not has_keywords):
            return "top_page", domain, brand_for(domain)
        if has_keywords:
            return "keyword_estimate", domain, brand_for(domain)
        raise ValueError(f"Unrecognized CSV: {name}")

    if low.endswith(".md"):
        token = re.split(r"\.md", name, flags=re.IGNORECASE)[0]
        token = re.sub(r"_(backlinks|traffic)_overview.*$", "", token, flags=re.I)
        token = re.sub(r"^traffic-overview[_-]?", "", token)
        token = re.split(r"-\d{4}-\d{2}-\d{2}$", token)[0]
        domain = extract_domain_token(token) or normalize_domain(token)
        if "backlinks_overview" in low:
            return "domain_report:backlinks", domain, brand_for(domain)
        return "domain_report:traffic", domain, brand_for(domain)

    raise ValueError(f"Unrecognized file: {name}")


# ---------------------------------------------------------------- parsers

def _open_zip(data: bytes) -> zipfile.ZipFile | None:
    try:
        return zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        return None


def _read_zip(path: Path) -> dict[str, bytes]:
    with open(path, "rb") as fh:
        raw = fh.read()
    out: dict[str, bytes] = {}

    def walk(data: bytes, top: bool = False):
        zf = _open_zip(data)
        if zf is None:
            if top:
                out["_nonzip"] = data
            return
        with zf:
            for n in zf.namelist():
                if n.endswith("/"):
                    continue
                payload = zf.read(n)
                if _open_zip(payload) is None:
                    out.setdefault(n, payload)
                else:
                    walk(payload)

    walk(raw, top=True)
    return out


def _csv_iter(data: bytes) -> list[dict]:
    text = data.decode("utf-8", "replace").lstrip("\ufeff")
    return list(csv.DictReader(io.StringIO(text)))


def _period_from_filters(inner: dict[str, bytes]) -> tuple[datetime | None, datetime | None]:
    data = inner.get("Filters.csv")
    if not data:
        return None, None
    for row in _csv_iter(data):
        if (row.get("Filter") or "").strip().lower() == "date":
            m = re.match(r"([A-Za-z]{3,9} \d{1,2}, \d{4})\s*-\s*(.+)", (row.get("Value") or "").strip())
            if m:
                start, end = parse_mdy(m.group(1)), parse_mdy(m.group(2))
                return (datetime.combine(start, dt.time.min, tzinfo=timezone.utc) if start else None,
                        datetime.combine(end, dt.time.min, tzinfo=timezone.utc) if end else None)
    return None, None


def parse_search_console(path: Path) -> tuple[dict, list[dict], list[dict]]:
    inner = _read_zip(path)
    period_from, period_to = _period_from_filters(inner)
    dims, daily = [], []
    key_fields = {
        "query": "Top queries", "page": "Top pages", "country": "Country",
        "device": "Device", "appearance": "Search appearance",
    }
    for name, data in inner.items():
        role, dim_type = GSC_PROFILE.get(name.lower(), (None, None))
        if role is None:
            continue
        for row in _csv_iter(data):
            if role == "daily":
                day = parse_iso_date(row.get("Date"))
                if day is None:
                    continue
                daily.append({
                    "day": day,
                    "clicks": parse_int(row.get("Clicks")) or 0,
                    "impressions": parse_int(row.get("Impressions")) or 0,
                    "ctr": parse_float(row.get("CTR")),
                    "position": parse_float(row.get("Position")),
                })
            else:
                key = row.get(key_fields[dim_type])
                if not key:
                    continue
                dims.append({
                    "dim_type": dim_type,
                    "key": key.strip(),
                    "clicks": parse_int(row.get("Clicks")) or 0,
                    "impressions": parse_int(row.get("Impressions")) or 0,
                    "ctr": parse_float(row.get("CTR")),
                    "position": parse_float(row.get("Position")),
                })
    return {"period_from": period_from, "period_to": period_to}, dims, daily


def parse_ai_overview(path: Path) -> tuple[dict, list[dict]]:
    inner = _read_zip(path)
    period_from, period_to = _period_from_filters(inner)
    rows = []
    for name, data in inner.items():
        base = name.rsplit(".", 1)[0].lower()
        spec = {"chart": ("chart", None, "Date"),
                "pages": ("pages", "Top pages", None),
                "countries": ("countries", "Country", None),
                "devices": ("devices", "Device", None)}.get(base)
        if spec is None:
            continue
        dim_type, key_field, date_field = spec
        for row in _csv_iter(data):
            rec = {"dim_type": dim_type, "impressions": parse_int(row.get("Impressions")) or 0}
            if key_field and row.get(key_field):
                rec["key"] = row[key_field].strip()[:255]
            if date_field:
                rec["day"] = parse_iso_date(row.get(date_field))
            rows.append(rec)
    return {"period_from": period_from, "period_to": period_to}, rows


def parse_ga4(path: Path) -> tuple[dict, list[dict], str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    start = end = domain = None
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        if m := re.search(r"Start date: (\d{8})", line):
            start = parse_compact_date(m.group(1))
        if m := re.search(r"End date: (\d{8})", line):
            end = parse_compact_date(m.group(1))
        if m := re.search(r"Property:\s*(.+)", line):
            domain = normalize_domain(m.group(1).split(" - ")[0])
    body = "\n".join(l for l in text.splitlines() if not l.strip().startswith("#"))
    rows = []
    for r in csv.DictReader(io.StringIO(body)):
        event = (r.get("Event name") or "").strip()
        if not event:
            continue
        rows.append({
            "event_name": event,
            "event_count": parse_int(r.get("Event count")) or 0,
            "total_users": parse_int(r.get("Total users")) or 0,
            "events_per_user": parse_float(r.get("Event count per active user")),
            "total_revenue": parse_float(r.get("Total revenue")) or 0.0,
        })
    meta = {
        "period_from": datetime.combine(start, dt.time.min, tzinfo=timezone.utc) if start else None,
        "period_to": datetime.combine(end, dt.time.min, tzinfo=timezone.utc) if end else None,
        "exported_at": datetime.combine(end, dt.time.min, tzinfo=timezone.utc) if end else None,
    }
    return meta, rows, domain


def parse_calls(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = []
    for raw in csv.DictReader(io.StringIO(text)):
        row = {k.strip(): (v or "").strip() for k, v in raw.items()}
        if not any(row.get(k) for k in ("Name", "Customer #", "Duration", "Date")):
            continue
        rows.append({
            "name": row.get("Name"),
            "customer_number": row.get("Customer #"),
            "source": row.get("Tracking Source"),
            "status": row.get("Call Status"),
            "search_query": row.get("Search Query") or row.get("Search Query ") or None,
            "referral": row.get("Referral"),
            "page": row.get("Page") or row.get("Page URL") or None,
            "last_url": row.get("Last URL"),
            "likelihood": parse_float(row.get("Likelihood")),
            "message_body": row.get("Message Body") or None,
            "duration_seconds": parse_duration_seconds(row.get("Duration")),
            "ring_time_seconds": parse_duration_seconds(row.get("Ring Time")),
            "call_date": parse_iso_date(row.get("Date")),
        })
    return rows


def parse_leads(path: Path) -> tuple[dict, list[dict]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    period_from = period_to = None
    m = re.search(r"Week ending:\s*(\d{2}-\d{2}-\d{4})\s*\(\s*(.*?)\s*\)", text)
    if m:
        try:
            to_date = dt.datetime.strptime(m.group(1), "%m-%d-%Y").date()
            period_to = datetime.combine(to_date, dt.time.min, tzinfo=timezone.utc)
            parts = re.fullmatch(r"(\d{2})/(\d{2})\s*-\s*(\d{2})/(\d{2})", m.group(2))
            if parts:
                start_year = to_date.year
                if int(parts.group(2)) > int(parts.group(4)):
                    start_year -= 1
                period_from = datetime.combine(
                    dt.date(start_year, int(parts.group(1)), int(parts.group(2))),
                    dt.time.min, tzinfo=timezone.utc)
        except ValueError:
            pass

    brand_domains = {
        "mastershield": "mastershield.com",
        "klean": "kleangutter.com",
        "micromesh": "micromeshgutterguards.com",
    }
    rows = []
    current_domain = None
    for line in text.splitlines():
        line = line.strip()
        bm = re.match(r"^([A-Za-z ]+[^:]*?)\s*:\s*(\d+)(?:\s+leads?)?$", line)
        if bm:
            label = bm.group(1).lower()
            current_domain = next((d for k, d in brand_domains.items() if label.startswith(k)), None)
            if current_domain is None:
                current_domain = next((d for k, d in brand_domains.items() if k.startswith(label)), None)
            continue
        if not current_domain:
            continue
        fm = re.match(r"-\s*Form fills?:\s*(\d+)", line)
        vm = re.match(r"-\s*VAPI calls?:\s*(\d+)", line)
        if not (fm or vm):
            line = re.sub(r"^-\s*", "", line)
            fm = re.match(r"Form fills?:\s*(\d+)", line)
            vm = re.match(r"VAPI calls?:\s*(\d+)", line)
        if not (fm or vm):
            continue
        rec = next((r for r in rows if r["domain"] == current_domain), None)
        if rec is None:
            rec = {"domain": current_domain, "form_fills": 0, "vapi_calls": 0}
            rows.append(rec)
        if fm:
            rec["form_fills"] = int(fm.group(1))
        if vm:
            rec["vapi_calls"] = int(vm.group(1))
    return {"period_from": period_from, "period_to": period_to}, rows


def parse_kbt(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = []
    for r in csv.DictReader(io.StringIO(text.lstrip("\ufeff"))):
        kw = (r.get("Keywords") or "").strip()
        if not kw:
            continue
        rows.append({
            "keyword": kw,
            "volume": parse_int(r.get("Volume")),
            "position": parse_float(r.get("Position")),
            "est_visits": parse_int(r.get("Est. Visits")),
            "difficulty": parse_float(r.get("SEO Difficulty")),
            "cpc": parse_float(r.get("CPC")),
            "ranking_url": r.get("Ranking URL") or None,
        })
    return rows


def parse_backlinks(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = []
    for r in csv.DictReader(io.StringIO(text.lstrip("\ufeff"))):
        if not r.get("Target URL"):
            continue
        rows.append({
            "source_title": r.get("Source Page Title"),
            "source_url": r.get("Source URL"),
            "target_url": r.get("Target URL"),
            "domain_authority": parse_int(r.get("Domain Authority")),
            "page_authority": parse_int(r.get("Page Authority")),
            "spam_score": parse_float(r.get("Spam Score")),
            "anchor_text": r.get("Anchor Text"),
            "first_seen": parse_iso_date(r.get("First Seen")),
            "last_seen": parse_iso_date(r.get("Last Seen")),
        })
    return rows


def parse_top_pages(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = []
    for r in csv.DictReader(io.StringIO(text.lstrip("\ufeff"))):
        if not r.get("URL"):
            continue
        rows.append({
            "url": r.get("URL"),
            "title": r.get("Title"),
            "est_visits": parse_int(r.get("Est. Visits")),
            "backlinks": parse_int(r.get("Backlinks")),
        })
    return rows


def parse_domain_report(path: Path, report_type: str) -> tuple[dict, list[dict], str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    dm = re.search(r"(?m)^Domain\s*\n\s*([^\n]+)$", text)
    domain = normalize_domain(dm.group(1)) if dm else None
    em = re.search(r"Exported on\s*(?:\n\s*)?([^\n:]+(?::[^\n]+)?)", text)
    exported_at = None
    if em:
        adate = parse_mdy(em.group(1)) or parse_iso_date(em.group(1))
        if adate:
            exported_at = datetime.combine(adate, dt.time.min, tzinfo=timezone.utc)
    metrics = []
    if report_type == "backlinks":
        for metric, pattern in (
            ("domain_authority", r"(?m)^Domain Authority\s*\n\s*([\d.,]+)"),
            ("referring_domains", r"(?m)^Referring Domains\s*\n\s*([\d.,]+)"),
            ("backlinks", r"(?m)^Backlinks\s*\n\s*([\d.,]+)"),
        ):
            mm = re.search(pattern, text)
            val = parse_float(mm.group(1)) if mm else None
            if val is not None:
                metrics.append({"metric": metric, "value": val})
    return {"exported_at": exported_at}, metrics, domain


# ---------------------------------------------------------------- assembly

def _build_detail_rows(export: ExternalExport, source_type: str, payload, domain: str | None):
    """Expand a parser payload into (ModelClass, list[dict]) pairs to insert."""
    out = []
    row_domain = domain or export.domain
    if source_type == "search_console":
        for rec in payload["dims"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((SearchConsoleDim, rec))
        for rec in payload["daily"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((SearchConsoleDaily, rec))
    elif source_type == "ai_overview":
        for rec in payload["impressions"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((AIOverviewImpressions, rec))
    elif source_type == "ga4_event":
        for rec in payload["events"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((GA4Event, rec))
    elif source_type == "call_tracking":
        for rec in payload["calls"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((CallTracking, rec))
    elif source_type == "lead_summary":
        for rec in payload["leads"]:
            rec.update({"export_id": export.id})
            out.append((LeadSummary, rec))
    elif source_type == "keyword_estimate":
        for rec in payload["keywords"]:
            rec.update({"export_id": export.id, "domain": row_domain})
            out.append((KeywordEstimate, rec))
    elif source_type == "backlink":
        for rec in payload["backlinks"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((Backlink, rec))
    elif source_type == "top_page":
        for rec in payload["top_pages"]:
            rec.update({"export_id": export.id, "domain": export.domain})
            out.append((TopPage, rec))
    elif source_type in {"traffic", "backlinks"} and "raw_text" in payload:
        out.append((DomainReport, {
            "export_id": export.id, "domain": row_domain,
            "report_type": source_type, "source_file": export.file_name,
            "raw_text": payload["raw_text"],
        }))
        for rec in payload["metrics"]:
            rec.update({"export_id": export.id, "domain": row_domain})
            out.append((DomainMetric, rec))
    return out


def import_external_file(db, path: Path, force: bool = False) -> dict:
    """Import a single export file; returns a result dict (never raises)."""
    digest = file_sha256(path.read_bytes())
    existing = db.query(ExternalExport).filter(ExternalExport.file_hash == digest).first()
    if existing and not force:
        return {"filename": path.name, "status": "skipped", "rows": existing.row_count}

    source_type, domain, brand = classify(path)
    report_type = None
    if source_type.startswith("domain_report:"):
        source_type, report_type = source_type.split(":", 1)

    if source_type == "search_console":
        meta, dims, daily = parse_search_console(path)
        payload = {"dims": dims, "daily": daily}
    elif source_type == "ai_overview":
        meta, rows = parse_ai_overview(path)
        payload = {"impressions": rows}
    elif source_type == "ga4_event":
        meta, rows, content_domain = parse_ga4(path)
        payload = {"events": rows}
        domain = content_domain or domain
        brand = brand_for(domain) or brand
    elif source_type == "call_tracking":
        meta, calls = {}, parse_calls(path)
        payload = {"calls": calls}
    elif source_type == "lead_summary":
        meta, leads = parse_leads(path)
        payload = {"leads": leads}
    elif source_type == "keyword_estimate":
        meta, kws = {}, parse_kbt(path)
        payload = {"keywords": kws}
    elif source_type == "backlink":
        meta, bks = {}, parse_backlinks(path)
        payload = {"backlinks": bks}
    elif source_type == "top_page":
        meta, tps = {}, parse_top_pages(path)
        payload = {"top_pages": tps}
    elif report_type in {"traffic", "backlinks"}:
        meta, metrics, content_domain = parse_domain_report(path, report_type)
        domain = content_domain or domain
        payload = {"metrics": metrics,
                   "raw_text": path.read_text(encoding="utf-8", errors="replace")}
        source_type = report_type
    else:
        raise ValueError(f"Unknown type {source_type}")

    if existing and force:
        db.delete(existing)
        db.flush()

    export = ExternalExport(
        source_type=source_type,
        domain=domain or "unknown",
        brand=brand,
        file_name=path.name,
        file_hash=digest,
        period_from=meta.get("period_from"),
        period_to=meta.get("period_to"),
        exported_at=meta.get("exported_at"),
        status="imported",
    )
    db.add(export)
    db.flush()

    total = 0
    for model, rows in _build_detail_rows(export, source_type, payload, domain):
        if not rows:
            continue
        db.execute(insert(model), rows)
        total += len(rows)
    export.row_count = total
    db.commit()
    return {"filename": path.name, "status": "imported", "rows": total,
            "source_type": source_type}


def delete_external_export(db, export) -> None:
    """Delete an external export row plus every detail row it owns.

    Uses explicit deletes rather than relying on DB-level ON DELETE CASCADE so
    the behaviour is identical on SQLite (tests) and Postgres (prod).
    """
    for model in DETAIL_MODELS:
        db.query(model).filter(model.export_id == export.id).delete(synchronize_session=False)
    db.delete(export)


def import_external_folder(data_dir: Path, db, force: bool = False) -> list[dict]:
    """Import every export file under ``data_dir``; one bad file never blocks the rest."""
    results = []
    if not data_dir.is_dir():
        return [{"filename": str(data_dir), "status": "error",
                 "error": "external data path not found"}]
    for path in sorted(data_dir.rglob("*")):
        if not path.is_file():
            continue
        try:
            results.append(import_external_file(db, path, force=force))
        except Exception as e:  # noqa: BLE001 - per-file isolation
            logger.warning("Failed to import %s: %s", path.name, e)
            results.append({"filename": path.name, "status": "error", "error": str(e)})
    return results