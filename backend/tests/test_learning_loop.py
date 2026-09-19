import uuid
from datetime import UTC, datetime, timedelta

import pytest
from app.models.external import (
    AIOverviewImpressions,
    CallTracking,
    ExternalExport,
    KeywordEstimate,
    SearchConsoleDim,
    TopPage,
)
from app.models.job import AgentJob
from app.models.learning import ContentPerformanceSnapshot, LearningSignal
from app.services.external_ingest import delete_external_export
from app.services.learning_loop import (
    build_learning_context,
    normalize_url,
    register_publication,
    snapshot_publications,
)

DOMAIN = "kleangutter.com"
URL = "https://kleangutter.com/gutter-guards/"


def _export(db, source_type, day):
    stamp = datetime(2026, 9, int(day), 12, 0, 0, tzinfo=UTC)
    row = ExternalExport(
        source_type=source_type,
        domain=DOMAIN,
        brand="kleangutter",
        file_name=f"{source_type}-{day}.csv",
        file_hash=f"{source_type}-w{day}",
        period_from=stamp - timedelta(days=6),
        period_to=stamp,
        exported_at=stamp,
        row_count=1,
        imported_at=stamp,
        status="imported",
    )
    db.add(row)
    db.flush()
    return row


def _seed_batch(db, day, *, position=2.1, impressions=500, clicks=20, ctr=4.0, ai=88, calls=1, visited=1200):
    """One full weekly cycle of external rows for the publication URL."""
    sc = _export(db, "search_console", day)
    db.add_all(
        [
            SearchConsoleDim(
                export_id=sc.id,
                domain=DOMAIN,
                dim_type="page",
                key=URL,
                clicks=clicks,
                impressions=impressions,
                ctr=ctr,
                position=position,
            ),
            SearchConsoleDim(
                export_id=sc.id,
                domain=DOMAIN,
                dim_type="query",
                key="klean gutter guards",
                clicks=clicks,
                impressions=impressions,
                ctr=ctr,
                position=position,
            ),
        ]
    )
    ai_row = _export(db, "ai_overview", day)
    db.add(
        AIOverviewImpressions(
            export_id=ai_row.id,
            domain=DOMAIN,
            dim_type="pages",
            key=URL,
            day=ai_row.period_to.date(),
            impressions=ai,
        )
    )
    kw = _export(db, "keyword_estimate", day)
    db.add(
        KeywordEstimate(
            export_id=kw.id,
            domain=DOMAIN,
            keyword="klean gutter guards",
            volume=1200,
            position=position,
            est_visits=visited,
            ranking_url=URL,
        )
    )
    tp = _export(db, "top_page", day)
    db.add(TopPage(export_id=tp.id, domain=DOMAIN, url=URL, title="Gutter Guards", est_visits=visited))
    call = _export(db, "call_tracking", day)
    if calls:
        db.add(
            CallTracking(
                export_id=call.id,
                domain=DOMAIN,
                name="Caller",
                status="answered",
                page="/gutter-guards/",
                last_url=URL,
                call_date=call.period_to.date(),
            )
        )
    db.commit()


