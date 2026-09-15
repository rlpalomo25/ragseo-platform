import io
import zipfile
from datetime import datetime, timezone

import pytest

from app.services.external_ingest import (
    classify,
    parse_duration_seconds,
    parse_leads,
    parse_top_pages,
    import_external_folder,
)
from app.services.external_data import build_market_context


def make_gsc_zip(domain="kleangutter"):
    buf = io.BytesIO()
    inner = io.BytesIO()
    with zipfile.ZipFile(inner, "w") as z:
        z.writestr("Chart.csv", "Date,Clicks,Impressions,CTR,Position\n"
                                "2026-08-28,10,100,10,5.2\n2026-08-29,20,120,16.67,4.5\n")
        z.writestr("Queries.csv", "Top queries,Clicks,Impressions,CTR,Position\n"
                                  "gutter guard cost,22,300,7.33,3.1\n"
                                  "klean gutter,8,90,8.89,1.0\n")
        z.writestr("Pages.csv", "Top pages,Clicks,Impressions,CTR,Position\n"
                                "https://kleangutter.com/,12,180,6.67,4.0\n")
        z.writestr("Countries.csv", "Country,Clicks,Impressions,CTR,Position\n"
                                    "United States,25,380,6.58,3.5\n")
        z.writestr("Devices.csv", "Device,Clicks,Impressions,CTR,Position\n"
                                  "Mobile,18,240,7.5,3.8\n")
        z.writestr("Filters.csv", "Filter,Value\nSearch type,Web\nDate,\"Aug 28, 2026-Sep 3, 2026\"\n")
    outer = io.BytesIO()
    with zipfile.ZipFile(outer, "w") as z:
        z.writestr(f"{domain}_GSC_Export_[09112026].csv", inner.getvalue())
    return outer.getvalue()


def make_ai_zip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("Chart.csv", "Date,Impressions\n2026-08-28,22\n2026-08-29,23\n")
        z.writestr("Pages.csv", "Top pages,Impressions\nhttps://kleangutter.com/,41\n")
        z.writestr("Countries.csv", "Country,Impressions\nUnited States,40\n")
        z.writestr("Devices.csv", "Device,Impressions\nDesktop,30\n")
        z.writestr("Filters.csv", "Filter,Value\nDate,\"Aug 28, 2026-Sep 3, 2026\"\n")
    return buf.getvalue()


GA4_CSV = """# ----------------------------------------
# Events: Event name
# Account: KleanGutter
# Property: Kleangutter.com - GA4
# ----------------------------------------
# Start date: 20260827
# End date: 20260903
Event name,Event count,Total users,Event count per active user,Total revenue
page_view,200,98,2.13,0
submit_lead_form,1,1,1,0
"""

CALLS_CSV = ('Name,Customer #,Tracking Source,Call Status,Search Query,Referral,Page,'
             'Last URL,Likelihood,Message Body,Duration,Ring Time,Talk Time,Date\n'
             '"Marty SOUTHERLAND",(615) 618-2000,Website,answered,"gutter guards",,'
             '/how-it-works/,https://kleangutter.com/,0.9,"Called for quote",'
             '00:03:40,00:02:47,00:00:48,2026-09-04\n')

LEADS_TXT = ("Week ending: 09-04-2026 (08/28 - 09/04)\n\n"
             "MasterShield: 21 leads\n  - Form fills: 21\n  - VAPI calls: 0\n\n"
             "Klean Gutter: 2 leads\n  - Form fills: 2\n  - VAPI calls: 0\n")

KBT_CSV = ("\ufeffNo,Keywords,Volume,Position,Est. Visits,SEO Difficulty,CPC,Ranking URL\n"
           "1,klean gutter,90,1,31,31,0.0,http://kleangutter.com/\n"
           "2,micro mesh gutter guards,12100,5,158,25,4.72,http://kleangutter.com/\n")

BACKLINK_CSV = ("\ufeffNo,Source Page Title,Source URL,Target URL,Domain Authority,Page Authority,"
                "Spam Score,Anchor Text,First Seen,Last Seen\n"
                '1,"Review","https://imdb.example/x","https://kleangutter.com/",95,69,5,"review",'
                "2023-03-23,2026-06-30\n")

TOP_PAGES_CSV = ("\ufeffNo,URL,Title,Est. Visits,Backlinks\n"
                 '1,"http://kleangutter.com/christmas-light-clips/","How to Hang Lights",24,5\n'
                 '2,"http://kleangutter.com/","Klean Gutter",21,159\n')

