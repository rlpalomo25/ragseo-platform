"""Learning-loop service: register publications, snapshot weekly performance.

Doc 203 ("Simple Performance Record") + Doc 205 (flags) + Doc 145 (revenue
intelligence). ``snapshot_publications`` matches a registered publish URL
against the imported GSC / AI-Overview / call / top-page / keyword data and
stores one ``ContentPerformanceSnapshot`` per (publication, source export).
Deltas vs the previous snapshot become WoW movements; Doc 203 thresholds
produce flags recorded as ``LearningSignal`` rows for human (Doc 205) review.
Doctrine updates stay human-driven (Doc 203 sec. 4.0) — this layer records and
exposes signals only.

``build_learning_context`` turns the measurements into a "## Performance
Memory" block for the writer/router, returned under a SEPARATE
``learning_sources`` key so the agents' canonical ``provenance`` contract
(the exact-set assertions in the tests) stays untouched.
"""

import logging
from datetime import date
from urllib.parse import urlsplit
from uuid import UUID

from sqlalchemy.orm import Session as DBSession

from app.models.external import (
    AIOverviewImpressions,
    CallTracking,
    ExternalExport,
    KeywordEstimate,
    SearchConsoleDim,
    TopPage,
)
from app.models.job import AgentJob
from app.models.learning import ContentPerformanceSnapshot, ContentPublication, LearningSignal
from app.services.external_data import latest_export_ids
from app.services.external_ingest import BRAND_DOMAINS, DOMAIN_ALIASES

logger = logging.getLogger(__name__)

# Doc 203 sec. 2.0: flag pages that moved >3 positions (either direction) or
# changed >20% in CTR / engagement between snapshots.
POSITION_FLAG_DELTA = 3.0
CTR_FLAG_DELTA = 0.20  # relative change

FLAG_LABELS = {
    "position_drop": "continued / decreased ranking (>3 positions change)",
    "ctr_drop": "CTR change beyond 20%",
    "movement": "impressions/visibility change beyond 20%",
    "ai_zero": "zero AI-Overview impressions on latest snapshot",
    "unmeasurable": "no ranking data matched this publication (Doc 203 sec. 8.0)",
}


def normalize_url(url: str) -> str:
    """Canonicalize a URL for matching: lowercase, no scheme/www/trailing slash."""
    if not url:
        return ""
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/").lower()
    if host:
        return f"{host}{path}"
    # Bare path or loose text — normalize without a host.
    return url.strip().lower().strip("/")


def _url_match(pub: str, candidate: str | None) -> bool:
    """True when a stored URL/path row matches the publication URL."""
    if not candidate:
        return False
    norm_pub = normalize_url(pub)
    norm_row = normalize_url(candidate)
    if not norm_pub or not norm_row:
        return False
    if norm_row == norm_pub:
        return True
    # Row may store a bare path (call tracking pages); match path only.
    _, _, pub_path = norm_pub.partition("/")
    if not norm_row.startswith("/") and len(norm_row) < len(norm_pub):
        return False
    return norm_row.endswith(pub_path) if pub_path else False


def _host_of(url: str) -> str:
    host = urlsplit(url.strip()).hostname or ""
    host = host.lower()
    return host[4:] if host.startswith("www.") else host


def _canonical_domain(url: str) -> str | None:
    """Map a publication host to a canonical known domain (brand or competitor)."""
    host = _host_of(url)
    if not host:
        return None
    if host in BRAND_DOMAINS:
        return host
    return DOMAIN_ALIASES.get(host) or host


def _newest_export(db: DBSession, domain: str) -> ExternalExport | None:
    """The newest export row for a domain (cycle anchor for snapshots)."""
    return (
        db.query(ExternalExport)
        .filter(ExternalExport.domain == domain)
        .order_by(ExternalExport.imported_at.desc(), ExternalExport.id.desc())
        .first()
    )


def register_publication(
    db: DBSession,
    job_id: UUID,
    url: str,
    published_at: date | None = None,
    keyword: str | None = None,
) -> ContentPublication:
    """Link a published URL (and optional target keyword) to a job."""
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if not job:
        raise ValueError(f"Job {job_id} not found")
    if not normalize_url(url):
        raise ValueError("publish_url must be a non-empty URL")
    pub = ContentPublication(
        job_id=job_id,
        publish_url=url.strip(),
        publish_date=published_at,
        target_keyword=(keyword or "").strip() or None,
        status="active",
    )
    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub


