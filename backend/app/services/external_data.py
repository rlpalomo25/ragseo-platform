"""Query helpers that turn raw external market data into agent-facing context.

``build_market_context(db, brand)`` is the main entry point: it pulls the
most-recent weekly snapshot for the given brand's money-site domain and
returns a (context_text, provenance) pair that plugs straight into the
Writer or Router agent prompt (Doc 329/C17 provenance style).

Every aggregation is scoped to the newest export of its source type for the
domain, so overlapping weekly imports (dedup by file sha256) never inflate
"this week" numbers with older history.
"""

from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from app.models.external import (
    AIOverviewImpressions,
    CallTracking,
    DomainMetric,
    ExternalExport,
    GA4Event,
    KeywordEstimate,
    LeadSummary,
    SearchConsoleDim,
    TopPage,
)
from app.services.external_ingest import BRAND_DOMAINS

DOMAIN_FOR_BRAND = {v: k for k, v in BRAND_DOMAINS.items()}

COMPETITOR_DOMAINS = [
    "leaffilter.com",
    "leafguard.com",
    "gutterhelmet.com",
    "gutterguardsamerica.com",
]


def _fmt_pct(v) -> str:
    if v is None:
        return "—"
    return f"{v:.1f}%"


def _fmt_int(v) -> str:
    if v is None:
        return "—"
    return f"{v:,}"


def _get_export_period(db: DBSession, domain: str) -> tuple[str | None, date | None, date | None]:
    row = (
        db.query(ExternalExport.period_from, ExternalExport.period_to, ExternalExport.file_name)
        .filter(ExternalExport.domain == domain)
        .order_by(ExternalExport.imported_at.desc())
        .first()
    )
    if not row:
        return None, None, None
    pf = row.period_from.date() if row.period_from else None
    pt = row.period_to.date() if row.period_to else None
    return row.file_name, pf, pt


def latest_export_ids(db: DBSession, domain: str) -> dict[str, UUID]:
    """Latest external_exports.id per source_type for a domain.

    "Latest" is decided by (imported_at, id): a tie on the import timestamp
    resolves deterministically to the highest (latest-created) export id so
    overlapping weekly files always collapse to a single snapshot.
    """
    best: dict[str, tuple[datetime, UUID]] = {}
    for row in db.query(ExternalExport).filter(ExternalExport.domain == domain).all():
        ts = row.imported_at if isinstance(row.imported_at, datetime) else datetime.min
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        key = (ts, row.id)
        if row.source_type not in best or key > best[row.source_type]:
            best[row.source_type] = key
    return {source_type: export_id for source_type, (_, export_id) in best.items()}