TRAFFIC_MD = """# Assessment Report

Exported on September 3, 2026
Domain
kleangutter.com
Language & Location
English | United States
Overview metrics
"""

BACKLINKS_MD = """# Assessment Report

REPORT
Backlink Overview
Exported on
Sep 4, 2026 1:46 PM
Domain
kleangutter.com
Domain Authority
41
GOOD
Referring Domains
2,527
GOOD
Backlinks
46,323
GOOD
"""


@pytest.fixture()
def external_dir(tmp_path):
    """A pastiche of the weekly 09042026 folder with every export type present."""
    (tmp_path / "KleanGutter_GSC_Export_[09112026].csv.zip.zip").write_bytes(make_gsc_zip())
    (tmp_path / "kleangutter.com-AI-Features-2026-09-03.zip").write_bytes(make_ai_zip())
    (tmp_path / "Kleangutter-Performance-on-Search-2026-09-04 csv.csv").write_text(GA4_CSV, encoding="utf-8")
    (tmp_path / "Klean Gutter- calls export from 2026-08-28 to 2026-09-04.csv").write_text(CALLS_CSV, encoding="utf-8")
    (tmp_path / "Leads_Summary_Week_08-28-2026_to_09-04-2026.txt").write_text(LEADS_TXT, encoding="utf-8")
    (tmp_path / "MasterShield.com_KBT.csv (3).csv").write_text(KBT_CSV, encoding="utf-8")
    (tmp_path / "LeafFilter.com_Backlinks.csv (4).csv").write_text(BACKLINK_CSV, encoding="utf-8")
    (tmp_path / "Top Pages kleangutter.com.csv").write_text(TOP_PAGES_CSV, encoding="utf-8")
    (tmp_path / "kleangutter.com_Traffic_Overview.pdf (3).md").write_text(TRAFFIC_MD, encoding="utf-8")
    (tmp_path / "kleangutter.com_Backlinks_Overview.pdf (3).md").write_text(BACKLINKS_MD, encoding="utf-8")
    return tmp_path


# ------------------------------------------------------------------- classifier

def test_classify_all_known_types(tmp_path):
    from pathlib import Path

    kbt_header = "No,Keywords,Volume,Position,Est. Visits,SEO Difficulty,CPC,Ranking URL"
    kbt_like = "No,URL,Title,Est. Visits,Backlinks"

    files = {
        "KleanGutter_GSC_Export_[09112026].csv.zip.zip": ("search_console", "kleangutter.com"),
        "MasterShield_GSC_Export_[x].csv.zip.zip": ("search_console", "mastershield.com"),
        "MicroMeshGutterGuards_GSC_Export_[x].csv.zip.zip": ("search_console", "micromeshgutterguards.com"),
        "kleangutter.com-AI-Features-2026-09-03.zip": ("ai_overview", "kleangutter.com"),
        "Kleangutter-Performance-on-Search-2026-09-04 csv.csv": ("ga4_event", "kleangutter.com"),
        "Mastershield - calls export from 2026-08-28 to 2026-09-04.csv": ("call_tracking", "mastershield.com"),
        "MicromeshGG  calls export from 2026-08-28 to 2026-09-04.csv": ("call_tracking", "micromeshgutterguards.com"),
        "Leads_Summary_Week_08-28-2026_to_09-04-2026.txt": ("lead_summary", "all"),
        "MasterShield.com_KBT.csv (3).csv": ("keyword_estimate", "mastershield.com"),
        "LeafFilter.com_Backlinks.csv (4).csv": ("backlink", "leaffilter.com"),
        "Top Pages kleangutter.com.csv": ("top_page", "kleangutter.com"),
        "Top pages ubersuggest_bobvila.com.csv": ("top_page", "bobvila.com"),
        "ubersuggest_gutterhelmet.com_(selected).csv": ("top_page", "gutterhelmet.com"),
        "GutterGuardsAmerica.com_KBT.csv (2).csv": ("top_page", "gutterguardsamerica.com"),
        "kleangutter.com_Traffic_Overview.pdf (3).md": ("domain_report", "kleangutter.com"),
        "traffic-overview_homecraftgutterprotection-com_2026-09-03.md": ("domain_report", "homecraftgutterprotection.com"),
    }
    for filename, (expected_type, expected_domain) in files.items():
        p = tmp_path / filename
        header = kbt_like if expected_type == "top_page" else kbt_header
        p.write_text(header + "\n" if filename.endswith(".csv") else "", encoding="utf-8")
        st, dom, brand = classify(Path(p))
        assert st.split(":", 1)[0] == expected_type, filename
        assert dom == expected_domain, filename


