import re
import hashlib
import logging
from pathlib import Path
from sqlalchemy.orm import Session as DBSession
from app.models.document import Document, DocReference
from app.models.chunk import DocChunk
from app.config import get_settings
from app.services.chunking import chunk_document, chunk_content_hash
from app.services.embeddings import embed_texts, EmbeddingError

logger = logging.getLogger(__name__)
settings = get_settings()

DOC_PATTERN = re.compile(r"Doc\s+(\d+(?:-\w+)?)\s*[_:]\s*(.+?)(?:\.md)?$", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"[Vv]ersion[*\s:]+?([\d][\d.]*)")
SERIES_MAP = {
    "1": "100", "2": "200", "3": "300", "4": "400", "9": "900",
}


def extract_doc_number(filename: str) -> str:
    match = DOC_PATTERN.search(filename)
    if match:
        return match.group(1)
    return filename.split("_")[0].split(".")[0]


def extract_series(doc_number: str) -> str:
    first_digit = re.match(r"(\d)", doc_number)
    if first_digit:
        prefix = first_digit.group(1)
        return SERIES_MAP.get(prefix, prefix + "00")
    return "misc"


def extract_doc_type(title: str, filename: str) -> str:
    lower = (title + " " + filename).lower()
    if "agent" in lower:
        return "agent"
    if any(x in lower for x in ["playbook", "writer"]):
        return "playbook"
    if "brand" in lower and "module" in lower:
        return "brand_module"
    if "schema" in lower:
        return "schema"
    if "system" in lower or "protocol" in lower:
        return "system"
    if "sop" in lower:
        return "sop"
    return "doctrine"


def extract_version(content: str) -> str | None:
    match = VERSION_PATTERN.search(content[:2000])
    return match.group(1) if match else None


def extract_references(content: str) -> list[str]:
    refs = set()
    for match in re.finditer(r"Doc\s+(\d+(?:-\w+)?)", content):
        refs.add(match.group(1))
    return list(refs)


def extract_title(content: str, filename: str) -> str:
    for line in content.split("\n")[:20]:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    name = filename.replace(".md", "").replace(":Zone.Identifier", "")
    match = DOC_PATTERN.search(name)
    if match:
        return match.group(2).strip()
    return name


def file_hash(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _rechunk_document(db: DBSession, doc: Document, stats: dict) -> None:
    """Rebuild chunks (and embeddings when configured) for one document."""
    db.query(DocChunk).filter(DocChunk.document_id == doc.id).delete()

    chunks = chunk_document(doc.content, doc.doc_number, doc.title)
    if not chunks:
        return

    vectors = None
    if settings.embeddings_enabled:
        try:
            vectors = embed_texts([c["content"] for c in chunks], input_type="document")
        except EmbeddingError as e:
            logger.warning("Embedding failed for Doc %s (storing without vectors): %s", doc.doc_number, e)
            stats["embedding_failures"] += 1

    for chunk_data in chunks:
        db.add(DocChunk(
            document_id=doc.id,
            chunk_index=chunk_data["chunk_index"],
            heading_path=chunk_data["heading_path"],
            content=chunk_data["content"],
            token_count=len(chunk_data["content"]) // 4,
            content_hash=chunk_content_hash(chunk_data["content"]),
            embedding=vectors[chunk_data["chunk_index"]] if vectors else None,
        ))
    stats["chunks"] += len(chunks)


def ingest_all_docs(db: DBSession) -> dict:
    doctrine_path = Path(settings.doctrine_path)
    if not doctrine_path.exists():
        raise FileNotFoundError(
            f"Doctrine path not found: {doctrine_path}. Set DOCTRINE_PATH to the folder "
            "containing the RAGSEO markdown library."
        )

    md_files = sorted(doctrine_path.glob("*.md"))
    stats = {"created": 0, "updated": 0, "skipped": 0, "chunks": 0, "embedding_failures": 0, "errors": []}

    for filepath in md_files:
        if filepath.name.startswith(".") or ":Zone.Identifier" in filepath.name:
            continue
        try:
            content = filepath.read_text(encoding="utf-8")
            fhash = file_hash(str(filepath))
            filename = filepath.name
            doc_number = extract_doc_number(filename)
            title = extract_title(content, filename)
            series = extract_series(doc_number)
            version = extract_version(content)
            doc_type = extract_doc_type(title, filename)
            word_count = len(content.split())
            last_updated = None

            existing = db.query(Document).filter(Document.filename == filename).first()
            if existing and existing.file_hash == fhash:
                has_chunks = db.query(DocChunk).filter(DocChunk.document_id == existing.id).first() is not None
                needs_backfill = False
                if settings.embeddings_enabled:
                    if not has_chunks:
                        # File unchanged but never chunked/embedded — backfill.
                        needs_backfill = True
                    else:
                        has_vectors = (
                            db.query(DocChunk)
                            .filter(DocChunk.document_id == existing.id, DocChunk.embedding.isnot(None))
                            .first()
                            is not None
                        )
                        # Chunked before embeddings were enabled (or vectors wiped
                        # by a dimension migration) — re-embed from scratch.
                        needs_backfill = not has_vectors
                if not needs_backfill:
                    stats["skipped"] += 1
                    continue
                _rechunk_document(db, existing, stats)
                db.commit()
                stats["skipped"] += 1
                continue

            if existing:
                existing.content = content
                existing.title = title
                existing.doc_number = doc_number
                existing.series = series
                existing.version = version
                existing.doc_type = doc_type
                existing.word_count = word_count
                existing.file_hash = fhash
                doc = existing
                stats["updated"] += 1
            else:
                doc = Document(
                    doc_number=doc_number,
                    title=title,
                    filename=filename,
                    content=content,
                    version=version,
                    series=series,
                    doc_type=doc_type,
                    word_count=word_count,
                    file_hash=fhash,
                )
                db.add(doc)
                db.flush()
                stats["created"] += 1

            _rechunk_document(db, doc, stats)

        except Exception as e:
            stats["errors"].append(f"{filename}: {str(e)}")

    db.commit()

    all_docs = db.query(Document).all()
    db.query(DocReference).delete()
    for doc in all_docs:
        refs = extract_references(doc.content)
        for ref in refs:
            db.add(DocReference(
                source_doc_id=doc.id,
                target_doc_number=ref,
                reference_type="references",
            ))
    db.commit()

    return stats