def _gsc_summary(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    q = db.query(SearchConsoleDim).filter(
        SearchConsoleDim.domain == domain, SearchConsoleDim.dim_type == "query"
    )
    if latest.get("search_console"):
        q = q.filter(SearchConsoleDim.export_id == latest["search_console"])
    dims = q.order_by(SearchConsoleDim.impressions.desc()).limit(12).all()
    if not dims:
        return "(no GSC query data)"
    lines = ["Top queries ranked in GSC (impressions / clicks / avg CTR / position):"]
    for d in dims:
        lines.append(
            f'  - "{d.key}" — {_fmt_int(d.impressions)} imp, {_fmt_int(d.clicks)} clicks, '
            f"CTR {_fmt_pct(d.ctr)}, pos {d.position:.1f}"
            if d.position
            else f'  - "{d.key}" — {_fmt_int(d.impressions)} imp, {_fmt_int(d.clicks)} clicks, '
            f"CTR {_fmt_pct(d.ctr)}"
        )
    return "\n".join(lines)


def _ai_summary(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    total_q = db.query(func.coalesce(func.sum(AIOverviewImpressions.impressions), 0)).filter(
        AIOverviewImpressions.domain == domain
    )
    if latest.get("ai_overview"):
        total_q = total_q.filter(AIOverviewImpressions.export_id == latest["ai_overview"])
    total = total_q.scalar()
    per_page_q = db.query(AIOverviewImpressions.key, AIOverviewImpressions.impressions).filter(
        AIOverviewImpressions.domain == domain, AIOverviewImpressions.dim_type == "pages"
    )
    if latest.get("ai_overview"):
        per_page_q = per_page_q.filter(AIOverviewImpressions.export_id == latest["ai_overview"])
    per_page = per_page_q.order_by(AIOverviewImpressions.impressions.desc()).limit(5).all()
    if not total:
        return ""
    lines = [f"AI-Overview impressions (week): {_fmt_int(total)} total"]
    for key, imp in per_page:
        lines.append(f"  - {key}: {imp} imp")
    return "\n".join(lines)


def _ga4_summary(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    q = db.query(GA4Event.event_name, GA4Event.event_count).filter(GA4Event.domain == domain)
    if latest.get("ga4_event"):
        q = q.filter(GA4Event.export_id == latest["ga4_event"])
    events = q.all()
    if not events:
        return "(no GA4 data)"
    parts = [f"{name}: {_fmt_int(count)}" for name, count in events]
    return "GA4 events (week): " + ", ".join(parts)


def _calls_summary(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    scope = []
    if latest.get("call_tracking"):
        scope.append(CallTracking.export_id == latest["call_tracking"])
    total = (
        db.query(func.count(CallTracking.id)).filter(CallTracking.domain == domain, *scope).scalar()
    ) or 0
    if total == 0:
        return "(no call data)"
    answered = (
        db.query(func.count(CallTracking.id))
        .filter(CallTracking.domain == domain, CallTracking.status == "answered", *scope)
        .scalar()
    ) or 0
    avg_dur = (
        db.query(func.avg(CallTracking.duration_seconds))
        .filter(CallTracking.domain == domain, CallTracking.duration_seconds > 0, *scope)
        .scalar()
    ) or 0
    top_query = (
        db.query(CallTracking.search_query)
        .filter(
            CallTracking.domain == domain,
            CallTracking.search_query.isnot(None),
            CallTracking.search_query != "",
            *scope,
        )
        .limit(1)
        .scalar()
    ) or "—"
    return (
        f"Calls: {total} total, {answered} answered, "
        f"avg duration {int(avg_dur // 60)}m{int(avg_dur % 60):02d}s; "
        f'top search query: "{top_query}"'
    )


def _leads_summary(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    row = db.query(LeadSummary).filter(LeadSummary.domain == domain)
    if latest.get("lead_summary"):
        row = row.filter(LeadSummary.export_id == latest["lead_summary"])
    row = row.order_by(LeadSummary.id.desc()).first()
    if row:
        return f"Leads (week): {row.form_fills} form fills, {row.vapi_calls} VAPI calls"
    row_all = db.query(LeadSummary).filter(LeadSummary.domain == "all")
    if latest.get("lead_summary"):
        row_all = row_all.filter(LeadSummary.export_id == latest["lead_summary"])
    row_all = row_all.order_by(LeadSummary.id.desc()).first()
    if row_all:
        return f"Leads (week aggregate): {row_all.form_fills} form fills, {row_all.vapi_calls} VAPI calls"
    return "(no lead data)"


def _top_pages_summary(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    q = db.query(TopPage).filter(TopPage.domain == domain)
    if latest.get("top_page"):
        q = q.filter(TopPage.export_id == latest["top_page"])
    pages = q.order_by(TopPage.est_visits.desc().nullslast()).limit(5).all()
    if not pages:
        return ""
    lines = ["Top organic pages (by est. visits):"]
    for p in pages:
        lines.append(f"  - {p.url} — {_fmt_int(p.est_visits)} visits, {p.backlinks or 0} backlinks")
    return "\n".join(lines)


def _brand_health(db: DBSession, domain: str, latest: dict[str, UUID]) -> str:
    report_ids = [latest[k] for k in ("backlinks", "traffic") if latest.get(k)]
    parts = []
    for metric in ["domain_authority", "referring_domains", "backlinks"]:
        q = db.query(DomainMetric.value).filter(DomainMetric.domain == domain, DomainMetric.metric == metric)
        if report_ids:
            q = q.filter(DomainMetric.export_id.in_(report_ids))
        val = q.order_by(DomainMetric.id.desc()).scalar()
        if val is not None:
            label = metric.replace("_", " ").title()
            formatted = f"{int(val):,}" if float(val).is_integer() else f"{val:,.1f}"
            parts.append(f"{label}: {formatted}")
    if not parts:
        return ""
    return "Brand backlink profile (source: Ubersuggest): " + ", ".join(parts)


def _competitor_snapshot(db: DBSession) -> str:
    lines = []
    for dom in COMPETITOR_DOMAINS:
        latest = latest_export_ids(db, dom)
        report_ids = [latest[k] for k in ("backlinks", "traffic") if latest.get(k)]
        da_q = db.query(DomainMetric.value).filter(
            DomainMetric.domain == dom, DomainMetric.metric == "domain_authority"
        )
        if report_ids:
            da_q = da_q.filter(DomainMetric.export_id.in_(report_ids))
        da = da_q.order_by(DomainMetric.id.desc()).scalar()
        kw_q = db.query(KeywordEstimate.keyword, KeywordEstimate.position, KeywordEstimate.est_visits).filter(
            KeywordEstimate.domain == dom
        )
        if latest.get("keyword_estimate"):
            kw_q = kw_q.filter(KeywordEstimate.export_id == latest["keyword_estimate"])
        kw = kw_q.order_by(KeywordEstimate.est_visits.desc().nullslast()).limit(1).first()
        parts = [f"DA {int(da)}" if da is not None else "DA —"]
        if kw and kw[1] is not None:
            parts.append(f'top kw "{kw[0]}" pos {kw[1]:.0f}, ~{_fmt_int(kw[2])} visits')
        lines.append(f"  - {dom}: {', '.join(parts)}")
    if not lines:
        return ""
    return "Competitor snapshot (source: Ubersuggest):\n" + "\n".join(lines)


def build_market_context(db: DBSession, brand: str) -> tuple[str, list[dict]]:
    """Return (context_block, provenance_list) for a brand's latest weekly data.

    ``brand`` is one of "kleangutter", "mastershield", "mmgg".
    """
    domain = DOMAIN_FOR_BRAND.get(brand)
    if not domain:
        return "", []

    latest = latest_export_ids(db, domain)

    _, pf, pt = _get_export_period(db, domain)
    period_label = ""
    if pf and pt:
        period_label = f"Week {pf.month}/{pf.day}-{pt.month}/{pt.day}/{pt.year}"
    elif pf:
        period_label = f"Week starting {pf.month}/{pf.day}/{pf.year}"

    blocks = [
        f"### Market Data for {domain} ({period_label})\n",
        _gsc_summary(db, domain, latest),
        _ai_summary(db, domain, latest),
        _ga4_summary(db, domain, latest),
        _calls_summary(db, domain, latest),
        _leads_summary(db, domain, latest),
        _brand_health(db, domain, latest),
        _top_pages_summary(db, domain, latest),
    ]
    comp = _competitor_snapshot(db)
    if comp:
        blocks.append(comp)

    context = "\n\n".join(b for b in blocks if b)
    provenance = [
        {
            "doc_number": "MARKET",
            "title": f"External market data ({period_label or 'latest import'})",
            "version": None,
        }
    ]
    return context, provenance
