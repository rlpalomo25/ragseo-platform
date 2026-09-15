import pytest

from tests.conftest import login


def test_stats_requires_auth(client):
    assert client.get("/api/stats").status_code == 401


def test_stats_aggregates(client, db_session, doctrine_corpus, test_user):
    from app.models.chunk import DocChunk
    from app.models.document import Document
    from app.services.orchestrator import create_job

    login(client, "testwriter", "secret123")

    doc = db_session.query(Document).order_by(Document.doc_number).first()
    for i in range(3):
        db_session.add(DocChunk(
            document_id=doc.id, chunk_index=i, heading_path="H", content="x" * 20,
            token_count=5, content_hash=f"plain{i}", embedding=None,
        ))
    for i in range(2):
        db_session.add(DocChunk(
            document_id=doc.id, chunk_index=10 + i, heading_path="H", content="y" * 20,
            token_count=5, content_hash=f"embed{i}", embedding=[0.1] * 768,
        ))
    db_session.commit()

    job = create_job(db_session, created_by=test_user.id, request="Write a gutter guard comparison page")
    job.revision_count = 2
    db_session.commit()

    body = client.get("/api/stats").json()

    assert body["documents"]["total"] == 9  # doctrine_corpus count
    assert body["documents"]["active"] == 9
    assert sum(body["documents"]["by_doc_type"].values()) == 9
    assert body["documents"]["by_series"]["100"] == 4
    assert body["documents"]["by_series"]["300"] == 5

    assert body["chunks"]["total"] == 5
    assert body["chunks"]["embedded"] == 2
    assert body["chunks"]["coverage"] == 0.4

    assert body["jobs"]["total"] == 1
    assert body["jobs"]["by_status"]["running"] == 1
    assert body["jobs"]["avg_revisions"] == 2.0
    assert body["jobs"]["with_revisions"] == 1
    assert body["jobs"]["created_last_7d"] == 1
    assert body["jobs"]["created_last_30d"] == 1
    assert body["jobs"]["failed_stages"] == 0


def test_stats_counts_failed_stages(client, db_session, doctrine_corpus, test_user):
    from app.models.job import JobStage
    from app.services.orchestrator import create_job

    login(client, "testwriter", "secret123")
    job = create_job(db_session, created_by=test_user.id, request="Write a service page")
    stage = db_session.query(JobStage).filter(JobStage.job_id == job.id).first()
    stage.status = "failed"
    db_session.commit()

    body = client.get("/api/stats").json()
    assert body["jobs"]["failed_stages"] == 1