def _percent_change(now, prev) -> float | None:
    if now is None or prev is None or prev == 0:
        return None
    return (now - prev) / prev


def _gather_metrics(db: DBSession, pub: ContentPublication, domain: str) -> dict:
    """Pull this cycle's per-URL metrics for a publication from the latest exports."""
    latest = latest_export_ids(db, domain)
    metrics: dict = {
        "position": None,
        "clicks": 0,
        "impressions": 0,
        "ctr": None,
        "ai_overview_impressions": 0,
        "calls": 0,
        "est_visits": None,
    }

    # GSC pages dimension (per-URL ranking health).
    page_q = db.query(SearchConsoleDim).filter(
        SearchConsoleDim.domain == domain, SearchConsoleDim.dim_type == "page"
    )
    if latest.get("search_console"):
        page_q = page_q.filter(SearchConsoleDim.export_id == latest["search_console"])
    page_best = None
    for row in page_q.all():
        if not _url_match(pub.publish_url, row.key):
            continue
        if page_best is None or row.impressions > page_best.impressions:
            page_best = row
    if page_best:
        metrics["clicks"] = page_best.clicks
        metrics["impressions"] = page_best.impressions
        metrics["ctr"] = page_best.ctr
        metrics["position"] = page_best.position

    # Target keyword ranking position (Doc 203 wants the keyword-level rank).
    if pub.target_keyword:
        kw_q = db.query(SearchConsoleDim).filter(
            SearchConsoleDim.domain == domain, SearchConsoleDim.dim_type == "query"
        )
        if latest.get("search_console"):
            kw_q = kw_q.filter(SearchConsoleDim.export_id == latest["search_console"])
        kw_norm = normalize_url(pub.target_keyword).replace("/", "")
        kw_row = next(
            (r for r in kw_q.all() if normalize_url(r.key).replace("/", "") == kw_norm),
            None,
        )
        if kw_row is not None:
            metrics["position"] = kw_row.position
        else:
            # Fall back to Ubersuggest keyword tables by ranking URL.
            kq = db.query(KeywordEstimate).filter(
                KeywordEstimate.domain == domain, KeywordEstimate.ranking_url.isnot(None)
            )
            if latest.get("keyword_estimate"):
                kq = kq.filter(KeywordEstimate.export_id == latest["keyword_estimate"])
            krow = next(
                (
                    r
                    for r in kq.all()
                    if _url_match(pub.publish_url, r.ranking_url)
                    and normalize_url(r.keyword).replace("/", "") == kw_norm
                ),
                None,
            )
            if krow is not None:
                metrics["position"] = krow.position

    # AI-Overview impressions captured for this page.
    ai_imp = 0
    ai_q = db.query(AIOverviewImpressions.key, AIOverviewImpressions.impressions).filter(
        AIOverviewImpressions.domain == domain, AIOverviewImpressions.dim_type == "pages"
    )
    if latest.get("ai_overview"):
        ai_q = ai_q.filter(AIOverviewImpressions.export_id == latest["ai_overview"])
    for key, imp in ai_q.all():
        if _url_match(pub.publish_url, key):
            ai_imp += imp or 0
    metrics["ai_overview_impressions"] = ai_imp

    # Phone calls landing on this page (call tracking page/last_url).
    call_q = db.query(CallTracking).filter(CallTracking.domain == domain)
    if latest.get("call_tracking"):
        call_q = call_q.filter(CallTracking.export_id == latest["call_tracking"])
    for row in call_q.all():
        if _url_match(pub.publish_url, row.page) or _url_match(pub.publish_url, row.last_url):
            metrics["calls"] += 1

    # Estimated organic visits from Ubersuggest top-pages.
    tp = db.query(TopPage).filter(TopPage.domain == domain)
    if latest.get("top_page"):
        tp = tp.filter(TopPage.export_id == latest["top_page"])
    trow = next((r for r in tp.all() if _url_match(pub.publish_url, r.url)), None)
    if trow is not None:
        metrics["est_visits"] = trow.est_visits

    return metrics


