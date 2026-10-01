import hashlib
import logging
import re
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session as DBSession

from app.config import get_settings
from app.models.chunk import DocChunk
from app.models.document import DocReference, Document
from app.services.chunking import chunk_content_hash, chunk_document
from app.services.embeddings import EmbeddingError, embed_texts

logger = logging.getLogger(__name__)
settings = get_settings()

# Anchored at the start so a name like "old Doc 100_Title.md" is rejected by the
# upload validator instead of quietly becoming Doc 100, which mirrors the
# anchored DOC_NAME check the frontend card runs. Every one of the 122 library
# files still matches, so this costs nothing.
DOC_PATTERN = re.compile(r"^Doc\s+(\d+(?:-\w+)?)\s*[_:]\s*(.+?)(?:\.md)?$", re.IGNORECASE)
VERSION_PATTERN = re.compile(r"[Vv]ersion[*\s:]+?([\d][\d.]*)")
SERIES_MAP = {
    "1": "100",
    "2": "200",
    "3": "300",
    "4": "400",
    "9": "900",
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
        db.add(
            DocChunk(
                document_id=doc.id,
                chunk_index=chunk_data["chunk_index"],
                heading_path=chunk_data["heading_path"],
                content=chunk_data["content"],
                token_count=len(chunk_data["content"]) // 4,
                content_hash=chunk_content_hash(chunk_data["content"]),
                embedding=vectors[chunk_data["chunk_index"]] if vectors else None,
            )
        )
    stats["chunks"] += len(chunks)


def doctrine_folders() -> list[Path]:
    """Baked + writable doctrine folders, baked first; nonexistent dirs skipped.

    ``doctrine_path`` is the read-only library baked into the image; uploads land
    in ``doctrine_upload_path``. Both must be scanned as a union: a sweep that
    only looked at the baked folder would mark every uploaded document
    ``missing`` within the hour.
    """
    folders: list[Path] = []
    for folder in dict.fromkeys(
        [
            Path(settings.doctrine_path),
            Path(settings.doctrine_upload_path),
        ]
    ):
        if folder.is_dir():
            folders.append(folder)
    return folders


def scan_doctrine_files() -> list[Path]:
    """Every ingestible ``.md`` across :func:`doctrine_folders`, deduplicated by name.

    ``Document.filename`` is the ingestion key, so two files with the same
    basename cannot coexist. The earlier folder wins — baked first — meaning an
    upload can never shadow a library file. (The upload endpoint also refuses
    those names up front with a 409, so a collision should be unreachable.)
    """
    files: list[Path] = []
    seen: dict[str, Path] = {}
    for folder in doctrine_folders():
        # ``glob("*.md")`` is case-sensitive on Linux, and the upload validator
        # accepts ``.MD`` (a Windows-authored name). Matching the suffix
        # case-insensitively keeps such a file from being ingested and then
        # swept to ``missing`` by the hourly reconcile.
        for filepath in sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".md"):
            if filepath.name.startswith(".") or ":Zone.Identifier" in filepath.name:
                continue
            shadowed = seen.get(filepath.name)
            if shadowed is not None:
                logger.warning(
                    "Ignoring %s in %s: filename already claimed by %s",
                    filepath,
                    folder,
                    shadowed.parent,
                )
                continue
            seen[filepath.name] = filepath
            files.append(filepath)
    return files


def _new_stats(**extra) -> dict:
    return {
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "superseded": 0,
        "chunks": 0,
        "embedding_failures": 0,
        "errors": [],
        **extra,
    }


def _needs_backfill(db: DBSession, doc: Document) -> bool:
    """True when a hash-unchanged document still needs chunks and/or vectors."""
    has_chunks = db.query(DocChunk).filter(DocChunk.document_id == doc.id).first() is not None
    if not has_chunks:
        # File unchanged but never chunked/embedded — backfill.
        return True
    if not settings.embeddings_enabled:
        return False
    has_vectors = (
        db.query(DocChunk).filter(DocChunk.document_id == doc.id, DocChunk.embedding.isnot(None)).first()
        is not None
    )
    # Chunked before embeddings were enabled (or vectors wiped by a dimension
    # migration) — re-embed from scratch.
    return not has_vectors


