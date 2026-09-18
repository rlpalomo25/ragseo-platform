"""Brand detection + brand-key consistency.

Regression: ``detect_brand`` must return the same key the external-data layer
understands (``BRAND_DOMAINS`` keys) so Klean Gutter jobs actually get market
context — previously ``detect_brand`` returned ``"klean_gutter"`` which no
``DOMAIN_FOR_BRAND`` entry mapped, silently skipping all market data.
"""
from datetime import datetime, timezone

from app.services.doctrine import BRAND_CONFIG, detect_brand
from app.models import external as m


def test_detect_brand_normalizes_klean_spellings():
    assert detect_brand("Write a local page for Klean Gutter") == "kleangutter"
    assert detect_brand("KleanGutter website structure") == "kleangutter"
    assert detect_brand("klean-gutter dealer page") == "kleangutter"
    assert detect_brand("brand: klean_gutter") == "kleangutter"
    assert detect_brand("MasterShield comparison") == "mastershield"
    assert detect_brand("MMGG gutter guards") == "mmgg"
    assert detect_brand("some unrelated roofing topic") == "generic"


def test_brand_config_uses_market_data_keys():
    # every brand key used for doctrine routing must resolve a market-domain key
    assert "kleangutter" in BRAND_CONFIG
    from app.services.external_data import DOMAIN_FOR_BRAND
    for brand in BRAND_CONFIG:
        assert brand in DOMAIN_FOR_BRAND


def test_klean_market_context_flows_from_detected_brand(db_session):
    exp = m.ExternalExport(
        source_type="search_console",
        domain="kleangutter.com",
        file_name="KleanGutter_GSC.csv",
        file_hash="klean-gsc-1",
        imported_at=datetime(2026, 9, 8, tzinfo=timezone.utc),
        row_count=1,
    )
    db_session.add(exp)
    db_session.commit()
    db_session.refresh(exp)
    db_session.add(m.SearchConsoleDim(
        export_id=exp.id, domain="kleangutter.com", dim_type="query",
        key="klean gutter near me", clicks=4, impressions=55, ctr=7.2, position=3.0))
    db_session.commit()

    from app.services.external_data import build_market_context

    brand = detect_brand("Write a Klean Gutter local page")
    assert brand == "kleangutter"
    context, _ = build_market_context(db_session, brand)
    assert "kleangutter.com" in context
    assert "klean gutter near me" in context
    assert "55 imp" in context