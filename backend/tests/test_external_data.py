"""Week-windowing: market context must only reflect the newest export per type.

Two weekly exports for the same domain (later ``imported_at``) must not let the
older one leak into ``build_market_context`` strings; aggregations collapse to
the single latest snapshot per source type.
"""

from datetime import UTC, datetime

from app.models import external as m
from app.services.external_data import build_market_context, latest_export_ids


def _utc(y, mo, d):
    return datetime(y, mo, d, tzinfo=UTC)


def _export(db, source_type, domain, day, seq):
    exp = m.ExternalExport(
        source_type=source_type,
        domain=domain,
        file_name=f"{source_type}-{seq:02d}.csv",
        file_hash=f"{source_type}-{domain}-{seq}-hash",
        imported_at=day,
        row_count=1,
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


def testlatest_export_ids_picks_newest_per_type(db_session):
    old = _export(db_session, "search_console", "kleangutter.com", _utc(2026, 9, 1), 1)
    new = _export(db_session, "search_console", "kleangutter.com", _utc(2026, 9, 8), 2)
    ai = _export(db_session, "ai_overview", "kleangutter.com", _utc(2026, 9, 8), 3)

    latest = latest_export_ids(db_session, "kleangutter.com")

    assert latest["search_console"] == new.id
    assert latest["ai_overview"] == ai.id
    assert old.id not in latest.values()
    assert latest_export_ids(db_session, "unknown.com") == {}


def testlatest_export_ids_tie_breaks_deterministically(db_session):
    a = _export(db_session, "keyword_estimate", "leaffilter.com", _utc(2026, 9, 8), 1)
    b = _export(db_session, "keyword_estimate", "leaffilter.com", _utc(2026, 9, 8), 2)

    first = latest_export_ids(db_session, "leaffilter.com")["keyword_estimate"]

    assert first in (a.id, b.id)
    assert latest_export_ids(db_session, "leaffilter.com")["keyword_estimate"] == first


def test_market_context_only_shows_latest_gsc_export(db_session):
    old = _export(db_session, "search_console", "kleangutter.com", _utc(2026, 9, 1), 1)
    new = _export(db_session, "search_console", "kleangutter.com", _utc(2026, 9, 8), 2)
    db_session.add(
        m.SearchConsoleDim(
            export_id=old.id,
            domain="kleangutter.com",
            dim_type="query",
            key="outdated query",
            clicks=1,
            impressions=900000,
        )
    )
    db_session.add(
        m.SearchConsoleDim(
            export_id=new.id,
            domain="kleangutter.com",
            dim_type="query",
            key="fresh query",
            clicks=1,
            impressions=123,
        )
    )
    db_session.commit()

    context, provenance = build_market_context(db_session, "kleangutter")

    assert "fresh query" in context
    assert "123 imp" in context
    assert "outdated query" not in context
    assert "900,000" not in context
    assert provenance[0]["doc_number"] == "MARKET"


def test_competitor_snapshot_scoped_to_latest_keyword_export(db_session):
    old = _export(db_session, "keyword_estimate", "leaffilter.com", _utc(2026, 9, 1), 1)
    new = _export(db_session, "keyword_estimate", "leaffilter.com", _utc(2026, 9, 8), 2)
    db_session.add(
        m.KeywordEstimate(
            export_id=old.id,
            domain="leaffilter.com",
            keyword="old competitor kw",
            position=2.0,
            est_visits=9999,
        )
    )
    db_session.add(
        m.KeywordEstimate(
            export_id=new.id, domain="leaffilter.com", keyword="new competitor kw", position=1.0, est_visits=7
        )
    )
    db_session.commit()

    context, _ = build_market_context(db_session, "kleangutter")

    assert "leaffilter.com" in context
    assert 'top kw "new competitor kw"' in context
    assert "old competitor kw" not in context


def test_brand_health_scoped_to_latest_report_export(db_session):
    old = _export(db_session, "backlinks", "kleangutter.com", _utc(2026, 9, 1), 1)
    new = _export(db_session, "backlinks", "kleangutter.com", _utc(2026, 9, 8), 2)
    db_session.add(
        m.DomainMetric(export_id=old.id, domain="kleangutter.com", metric="domain_authority", value=41)
    )
    db_session.add(
        m.DomainMetric(export_id=new.id, domain="kleangutter.com", metric="domain_authority", value=55)
    )
    db_session.commit()

    context, _ = build_market_context(db_session, "kleangutter")

    assert "Domain Authority: 55" in context
    assert "Domain Authority: 41" not in context