# ------------------------------------------------------------------- parsers

def test_parse_duration_seconds():
    assert parse_duration_seconds("00:03:40") == 220
    assert parse_duration_seconds("03:40") == 220
    assert parse_duration_seconds("45") == 45
    assert parse_duration_seconds("-") is None


def test_parse_leads_recognizes_each_brand(tmp_path):
    p = tmp_path / "Leads.txt"
    p.write_text(LEADS_TXT, encoding="utf-8")
    meta, rows = parse_leads(p)
    by_domain = {r["domain"]: r for r in rows}
    assert by_domain["mastershield.com"]["form_fills"] == 21
    assert by_domain["kleangutter.com"]["form_fills"] == 2
    assert by_domain["kleangutter.com"]["vapi_calls"] == 0
    assert meta["period_to"] == datetime(2026, 9, 4, tzinfo=timezone.utc)


def test_parse_top_pages(tmp_path):
    p = tmp_path / "Top Pages kleangutter.com.csv"
    p.write_text(TOP_PAGES_CSV, encoding="utf-8")
    rows = parse_top_pages(p)
    assert len(rows) == 2
    assert rows[0]["est_visits"] == 24
    assert rows[1]["backlinks"] == 159


# ------------------------------------------------------------------- full import

def test_import_external_folder_populates_tables_and_is_idempotent(client, admin_user, db_session, external_dir):
    from app.models import external as m

    results = import_external_folder(external_dir, db_session)
    by_name = {r["filename"]: r for r in results}
    assert all(r["status"] == "imported" for r in results), [r for r in results if r["status"] != "imported"]

    exports = db_session.query(m.ExternalExport).all()
    assert len(exports) == 10
    assert len(db_session.query(m.SearchConsoleDim).all()) == 5
    assert len(db_session.query(m.SearchConsoleDaily).all()) == 2
    assert len(db_session.query(m.AIOverviewImpressions).all()) == 5
    assert len(db_session.query(m.GA4Event).all()) == 2
    assert len(db_session.query(m.CallTracking).all()) == 1
    assert len(db_session.query(m.LeadSummary).all()) == 2
    assert len(db_session.query(m.KeywordEstimate).all()) == 2
    assert len(db_session.query(m.Backlink).all()) == 1
    assert len(db_session.query(m.TopPage).all()) == 2
    assert len(db_session.query(m.DomainReport).all()) == 2
    da = (db_session.query(m.DomainMetric)
          .filter(m.DomainMetric.metric == "domain_authority").first())
    assert da is not None and int(da.value) == 41

    sc = db_session.query(m.SearchConsoleDim).first()
    assert sc.domain == "kleangutter.com"
    assert sc.dim_type == "query"
    assert sc.key == "gutter guard cost"
    assert sc.position == 3.1

    kt = db_session.query(m.KeywordEstimate).first()
    assert kt.domain == "mastershield.com"
    assert kt.keyword == "klean gutter"

    # idempotency: same folder, second pass -> everything skipped, counts unchanged
    results2 = import_external_folder(external_dir, db_session)
    assert all(r["status"] == "skipped" for r in results2)
    assert len(db_session.query(m.SearchConsoleDim).all()) == 5


def test_import_per_file_error_does_not_block_folder(client, admin_user, db_session, external_dir, tmp_path):
    bad = tmp_path / "not-a-valid-file.xyz"
    bad.write_text("garbage", encoding="utf-8")
    external_dir.joinpath("bogus_export.xyz").write_text("garbage", encoding="utf-8")
    results = import_external_folder(external_dir, db_session)
    bogus = [r for r in results if r["filename"] == "bogus_export.xyz"]
    assert bogus and bogus[0]["status"] == "error"
    good = [r for r in results if r["status"] == "imported"]
    assert len(good) == 10


def test_market_context_builds_for_brand(client, admin_user, db_session, external_dir):
    import_external_folder(external_dir, db_session)
    context, provenance = build_market_context(db_session, "kleangutter")
    assert "kleangutter.com" in context
    assert "gutter guard cost" in context
    assert "Leads (week)" in context
    assert provenance[0]["doc_number"] == "MARKET"


# ------------------------------------------------------------------- API

def login_admin(client):
    from tests.conftest import login

    return login(client, "testadmin", "adminpass")


