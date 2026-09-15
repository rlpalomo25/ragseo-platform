from pathlib import Path

import pytest

from app.services.doc_ingestion import file_hash


@pytest.fixture()
def ingest_dir(tmp_path, monkeypatch):
    """A doctoned folder on disk plus a matching DB doc, with doctrine_path pointed at it."""
    from app.config import get_settings

    d1 = tmp_path / "Doc 100_ Test D1.md"
    d1.write_text("# Test D1\n\nBody of the first doc.\n", encoding="utf-8")
    d2 = tmp_path / "Doc 200_ Test D2.md"
    d2.write_text("# Test D2\n\nBody of the second doc.\n", encoding="utf-8")

    get_settings().doctrine_path = str(tmp_path)
    return tmp_path


def login_admin(client):
    from tests.conftest import login

    return login(client, "testadmin", "adminpass")


def test_ingest_status_requires_admin(client, test_user, ingest_dir):
    from tests.conftest import login

    login(client, "testwriter", "secret123")
    assert client.get("/api/ingest/status").status_code == 403
    assert client.post("/api/ingest/reingest").status_code == 403


def test_ingest_status_reports_new_changed_unchanged(client, admin_user, db_session, ingest_dir):
    from app.models.chunk import DocChunk
    from tests.conftest import seed_doc

    d1_path = ingest_dir / "Doc 100_ Test D1.md"

    unchanged = seed_doc(db_session, "100", "Test D1", d1_path.read_text())
    unchanged.file_hash = file_hash(str(d1_path))
    db_session.add(unchanged)
    db_session.flush()

    changed = seed_doc(db_session, "200", "Old Title", "Old body data")
    changed.filename = "Doc 200_ Test D2.md"
    changed.file_hash = "stale-hash"
    db_session.add(changed)
    db_session.flush()

    db_session.add(DocChunk(document_id=unchanged.id, chunk_index=0, heading_path="",
                           content="Body of the first doc.", token_count=5, content_hash="h",
                           embedding=None))
    db_session.add(DocChunk(document_id=unchanged.id, chunk_index=1, heading_path="",
                           content="more", token_count=2, content_hash="h2",
                           embedding=[0.1] * 768))
    db_session.commit()

    login_admin(client)
    body = client.get("/api/ingest/status").json()

    by_name = {f["filename"]: f for f in body["files"]}
    assert by_name["Doc 100_ Test D1.md"]["status"] == "unchanged"
    assert by_name["Doc 100_ Test D1.md"]["chunk_count"] == 2
    assert by_name["Doc 100_ Test D1.md"]["embedded_chunks"] == 1
    assert by_name["Doc 200_ Test D2.md"]["status"] == "changed"

    totals = body["totals"]
    assert totals["files"] == 2
    assert totals["new"] == 0
    assert totals["changed"] == 1
    assert totals["unchanged"] == 1
    assert totals["chunks"] == 2
    assert totals["embedded"] == 1
    assert totals["embedding_coverage"] == 0.5


def test_ingest_reingest_then_status(client, admin_user, db_session, ingest_dir):
    from tests.conftest import login

    login(client, "testadmin", "adminpass")
    result = client.post("/api/ingest/reingest").json()
    assert result["message"] == "Reingestion complete"
    assert result["stats"]["created"] == 2
    assert result["stats"]["chunks"] >= 2
    assert result["stats"]["embedding_failures"] == 0

    body = client.get("/api/ingest/status").json()
    assert body["totals"]["new"] == 0
    assert body["totals"]["unchanged"] == 2