def _ingest_one(
    db: DBSession,
    filepath: Path,
    *,
    stats: dict,
    by_filename: dict[str, Document],
    by_number: dict[str, Document],
    backfill: bool = False,
) -> str:
    """Ingest one markdown file, returning its outcome.

    Outcomes: ``skipped`` (bytes unchanged), ``backfilled`` (unchanged bytes but
    chunks/vectors were missing), ``updated``, ``created``.

    ``by_filename`` is keyed on every document row, ``by_number`` on active rows
    only. Both are mutated in place so a document ingested earlier in the same
    scan is visible to later files, and both are rebuilt by the caller after a
    supersede. Keeping the caches is what lets this single routine serve the
    full scan, the reconcile sweep and the scoped upload ingest.

    ``backfill`` re-chunks an unchanged file whose vectors are missing. Only a
    full reingest asks for that; the hourly reconcile is a freshness pass and
    must not spend an embedding budget on every document.
    """
    content = filepath.read_text(encoding="utf-8")
    fhash = file_hash(str(filepath))
    filename = filepath.name
    doc_number = extract_doc_number(filename)
    title = extract_title(content, filename)
    series = extract_series(doc_number)
    version = extract_version(content)
    doc_type = extract_doc_type(title, filename)
    word_count = len(content.split())
    now = datetime.now(UTC)

    existing_by_filename = by_filename.get(filename)
    if existing_by_filename is not None and existing_by_filename.file_hash == fhash:
        if backfill and _needs_backfill(db, existing_by_filename):
            _rechunk_document(db, existing_by_filename, stats)
            db.flush()
            return "backfilled"
        return "skipped"

    # Free the doc_number BEFORE the INSERT below: if a different active doc owns
    # this number, supersede it first (and flush) so the new/updated row does not
    # violate uq_documents_doc_number_active. Inserting first would raise
    # IntegrityError inside the per-file try (and, left unrolled-back, poison
    # every later file).
    existing_by_number = by_number.get(doc_number)
    if (
        existing_by_number is not None
        and existing_by_number.status == "active"
        and existing_by_number.filename != filename
    ):
        existing_by_number.status = "superseded"
        existing_by_number.last_updated = now
        stats["superseded"] += 1
        by_number.pop(doc_number, None)
        db.flush()

    if existing_by_filename is not None:
        doc = existing_by_filename
        was_active = doc.status == "active"
        doc.content = content
        doc.title = title
        doc.doc_number = doc_number
        doc.series = series
        doc.version = version
        doc.doc_type = doc_type
        doc.word_count = word_count
        doc.file_hash = fhash
        doc.last_updated = now
        # The file is on disk and now owns its doc_number (the previous owner was
        # superseded above), so a row left `missing`/`superseded` by an earlier
        # sweep has to come back — otherwise a restored upload stays invisible
        # to retrieval forever.
        if not was_active:
            logger.info("Doc %s (%s) restored to active from status '%s'", doc_number, filename, doc.status)
            doc.status = "active"
        by_filename[filename] = doc
        by_number[doc_number] = doc
        outcome = "updated"
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
            last_updated=now,
        )
        db.add(doc)
        db.flush()
        by_filename[filename] = doc
        by_number[doc_number] = doc
        outcome = "created"

    _rechunk_document(db, doc, stats)
    return outcome


def _rebuild_references(db: DBSession, active_only: bool) -> None:
    """Recompute the whole reference graph from document bodies.

    ``active_only`` differs by caller: a reconcile only cares about what agents
    can retrieve, while a full reingest refreshes superseded rows too so the
    history stays inspectable.
    """
    query = db.query(Document)
    if active_only:
        query = query.filter(Document.status == "active")
    docs = query.all()
    db.query(DocReference).delete()
    for doc in docs:
        for ref in extract_references(doc.content):
            db.add(
                DocReference(
                    source_doc_id=doc.id,
                    target_doc_number=ref,
                    reference_type="references",
                )
            )
    db.commit()


def _doctrine_folders_or_fail() -> list[Path]:
    folders = doctrine_folders()
    if not folders:
        raise FileNotFoundError(
            f"Doctrine path not found: {settings.doctrine_path}. Set DOCTRINE_PATH to the folder "
            "containing the RAGSEO markdown library."
        )
    return folders


def ingest_all_docs(db: DBSession) -> dict:
    """Ingest every markdown file across all doctrine folders (full reingest)."""
    _doctrine_folders_or_fail()

    md_files = scan_doctrine_files()
    stats = _new_stats()

    db_docs = db.query(Document).all()
    by_filename = {d.filename: d for d in db_docs}
    by_number = {d.doc_number: d for d in db_docs if d.status == "active"}

    for filepath in md_files:
        try:
            # SAVEPOINT per file: a bad file must not discard the documents
            # already ingested earlier in this same scan (a session-wide rollback
            # would) and must not poison every later file with a poisoned
            # transaction.
            with db.begin_nested():
                outcome = _ingest_one(
                    db,
                    filepath,
                    stats=stats,
                    by_filename=by_filename,
                    by_number=by_number,
                    backfill=True,
                )
            if outcome in ("skipped", "backfilled"):
                stats["skipped"] += 1
            elif outcome == "updated":
                stats["updated"] += 1
            else:
                stats["created"] += 1
        except Exception as e:
            stats["errors"].append(f"{filepath.name}: {e!s}")

    db.commit()
    _rebuild_references(db, active_only=False)
    return stats