def _job(db, user, brand="kleangutter", title="Klean Gutter Guards page"):
    job = AgentJob(
        title=title,
        request="Write a page for clean gutters",
        brand=brand,
        content_type="local",
        status="awaiting_approval",
        created_by=user.id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def test_normalize_url():
    assert normalize_url("https://www.KleanGutter.com/Gutter-Guards/") == "kleangutter.com/gutter-guards"
    assert normalize_url("http://kleangutter.com") == "kleangutter.com"
    assert normalize_url("/gutter-guards/") == "gutter-guards"
    assert normalize_url("https://kleangutter.com/gutter-guards?ref=x#top") == "kleangutter.com/gutter-guards"
    assert normalize_url("") == ""


def test_register_publication_requires_valid_job_and_url(db_session, test_user):
    with pytest.raises(ValueError, match="not found"):
        register_publication(db_session, uuid.uuid4(), URL)
    job = _job(db_session, test_user)
    with pytest.raises(ValueError, match="non-empty URL"):
        register_publication(db_session, job.id, "   ")
    pub = register_publication(db_session, job.id, URL, keyword="klean gutter guards")
    assert pub.status == "active"
    assert pub.publish_url == URL
    assert pub.target_keyword == "klean gutter guards"


def test_snapshot_first_cycle_baseline(db_session, test_user):
    job = _job(db_session, test_user)
    pub = register_publication(db_session, job.id, URL, keyword="klean gutter guards")
    _seed_batch(db_session, "1")  # day 1 = single weekly cycle

    stats = snapshot_publications(db_session)
    assert stats["publications"] == 1
    assert stats["snapshots"] == 1

    snap = db_session.query(ContentPerformanceSnapshot).one()
    # Keyword-level position wins over pages-dim position.
    assert snap.position == 2.1
    assert snap.clicks == 20
    assert snap.impressions == 500
    assert snap.ctr == 4.0
    assert snap.ai_overview_impressions == 88
    assert snap.calls == 1
    assert snap.est_visits == 1200
    assert snap.movement is None
    assert snap.flags == []  # no baseline flags

    context, sources = build_learning_context(db_session, "kleangutter")
    assert "Performance Memory" in context
    assert URL in context
    assert "pos 2.1" in context
    assert sources[0]["doc_number"] == "MEMORY"
    assert pub.id  # publication survived registration


def test_snapshot_second_cycle_movement_and_flags_idempotent(db_session, test_user):
    job = _job(db_session, test_user)
    register_publication(db_session, job.id, URL, keyword="klean gutter guards")
    _seed_batch(db_session, "1", position=2.1, impressions=500, ctr=4.0, ai=88)
    snapshot_publications(db_session)

    # Week 2: ranking and engagement all worsen.
    _seed_batch(db_session, "10", position=8.9, impressions=120, clicks=5, ctr=1.2, ai=0)
    stats = snapshot_publications(db_session)
    assert stats["snapshots"] == 1  # this run created exactly the new (week-2) snapshot
    assert stats["signals"] == 4  # position_drop + ctr_drop + movement + ai_zero

    snaps = db_session.query(ContentPerformanceSnapshot).order_by(ContentPerformanceSnapshot.period_to).all()
    assert len(snaps) == 2
    latest = snaps[-1]
    assert latest.position == 8.9
    assert latest.movement == pytest.approx(6.8)
    assert latest.movement_ctr == pytest.approx(-2.8)
    assert latest.movement_impressions == -380
    assert set(latest.flags) == {"position_drop", "ctr_drop", "movement", "ai_zero"}

    signals = db_session.query(LearningSignal).all()
    assert len(signals) == 4
    assert {s.source for s in signals} == {
        "pub_perf:position_drop",
        "pub_perf:ctr_drop",
        "pub_perf:movement",
        "pub_perf:ai_zero",
    }

    # Idempotency: re-running the same cycle never duplicates a snapshot or signal.
    stats2 = snapshot_publications(db_session)
    assert db_session.query(ContentPerformanceSnapshot).count() == 2
    assert db_session.query(LearningSignal).count() == 4
    assert stats2["signals"] == 0

    context, _ = build_learning_context(db_session, "kleangutter")
    assert "moved 6.8 down" in context
    assert "CTR Δ -2.8pp" in context
    assert "flags: " in context


def test_unmeasurable_flag_when_nothing_matches(db_session, test_user):
    job = _job(db_session, test_user)
    register_publication(db_session, job.id, "https://kleangutter.com/nowhere/")
    _seed_batch(db_session, "1")
    snapshot_publications(db_session)
    snap = db_session.query(ContentPerformanceSnapshot).one()
    assert snap.position is None
    assert snap.impressions == 0
    assert "unmeasurable" in snap.flags


def test_delete_export_removes_its_snapshots(db_session, test_user):
    job = _job(db_session, test_user)
    register_publication(db_session, job.id, URL, keyword="klean gutter guards")
    _seed_batch(db_session, "1")
    snapshot_publications(db_session)
    assert db_session.query(ContentPerformanceSnapshot).count() == 1

    snap = db_session.query(ContentPerformanceSnapshot).first()
    export = db_session.query(ExternalExport).filter(ExternalExport.id == snap.source_export_id).first()
    delete_external_export(db_session, export)
    db_session.commit()
    # Deleting the export must not orphan the snapshots that anchored on it.
    assert db_session.query(ContentPerformanceSnapshot).count() == 0


def test_writer_injects_learning_sources_without_touching_provenance(doctrine_corpus, monkeypatch):
    from app.services.agents import writer as writer_module

    captured = {}

    def fake_call_llm(system_prompt, user_message, max_tokens=4096):
        captured["user_message"] = user_message
        return (
            "===RAGSEO_META===\n"
            '{"title": "T", "meta_title": "MT", "meta_description": "MD", '
            '"content_type": "local", "brand": "kleangutter"}\n'
            "===RAGSEO_CONTENT===\n# T\n\nBody.\n"
        )

    monkeypatch.setattr(writer_module, "call_llm", fake_call_llm)
    fake_sources = [{"doc_number": "MEMORY", "title": "Learning loop", "version": None}]
    monkeypatch.setattr(
        writer_module,
        "build_learning_context",
        lambda db, brand: ("## Performance Memory\n  - https://kleangutter.com/ pos 3.1", fake_sources),
    )

    result = writer_module.run_writer(doctrine_corpus, {"request": "Klean Gutter cleaning page"})
    assert "Performance Memory" in captured["user_message"]
    assert result["learning_sources"] == fake_sources
    # provenance stays an exact set of governing docs — MEMORY is separate.
    stamped = {p["doc_number"] for p in result["provenance"]}
    assert stamped == {"100", "320", "131"}


def test_writer_empty_learning_sources_when_no_data(doctrine_corpus, captured_writer_call):
    from app.services.agents import writer as writer_module

    result = writer_module.run_writer(doctrine_corpus, {"request": "MasterShield comparison page"})
    assert result["learning_sources"] == []
    assert "Performance Memory" not in captured_writer_call["user_message"]


@pytest.fixture()
def captured_writer_call(monkeypatch):
    calls = {}

    def fake_call_llm(system_prompt, user_message, max_tokens=4096):
        calls["user_message"] = user_message
        return (
            "===RAGSEO_META===\n"
            '{"title": "T", "meta_title": "MT", "meta_description": "MD", '
            '"content_type": "comparison", "brand": "mastershield"}\n'
            "===RAGSEO_CONTENT===\n# T\n\nBody.\n"
        )

    from app.services.agents import writer as writer_module

    monkeypatch.setattr(writer_module, "call_llm", fake_call_llm)
    return calls


def test_api_publication_writer_only(client, test_user, db_session):
    from tests.conftest import login

    job = _job(db_session, test_user)

    # Anonymous access denied.
    resp = client.post(f"/api/jobs/{job.id}/publication", json={"url": URL})
    assert resp.status_code == 401

    login(client, "testwriter", "secret123")
    resp = client.post(
        f"/api/jobs/{job.id}/publication",
        json={"url": URL, "target_keyword": "klean gutter guards", "publish_date": "2026-09-01"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["publish_url"] == URL
    assert body["job_id"] == str(job.id)
    assert body["target_keyword"] == "klean gutter guards"


def test_api_flags_admin_only(client, test_user, admin_user, db_session):
    from tests.conftest import login

    login(client, "testwriter", "secret123")
    assert client.get("/api/learning/flags").status_code == 403
    assert client.post("/api/learning/recompute").status_code == 403

    login(client, "testadmin", "adminpass")
    resp = client.get("/api/learning/flags")
    assert resp.status_code == 200
    assert resp.json()["count"] == 0

    recompute = client.post("/api/learning/recompute")
    assert recompute.status_code == 200
    body = recompute.json()
    assert body["publications"] == 0
    assert body["snapshots"] == 0
    assert body["signals"] == 0