def test_external_api_requires_admin(client, test_user, external_dir, monkeypatch):
    from tests.conftest import login

    login(client, "testwriter", "secret123")
    assert client.get("/api/ingest/external/status").status_code == 403
    assert client.post("/api/ingest/external").status_code == 403


def test_external_status_and_import(client, admin_user, external_dir, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "external_data_path", str(external_dir))
    login_admin(client)

    status = client.get("/api/ingest/external/status")
    assert status.status_code == 200
    body = status.json()
    assert body["totals"]["files"] == 10
    assert body["totals"]["imported"] == 0
    assert all(f["status"] == "new" for f in body["files"])

    imported = client.post("/api/ingest/external")
    assert imported.status_code == 200
    imp = imported.json()
    assert imp["imported"] == 10
    assert imp["skipped"] == 0
    assert imp["errors"] == 0

    again = client.post("/api/ingest/external")
    assert again.json()["skipped"] == 10

    status2 = client.get("/api/ingest/external/status")
    assert status2.json()["totals"]["imported"] == 10


# ------------------------------------------------------------------- upload API

def _upload_path(tmp_path):
    return str(tmp_path / "uploads")


def _upload_files(client, names_contents, upload_dir):
    files = [("files", (name, content, "application/octet-stream"))
             for name, content in names_contents]
    return client.post("/api/ingest/external/upload", files=files)


def test_upload_requires_auth(client, admin_user, tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "external_upload_path", _upload_path(tmp_path))
    r = client.post("/api/ingest/external/upload", files=[("files", ("x.csv", b"x", "text/plain"))])
    assert r.status_code == 401


def test_writer_can_upload_and_imports(client, test_user, db_session, tmp_path, monkeypatch):
    from app.config import get_settings
    from app.models import external as m

    upload_dir = _upload_path(tmp_path)
    monkeypatch.setattr(get_settings(), "external_upload_path", upload_dir)
    from tests.conftest import login
    login(client, "testwriter", "secret123")

    r = _upload_files(client, [
        ("KleanGutter_GSC_Export_[09112026].csv.zip.zip", make_gsc_zip()),
        ("Leads_Summary_Week_08-28-2026_to_09-04-2026.txt", LEADS_TXT.encode()),
    ], upload_dir)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["imported"] == 2
    assert body["skipped"] == 0
    assert body["errors"] == 0
    assert {f["filename"] for f in body["files"]} == {
        "KleanGutter_GSC_Export_[09112026].csv.zip.zip",
        "Leads_Summary_Week_08-28-2026_to_09-04-2026.txt",
    }

    assert db_session.query(m.ExternalExport).count() == 2
    assert db_session.query(m.SearchConsoleDaily).count() == 2
    assert db_session.query(m.LeadSummary).count() == 2

    # same content again -> skipped, row counts unchanged
    r2 = _upload_files(client, [
        ("KleanGutter_GSC_Export_[09112026].csv.zip.zip", make_gsc_zip()),
    ], upload_dir)
    body2 = r2.json()
    assert body2["imported"] == 0
    assert body2["skipped"] == 1
    assert db_session.query(m.SearchConsoleDaily).count() == 2


def test_upload_status_shows_uploaded_files(client, admin_user, tmp_path, monkeypatch):
    from app.config import get_settings

    upload_dir = _upload_path(tmp_path)
    monkeypatch.setattr(get_settings(), "external_upload_path", upload_dir)
    login_admin(client)

    _upload_files(client, [
        ("KleanGutter_GSC_Export_[09112026].csv.zip.zip", make_gsc_zip()),
    ], upload_dir)

    r = client.get("/api/ingest/external/status")
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["files"] == 1
    assert body["totals"]["imported"] == 1


def test_upload_sanitizes_path_traversal(client, test_user, tmp_path, monkeypatch):
    from app.config import get_settings

    upload_dir = _upload_path(tmp_path)
    monkeypatch.setattr(get_settings(), "external_upload_path", upload_dir)
    from tests.conftest import login
    login(client, "testwriter", "secret123")

    r = client.post("/api/ingest/external/upload", files=[
        ("files", ("../../Leads_Summary_Week_08-28-2026_to_09-04-2026.txt", LEADS_TXT.encode(), "text/plain"))])
    assert r.status_code == 200, r.text
    assert r.json()["imported"] == 1
    assert (tmp_path / "uploads" / "Leads_Summary_Week_08-28-2026_to_09-04-2026.txt").is_file()
    assert not (tmp_path / "Leads_Summary_Week_08-28-2026_to_09-04-2026.txt").exists()