def ingest_files(db: DBSession, paths: list[Path]) -> dict:
    """Ingest only the given files, with no filesystem sweep.

    Scoped on purpose: the website upload path must not be able to mark
    anything ``missing``, and it must not re-embed the whole library. The
    reference graph is still rebuilt so the new documents' cross-references are
    immediately visible in the UI.

    Returns the usual stat counters plus a per-file ``files`` breakdown (one
    entry per path, ``doc_number``/``title``/``chunks`` filled in) so the
    upload endpoint can report exactly what each document became.
    """
    stats = _new_stats()
    results: list[dict] = []

    db_docs = db.query(Document).all()
    by_filename = {d.filename: d for d in db_docs}
    by_number = {d.doc_number: d for d in db_docs if d.status == "active"}

    for filepath in paths:
        entry = {
            "filename": filepath.name,
            "doc_number": extract_doc_number(filepath.name),
            "title": extract_title("", filepath.name),
            "status": "unchanged",
            "chunks": 0,
            "error": None,
        }
        chunks_before = stats["chunks"]
        try:
            with db.begin_nested():
                outcome = _ingest_one(
                    db,
                    filepath,
                    stats=stats,
                    by_filename=by_filename,
                    by_number=by_number,
                )
                doc = by_filename.get(filepath.name)
                if doc is not None:
                    entry["doc_number"] = doc.doc_number
                    entry["title"] = doc.title
            # `skipped` is the stats counter's vocabulary; the per-file entry
            # speaks the same words the ingest-status API uses, so the upload
            # response does not have to translate (and cannot mistranslate an
            # unknown outcome into a spurious error).
            entry["status"] = "unchanged" if outcome == "skipped" else outcome
            entry["chunks"] = stats["chunks"] - chunks_before
            if outcome == "updated":
                stats["updated"] += 1
            elif outcome == "created":
                stats["created"] += 1
            else:
                stats["skipped"] += 1
        except Exception as e:
            stats["errors"].append(f"{filepath.name}: {e!s}")
            entry["status"] = "error"
            entry["error"] = str(e)
        results.append(entry)

    db.commit()
    _rebuild_references(db, active_only=True)
    stats["files"] = results
    return stats


def reconcile_doctrine(db: DBSession) -> dict:
    """Reconcile DB with filesystem: insert new, mark missing, detect superseded.

    Runs hourly on the worker, so it scans the union of the baked library and
    the upload folder — a scan of the baked folder alone would mark every
    uploaded document ``missing`` within the hour.

    Returns stats dict with created, updated, missing, superseded, errors.
    """
    _doctrine_folders_or_fail()

    stats = _new_stats(missing=0)

    # Active docs are what the missing-sweep below may touch; every doc is needed
    # for the filename cache so a restored file updates its row instead of
    # creating a duplicate.
    db_docs = db.query(Document).all()
    by_filename = {d.filename: d for d in db_docs}
    by_number = {d.doc_number: d for d in db_docs if d.status == "active"}

    md_files = scan_doctrine_files()
    fs_filenames = set()

    for filepath in md_files:
        fs_filenames.add(filepath.name)
        try:
            with db.begin_nested():
                outcome = _ingest_one(
                    db,
                    filepath,
                    stats=stats,
                    by_filename=by_filename,
                    by_number=by_number,
                )
            if outcome == "updated":
                stats["updated"] += 1
            elif outcome == "created":
                stats["created"] += 1
        except Exception as e:
            stats["errors"].append(f"{filepath.name}: {e!s}")

    # Mark DB docs not on filesystem as missing. Skip docs this run already
    # moved off active (superseded above) — otherwise the sweep would clobber
    # their fresh "superseded" status with "missing".
    for doc in db_docs:
        if doc.status != "active":
            continue
        if doc.filename not in fs_filenames:
            doc.status = "missing"
            doc.last_updated = datetime.now(UTC)
            stats["missing"] += 1

    db.commit()
    _rebuild_references(db, active_only=True)
    return stats