def _previous_snapshot(db: DBSession, pub_id: UUID, anchor_id: UUID) -> ContentPerformanceSnapshot | None:
    return (
        db.query(ContentPerformanceSnapshot)
        .join(ExternalExport, ExternalExport.id == ContentPerformanceSnapshot.source_export_id)
        .filter(
            ContentPerformanceSnapshot.publication_id == pub_id,
            ContentPerformanceSnapshot.source_export_id != anchor_id,
        )
        .order_by(ExternalExport.imported_at.desc(), ExternalExport.id.desc())
        .first()
    )


def _flags_for(cur: dict, prev: ContentPerformanceSnapshot | None) -> list[str]:
    flags: list[str] = []
    if (
        cur.get("position") is not None
        and prev is not None
        and prev.position is not None
        and abs(cur["position"] - prev.position) > POSITION_FLAG_DELTA
    ):
        flags.append("position_drop")
    if cur.get("ai_overview_impressions") == 0:
        flags.append("ai_zero")
    if cur.get("position") is None and cur.get("impressions") == 0:
        # No GSC/keyword match at all -> unmeasurable this cycle (Doc 203 sec. 8.0).
        flags.append("unmeasurable")
    if prev is not None:
        pct_ctr = _percent_change(cur.get("ctr"), prev.ctr)
        if pct_ctr is not None and abs(pct_ctr) > CTR_FLAG_DELTA:
            flags.append("ctr_drop")
        pct_imp = _percent_change(cur.get("impressions"), prev.impressions)
        if prev.impressions and pct_imp is not None and abs(pct_imp) > CTR_FLAG_DELTA:
            flags.append("movement")
    return flags


def _record_signals(db: DBSession, pub: ContentPublication, snapshot: ContentPerformanceSnapshot) -> int:
    created = 0
    period_label = ""
    if snapshot.period_to and snapshot.period_from:
        period_label = (
            f"Week {snapshot.period_from.month}/{snapshot.period_from.day}-"
            f"{snapshot.period_to.month}/{snapshot.period_to.day}"
        )

    for flag in snapshot.flags or []:
        observation = (
            f"Flag '{flag}' ({FLAG_LABELS.get(flag, flag)}) on {pub.publish_url} — "
            f"{period_label or 'latest cycle'}: pos {snapshot.position}, "
            f"{snapshot.impressions} imp, ctr {snapshot.ctr}"
        )
        dup = (
            db.query(LearningSignal)
            .filter(
                LearningSignal.publication_id == pub.id,
                LearningSignal.source == f"pub_perf:{flag}",
                LearningSignal.observation == observation,
            )
            .first()
        )
        if dup:
            continue
        db.add(
            LearningSignal(
                publication_id=pub.id,
                source=f"pub_perf:{flag}",
                observation=observation,
            )
        )
        created += 1
    if created:
        db.commit()
    return created


def snapshot_publications(db: DBSession, force: bool = False) -> dict:
    """Recompute the latest performance snapshot for every active publication."""
    stats = {"publications": 0, "snapshots": 0, "signals": 0}
    publications = db.query(ContentPublication).filter(ContentPublication.status == "active").all()
    stats["publications"] = len(publications)

    for pub in publications:
        domain = _canonical_domain(pub.publish_url)
        if not domain:
            continue
        export = _newest_export(db, domain)
        if export is None:
            continue

        anchor_id = export.id
        if force:
            db.query(ContentPerformanceSnapshot).filter(
                ContentPerformanceSnapshot.publication_id == pub.id,
                ContentPerformanceSnapshot.source_export_id == anchor_id,
            ).delete(synchronize_session=False)
            db.commit()

        # Idempotency: one snapshot per (publication, export) via the unique index.
        existing = (
            db.query(ContentPerformanceSnapshot)
            .filter(
                ContentPerformanceSnapshot.publication_id == pub.id,
                ContentPerformanceSnapshot.source_export_id == anchor_id,
            )
            .first()
        )
        if existing:
            stats["snapshots"] += 1
            continue

        prev = _previous_snapshot(db, pub.id, anchor_id)
        cur = _gather_metrics(db, pub, domain)
        flags = _flags_for(cur, prev)

        movement = None
        movement_ctr = None
        movement_impressions = None
        if prev is not None:
            if cur["position"] is not None and prev.position is not None:
                movement = round(cur["position"] - prev.position, 2)
            if cur["ctr"] is not None and prev.ctr is not None:
                movement_ctr = round(cur["ctr"] - prev.ctr, 4)
            movement_impressions = (
                cur["impressions"] - prev.impressions if prev.impressions is not None else None
            )

        snapshot = ContentPerformanceSnapshot(
            publication_id=pub.id,
            source_export_id=anchor_id,
            period_from=export.period_from,
            period_to=export.period_to,
            position=cur["position"],
            clicks=cur["clicks"],
            impressions=cur["impressions"],
            ctr=cur["ctr"],
            ai_overview_impressions=cur["ai_overview_impressions"],
            calls=cur["calls"],
            est_visits=cur["est_visits"],
            movement=movement,
            movement_ctr=movement_ctr,
            movement_impressions=movement_impressions,
            flags=flags,
        )
        db.add(snapshot)
        try:
            db.commit()
        except Exception:
            logger.exception("Failed to persist snapshot for %s", pub.url)
            db.rollback()
            continue
        stats["snapshots"] += 1
        stats["signals"] += _record_signals(db, pub, snapshot)

    return stats


