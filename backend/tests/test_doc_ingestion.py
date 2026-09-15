import pytest
from app.services.doc_ingestion import (
    extract_doc_number,
    extract_series,
    extract_doc_type,
    extract_version,
    extract_references,
    extract_title,
    ingest_all_docs,
)
from app.config import get_settings


@pytest.mark.parametrize("filename,expected", [
    ("Doc 100_ Master Content Doctrine.md", "100"),
    ("Doc 316-MS_ Writer Agent Instructions.md", "316-MS"),
    ("Doc 361-KG_ Knowledge Pack.md", "361-KG"),
])
def test_extract_doc_number(filename, expected):
    assert extract_doc_number(filename) == expected


@pytest.mark.parametrize("doc_number,expected", [
    ("100", "100"), ("230", "200"), ("316-MS", "300"), ("430", "400"), ("900", "900"),
])
def test_extract_series(doc_number, expected):
    assert extract_series(doc_number) == expected


@pytest.mark.parametrize("title,filename,expected", [
    ("Routing Agent", "Doc 306_ Routing Agent.md", "agent"),
    ("Writer Playbook", "Doc 170_ Writer Playbook.md", "playbook"),
    ("MasterShield Brand Module", "Doc 130.md", "brand_module"),
    ("Constraint System", "Doc 110.md", "system"),
    ("Keyword Selection SOP", "Doc 151.md", "sop"),
    ("Something Else", "Doc 105.md", "doctrine"),
])
def test_extract_doc_type(title, filename, expected):
    assert extract_doc_type(title, filename) == expected


def test_extract_version():
    assert extract_version("**Version:** 2.7") == "2.7"
    assert extract_version("Version: 13.4") == "13.4"
    assert extract_version("no version here") is None


def test_extract_references_dedupes():
    content = "Per Doc 100 and Doc 122; see Doc 100 again. Also Doc 316-MS."
    refs = set(extract_references(content))
    assert refs == {"100", "122", "316-MS"}


def test_extract_title_prefers_h1():
    content = "junk\n# Real Title\nmore"
    assert extract_title(content, "Doc 100_ Fallback.md") == "Real Title"


def test_extract_title_falls_back_to_filename():
    assert extract_title("no heading", "Doc 122_ Retrieval Chunking.md") == "Retrieval Chunking"


def test_ingest_all_docs_end_to_end(db_session, tmp_path):
    (tmp_path / "Doc 500_ Test Doc.md").write_text(
        "# Doc 500: Test Doc\n\nVersion: 1.2\n\n## Alpha\n\nAlpha body text.\n",
        encoding="utf-8",
    )
    (tmp_path / "Doc 500_ Test Doc.md:Zone.Identifier").write_text("junk", encoding="utf-8")
    (tmp_path / ".hidden.md").write_text("skip", encoding="utf-8")

    settings = get_settings()
    original = settings.doctrine_path
    settings.doctrine_path = str(tmp_path)
    try:
        stats = ingest_all_docs(db_session)
    finally:
        settings.doctrine_path = original

    assert stats["created"] == 1
    assert stats["errors"] == []

    from app.models.document import Document, DocReference
    from app.models.chunk import DocChunk

    doc = db_session.query(Document).one()
    assert doc.doc_number == "500"
    assert doc.version == "1.2"
    assert doc.series == "500" or doc.series.startswith("5")
    # Chunks were created even without embeddings configured.
    chunks = db_session.query(DocChunk).filter(DocChunk.document_id == doc.id).all()
    assert len(chunks) >= 1
    assert all(c.embedding is None for c in chunks)

    # Self-reference to Doc 500 was recorded.
    ref = db_session.query(DocReference).filter_by(source_doc_id=doc.id).first()
    assert ref is not None


def test_ingest_skips_unchanged_files(db_session, tmp_path):
    f = tmp_path / "Doc 501_ Stable.md"
    f.write_text("# Doc 501: Stable\n\nBody.\n", encoding="utf-8")

    settings = get_settings()
    original = settings.doctrine_path
    settings.doctrine_path = str(tmp_path)
    try:
        first = ingest_all_docs(db_session)
        second = ingest_all_docs(db_session)
    finally:
        settings.doctrine_path = original

    assert first["created"] == 1
    assert second["created"] == 0
    assert second["skipped"] == 1


def test_ingest_backfills_missing_embeddings(db_session, tmp_path, monkeypatch):
    from app.models.document import Document
    from app.models.chunk import DocChunk

    f = tmp_path / "Doc 502_ Needs Embed.md"
    f.write_text("# Doc 502: Needs Embed\n\nBody.\n", encoding="utf-8")

    settings = get_settings()
    original = settings.doctrine_path
    settings.doctrine_path = str(tmp_path)
    settings.embedding_provider = "none"
    try:
        ingest_all_docs(db_session)
    finally:
        settings.doctrine_path = original

    doc = db_session.query(Document).one()
    chunks = db_session.query(DocChunk).filter(DocChunk.document_id == doc.id).all()
    assert len(chunks) >= 1
    assert all(c.embedding is None for c in chunks)

    def fake_embed(texts, input_type="document"):
        return [[0.5] * settings.embedding_dimensions for _ in texts]

    monkeypatch.setattr("app.services.doc_ingestion.embed_texts", fake_embed)
    settings.embedding_provider = "ollama"
    settings.embedding_dimensions = 768
    try:
        settings.doctrine_path = str(tmp_path)
        stats = ingest_all_docs(db_session)
    finally:
        settings.embedding_provider = "none"

    assert stats["embedding_failures"] == 0
    chunks = db_session.query(DocChunk).filter(DocChunk.document_id == doc.id).all()
    assert len(chunks) >= 1
    assert all(c.embedding is not None for c in chunks)


def test_ingest_missing_path_raises(db_session, tmp_path):
    settings = get_settings()
    original = settings.doctrine_path
    settings.doctrine_path = str(tmp_path / "does-not-exist")
    try:
        with pytest.raises(FileNotFoundError):
            ingest_all_docs(db_session)
    finally:
        settings.doctrine_path = original
