"""Hybrid retrieval over the doctrine chunk store (keyword path; embeddings off).

Regression focus: ``doc_numbers=[...]`` filters must not raise on the ``IN``
bind (needs ``expanding=True``) and must exclude non-listed docs.
"""
import pytest

from tests.conftest import seed_doc
from app.models.chunk import DocChunk


@pytest.fixture()
def retrieval_corpus(db_session):
    doc100 = seed_doc(db_session, "100", "Master Content Doctrine",
                      "# Master Content Doctrine\n\nCore content rules live here.")
    doc316 = seed_doc(db_session, "316", "Writer Agent Instructions",
                      "# Writer Instructions\n\nFollow the block order and structure.")
    doc130 = seed_doc(db_session, "130", "MasterShield Brand Module",
                      "# Brand Module\n\nVoice: The Guardian Engineer posture.")
    for idx, (doc, text) in enumerate([(doc100, "content rules for page structure"),
                                       (doc316, "writer must follow the content order"),
                                       (doc130, "brand voice content posture text")]):
        db_session.add(DocChunk(
            document_id=doc.id, chunk_index=idx, heading_path="",
            content=text, token_count=len(text.split()),
            content_hash=f"h{idx}", embedding=None))
    db_session.commit()
    return db_session


def test_retrieve_without_doc_numbers_returns_mixed_docs(retrieval_corpus):
    from app.services.retrieval import retrieve

    results = retrieve(retrieval_corpus, "content structure order", top_k=10)
    assert results
    doc_numbers = {r.doc_number for r in results}
    assert "100" in doc_numbers
    assert "130" in doc_numbers


def test_retrieve_with_doc_numbers_filters_docs(retrieval_corpus):
    from app.services.retrieval import retrieve

    results = retrieve(retrieval_corpus, "content structure order", top_k=10,
                       doc_numbers=["100", "316"])
    assert results
    doc_numbers = {r.doc_number for r in results}
    assert doc_numbers <= {"100", "316"}
    assert "130" not in doc_numbers


def test_retrieve_with_single_doc_number(retrieval_corpus):
    from app.services.retrieval import retrieve

    results = retrieve(retrieval_corpus, "content structure order", top_k=10,
                       doc_numbers=["316"])
    assert results
    assert {r.doc_number for r in results} == {"316"}