def build_learning_context(db: DBSession, brand: str, topic: str = "") -> tuple[str, list[dict]]:
    """Return ("## Performance Memory" block, learning_sources) for a brand.

    The provenance list is a SEPARATE ``learning_sources`` key — never merged
    into the agents' ``provenance`` (which tests assert as an exact set).
    """
    domain = next((d for d, b in BRAND_DOMAINS.items() if b == brand), None)
    if not domain:
        return "", []

    pubs = (
        db.query(ContentPublication)
        .join(AgentJob, AgentJob.id == ContentPublication.job_id)
        .filter(AgentJob.brand == brand, ContentPublication.status == "active")
        .order_by(ContentPublication.created_at.desc())
        .limit(20)
        .all()
    )
    if not pubs:
        return "", []

    lines = ["### Performance Memory (past published content measured weekly)"]
    for pub in pubs:
        snap = (
            db.query(ContentPerformanceSnapshot)
            .join(ExternalExport, ExternalExport.id == ContentPerformanceSnapshot.source_export_id)
            .filter(ContentPerformanceSnapshot.publication_id == pub.id)
            .order_by(ExternalExport.imported_at.desc(), ExternalExport.id.desc())
            .first()
        )
        if snap is None:
            lines.append(
                f"  - {pub.publish_url} — registered, waiting for next data import"
                f"{(' (keyword ' + pub.target_keyword + ')') if pub.target_keyword else ''}"
            )
            continue
        parts = [f"pos {snap.position:.1f}" if snap.position is not None else "pos n/a"]
        if snap.movement is not None:
            arrow = "up" if snap.movement <= 0 else "down"
            parts.append(f"moved {abs(snap.movement):.1f} {arrow}")
        parts.append(f"{snap.impressions:,} imp · {snap.clicks:,} clicks")
        if snap.ctr is not None:
            parts.append(f"CTR {snap.ctr:.1f}%")
        parts.append(f"{snap.ai_overview_impressions} AI-imp")
        parts.append(f"{snap.calls} calls")
        if snap.est_visits is not None:
            parts.append(f"~{snap.est_visits:,} visits")
        if snap.movement_ctr is not None:
            parts.append(f"CTR Δ {snap.movement_ctr:+.1f}pp")
        if snap.impressions is not None and snap.movement_impressions is not None:
            parts.append(f"imp Δ {snap.movement_impressions:+d}")
        if snap.flags:
            parts.append("flags: " + ", ".join(FLAG_LABELS.get(f, f) for f in snap.flags))
        kw = f' (keyword "{pub.target_keyword}")' if pub.target_keyword else ""
        pub_date = f"published {pub.publish_date}" if pub.publish_date else "published?"
        lines.append(
            f"  - [{snap.period_to or 'latest'}] {pub.publish_url}{kw} {pub_date} — {', '.join(parts)}"
        )

    context = "\n".join(lines)
    sources = [
        {
            "doc_number": "MEMORY",
            "title": "Learning loop: measured performance of published content",
            "version": None,
        }
    ]
    return context, sources
