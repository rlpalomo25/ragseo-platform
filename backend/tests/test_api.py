import pytest
from uuid import uuid4

from tests.conftest import login


@pytest.fixture()
def writer_headers(client, test_user):
    login(client, "testwriter", "secret123")
    return {}


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_list_documents_empty(client, writer_headers):
    response = client.get("/api/docs")
    assert response.status_code == 200
    assert response.json() == {"documents": [], "total": 0, "page": 1, "page_size": 50}


def test_list_documents_includes_chunk_coverage(client, writer_headers, db_session):
    from app.models.document import Document
    from app.models.chunk import DocChunk

    doc = Document(
        doc_number="100",
        title="Master Content Doctrine",
        filename="Doc 100_ Master Content Doctrine.md",
        content="The master doctrine of content production.",
        status="active",
    )
    db_session.add(doc)
    db_session.flush()
    db_session.add(DocChunk(document_id=doc.id, chunk_index=0, heading_path="", content="a" * 20,
                            token_count=5, content_hash="h1", embedding=None))
    db_session.add(DocChunk(document_id=doc.id, chunk_index=1, heading_path="", content="b" * 20,
                            token_count=5, content_hash="h2", embedding=[0.1] * 768))
    db_session.commit()

    body = client.get("/api/docs").json()
    assert len(body["documents"]) == 1
    assert body["documents"][0]["chunk_count"] == 2
    assert body["documents"][0]["embedded_chunks"] == 1


def test_document_detail_includes_chunk_coverage(client, writer_headers, db_session):
    from app.models.document import Document
    from app.models.chunk import DocChunk

    doc = Document(
        doc_number="101",
        title="Some Doctrine",
        filename="Doc 101_ Some Doctrine.md",
        content="Content here.",
        status="active",
    )
    db_session.add(doc)
    db_session.flush()
    db_session.add(DocChunk(document_id=doc.id, chunk_index=0, heading_path="", content="c" * 20,
                            token_count=5, content_hash="h", embedding=[0.1] * 768))
    db_session.commit()

    body = client.get(f"/api/docs/{doc.id}").json()
    assert body["chunk_count"] == 1
    assert body["embedded_chunks"] == 1


def test_get_document_rejects_malformed_uuid(client, writer_headers):
    response = client.get("/api/docs/not-a-uuid")
    assert response.status_code == 422


def test_get_document_not_found(client, writer_headers):
    response = client.get(f"/api/docs/{uuid4()}")
    assert response.status_code == 404


def test_agent_run_unknown_type_rejected(client, writer_headers):
    response = client.post("/api/agents/run", json={"agent_type": "nope", "input_data": {}})
    assert response.status_code == 400


def test_agents_endpoint_requires_writer_role(client, test_user):
    assert client.get("/api/agents").status_code == 401


def test_search_falls_back_to_keyword_without_chunks(client, writer_headers, db_session):
    from app.models.document import Document

    db_session.add(Document(
        doc_number="100",
        title="Master Content Doctrine",
        filename="Doc 100_ Master Content Doctrine.md",
        content="The master doctrine of content production.",
        status="active",
    ))
    db_session.commit()

    response = client.get("/api/docs/search", params={"q": "doctrine"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["documents"][0]["doc_number"] == "100"