def test_upload_rejects_oversized_file(client, test_user, tmp_path, monkeypatch):
    from app.config import get_settings
    import app.routers.ingest as ingest_router

    monkeypatch.setattr(get_settings(), "external_upload_path", _upload_path(tmp_path))
    monkeypatch.setattr(ingest_router, "MAX_UPLOAD_BYTES", 16)
    from tests.conftest import login
    login(client, "testwriter", "secret123")

    big = b"x" * 64
    r = client.post("/api/ingest/external/upload", files=[
        ("files", ("huge.csv", big, "text/plain"))])
    assert r.status_code == 413


# ------------------------------------------------------------------- delete API

def _delete_files(client, filenames):
    return client.request("DELETE", "/api/ingest/external/delete",
                          json={"filenames": filenames})


def test_delete_requires_auth(client, admin_user, tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "external_upload_path", _upload_path(tmp_path))
    r = _delete_files(client, ["x.csv"])
    assert r.status_code == 401


def test_writer_can_delete_uploaded_files(client, test_user, db_session, tmp_path, monkeypatch):
    from app.config import get_settings
    from app.models import external as m

    upload_dir = _upload_path(tmp_path)
    monkeypatch.setattr(get_settings(), "external_upload_path", upload_dir)
    from tests.conftest import login
    login(client, "testwriter", "secret123")

    _upload_files(client, [
        ("KleanGutter_GSC_Export_[09112026].csv.zip.zip", make_gsc_zip()),
        ("Leads_Summary_Week_08-28-2026_to_09-04-2026.txt", LEADS_TXT.encode()),
    ], upload_dir)
    assert db_session.query(m.ExternalExport).count() == 2
    assert db_session.query(m.SearchConsoleDaily).count() == 2

    r = _delete_files(client, ["KleanGutter_GSC_Export_[09112026].csv.zip.zip"])
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["deleted"] == 1
    assert body["baked"] == 0
    assert body["not_found"] == 0
    assert body["files"][0]["status"] == "deleted"
    assert not (tmp_path / "uploads" / "KleanGutter_GSC_Export_[09112026].csv.zip.zip").exists()

    # detail rows cascade-gone with the export
    assert db_session.query(m.ExternalExport).count() == 1
    assert db_session.query(m.SearchConsoleDaily).count() == 0
    assert db_session.query(m.SearchConsoleDim).count() == 0
    assert db_session.query(m.LeadSummary).count() == 2


def test_delete_reports_baked_file(client, admin_user, external_dir, tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "external_data_path", str(external_dir))
    monkeypatch.setattr(get_settings(), "external_upload_path", _upload_path(tmp_path))
    login_admin(client)

    r = _delete_files(client, ["KleanGutter_GSC_Export_[09112026].csv.zip.zip"])
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["deleted"] == 0
    assert body["baked"] == 1
    assert body["files"][0]["status"] == "baked"
    # baked files are never touched
    assert (external_dir / "KleanGutter_GSC_Export_[09112026].csv.zip.zip").exists()


def test_delete_reports_not_found(client, test_user, tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "external_upload_path", _upload_path(tmp_path))
    from tests.conftest import login
    login(client, "testwriter", "secret123")

    r = _delete_files(client, ["nope.csv"])
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["not_found"] == 1
    assert body["files"][0]["status"] == "not_found"


def test_delete_status_flags_deletable_uploads(client, admin_user, external_dir, tmp_path, monkeypatch):
    from app.config import get_settings

    upload_dir = _upload_path(tmp_path)
    monkeypatch.setattr(get_settings(), "external_data_path", str(external_dir))
    monkeypatch.setattr(get_settings(), "external_upload_path", upload_dir)
    login_admin(client)

    # baked-only file -> not deletable
    status = client.get("/api/ingest/external/status").json()
    by_name = {f["filename"]: f for f in status["files"]}
    assert by_name["KleanGutter_GSC_Export_[09112026].csv.zip.zip"]["deletable"] is False

    # uploaded file -> deletable
    _upload_files(client, [
        ("Leads_Summary_Week_08-28-2026_to_09-04-2026.txt", LEADS_TXT.encode()),
    ], upload_dir)
    status2 = client.get("/api/ingest/external/status").json()
    by_name2 = {f["filename"]: f for f in status2["files"]}
    assert by_name2["Leads_Summary_Week_08-28-2026_to_09-04-2026.txt"]["deletable"] is True