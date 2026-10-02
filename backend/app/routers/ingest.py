"""Admin ingest control panel: preview doctrine folder vs DB, then reingest."""

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from app.config import get_settings
from app.database import get_db
from app.dependencies import require_admin, require_writer
from app.models.chunk import DocChunk
from app.models.document import Document
from app.models.external import ExternalExport
from app.models.user import User
from app.services.audit import log_audit
from app.services.doc_ingestion import (
    DOC_PATTERN,
    doctrine_folders,
    extract_doc_number,
    extract_doc_type,
    extract_series,
    extract_title,
    extract_version,
    file_hash,
    ingest_all_docs,
    ingest_files,
    scan_doctrine_files,
)
from app.services.external_ingest import (
    classify,
    delete_external_export,
    file_sha256,
    import_external_file,
    import_external_folder,
)
from app.services.learning_loop import snapshot_publications
from app.services.uploads import (
    BatchTooLarge,
    UploadTooLarge,
    is_hidden_path,
    safe_filename,
    stage_uploads,
)

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()

MAX_UPLOAD_BYTES = 200 * 1024 * 1024  # 200 MB per uploaded export file
MAX_DOCTRINE_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB per uploaded doctrine doc
# Per-file caps do not bound a request. Starlette spools the entire multipart
# body to a temp file *before* the endpoint runs, so an unbounded batch is a
# disk-exhaustion primitive by a logged-in writer.
#
# `File(..., max_length=N)` is NOT a way to cap the file count: on FastAPI 0.115
# that argument lands in the pydantic FieldInfo and never reaches Starlette's
# MultiPartParser, so it is silently ignored for a `list[UploadFile]`. The parser
# caps live in `Request.form(max_files=...)`, which FastAPI calls with its own
# defaults. Enforced instead by:
#   1. RequestBodyLimitMiddleware — rejects on Content-Length before the body is
#      read at all, which is the only place the 10 GB/200 GB case is caught early.
#   2. An explicit count check at the top of each route, authoritative for
#      chunked requests that arrive without a Content-Length.
MAX_DOCTRINE_FILES = 20
MAX_DOCTRINE_TOTAL_BYTES = 50 * 1024 * 1024  # 50 MB per batch
MAX_DOCTRINE_REQUEST_BYTES = 60 * 1024 * 1024  # Content-Length ceiling incl. multipart framing
MAX_EXTERNAL_FILES = 10
MAX_EXTERNAL_TOTAL_BYTES = 500 * 1024 * 1024  # 500 MB per batch
MAX_EXTERNAL_REQUEST_BYTES = 510 * 1024 * 1024  # Content-Length ceiling incl. multipart framing
# Document.filename is String(255); a longer name would be truncated by the DB
# (or rejected outright on Postgres) and then never match its own file again.
MAX_DOCTRINE_FILENAME_LEN = 255
DOCTRINE_NAME_EXAMPLE = "Doc <number>_<Title>.md (for example: Doc 100_Master Content Doctrine.md)"


def _external_folders() -> list[Path]:
    """Baked + writable external-data folders; nonexistent dirs are skipped."""
    folders: list[Path] = []
    for folder in dict.fromkeys(
        [
            Path(settings.external_data_path),
            Path(settings.external_upload_path),
        ]
    ):
        if folder.is_dir():
            folders.append(folder)
    return folders


class IngestFileStatus(BaseModel):
    filename: str
    doc_number: str
    title: str
    series: str | None = None
    doc_type: str | None = None
    version: str | None = None
    word_count: int = 0
    status: str  # "new" | "changed" | "unchanged" | "error"
    error: str | None = None
    chunk_count: int = 0
    embedded_chunks: int = 0


class IngestTotals(BaseModel):
    files: int = 0
    new: int = 0
    changed: int = 0
    unchanged: int = 0
    errors: int = 0
    chunks: int = 0
    embedded: int = 0
    embedding_coverage: float = 0.0


class IngestStatusResponse(BaseModel):
    doctrine_path: str
    totals: IngestTotals
    files: list[IngestFileStatus]
    doctrine_folders: list[str] = []


class IngestStats(BaseModel):
    created: int = 0
    updated: int = 0
    skipped: int = 0
    chunks: int = 0
    embedding_failures: int = 0
    errors: list[str] = []


class IngestResultResponse(BaseModel):
    message: str
    stats: IngestStats


def _scan_doctrine(db: DBSession) -> list[IngestFileStatus]:
    """Inspect every markdown file across the doctrine folders (baked + uploads)."""
    files: list[IngestFileStatus] = []
    for filepath in scan_doctrine_files():
        try:
            content = filepath.read_text(encoding="utf-8")
            fhash = file_hash(str(filepath))
            filename = filepath.name
            doc_number = extract_doc_number(filename)
            title = extract_title(content, filename)

            existing = db.query(Document).filter(Document.filename == filename).first()
            if existing and existing.file_hash == fhash:
                status = "unchanged"
            elif existing:
                status = "changed"
            else:
                status = "new"

            chunk_count = 0
            embedded_chunks = 0
            if existing:
                row = (
                    db.query(func.count(DocChunk.id), func.count(DocChunk.embedding))
                    .filter(DocChunk.document_id == existing.id)
                    .first()
                )
                chunk_count, embedded_chunks = row or (0, 0)

            files.append(
                IngestFileStatus(
                    filename=filename,
                    doc_number=doc_number,
                    title=title,
                    series=extract_series(doc_number),
                    doc_type=extract_doc_type(title, filename),
                    version=extract_version(content),
                    word_count=len(content.split()),
                    status=status,
                    chunk_count=chunk_count or 0,
                    embedded_chunks=embedded_chunks or 0,
                )
            )
        except Exception as e:
            logger.warning("Failed to inspect %s: %s", filepath.name, e)
            files.append(
                IngestFileStatus(
                    filename=filepath.name,
                    doc_number="",
                    title="",
                    status="error",
                    error=str(e),
                )
            )
    return files


@router.get("/ingest/status", response_model=IngestStatusResponse)
def ingest_status(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    folders = doctrine_folders()
    if not folders:
        raise HTTPException(status_code=500, detail=f"Doctrine path not found: {settings.doctrine_path}")

    files = _scan_doctrine(db)
    totals = IngestTotals()
    for f in files:
        totals.files += 1
        if f.status == "new":
            totals.new += 1
        elif f.status == "changed":
            totals.changed += 1
        elif f.status == "unchanged":
            totals.unchanged += 1
        elif f.status == "error":
            totals.errors += 1
        totals.chunks += f.chunk_count
        totals.embedded += f.embedded_chunks
    if totals.chunks:
        totals.embedding_coverage = round(totals.embedded / totals.chunks, 4)

    return IngestStatusResponse(
        doctrine_path=settings.doctrine_path,
        doctrine_folders=[str(f) for f in folders],
        totals=totals,
        files=files,
    )


@router.post("/ingest/reingest", response_model=IngestResultResponse)
def reingest(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    try:
        stats = ingest_all_docs(db)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return IngestResultResponse(message="Reingestion complete", stats=IngestStats(**stats))


class DoctrineUploadItem(BaseModel):
    filename: str
    doc_number: str = ""
    title: str = ""
    status: str  # "created" | "updated" | "unchanged" | "error"
    chunks: int = 0
    superseded: str | None = None
    error: str | None = None


class DoctrineUploadResultResponse(BaseModel):
    message: str
    created: int = 0
    updated: int = 0
    unchanged: int = 0
    errors: int = 0
    chunks: int = 0
    files: list[DoctrineUploadItem] = []


def _baked_doctrine_names() -> set[str]:
    """Filenames owned by the read-only library baked into the image."""
    baked = Path(settings.doctrine_path)
    if not baked.is_dir():
        return set()
    return {p.name for p in baked.iterdir() if p.is_file()}


def _reject_unusable_doctrine_name(name: str, baked: set[str]) -> None:
    """Refuse a filename the doctrine parser would mangle, or that already exists baked.

    ``extract_doc_number`` falls back to the whole filename when there is no
    ``_``/``:`` after the number, so a loose name like ``random.md`` yields
    ``doc_number="random"``. That garbage becomes permanent under
    ``uq_documents_doc_number_active``, permanently blocking the real Doc 100.
    Every rejection below therefore happens *before* anything is written to
    disk, and rejects the whole batch so a typo cannot half-apply.
    """
    if len(name) > MAX_DOCTRINE_FILENAME_LEN:
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' is longer than {MAX_DOCTRINE_FILENAME_LEN} characters",
        )
    if not name.lower().endswith(".md"):
        raise HTTPException(status_code=400, detail=f"'{name}' is not a markdown (.md) file")
    if not DOC_PATTERN.search(name):
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' does not carry a recognisable doc number. Expected {DOCTRINE_NAME_EXAMPLE}",
        )
    if name in baked:
        # scan_doctrine_files() resolves filename collisions in favour of the
        # baked folder, so an accepted upload shadowing a library file would be
        # reported as ingested and then silently ignored by every later scan.
        raise HTTPException(
            status_code=409,
            detail=(
                f"'{name}' is part of the baked doctrine library. Editing library "
                "documents is an ops task (sync_doctrine.sh + redeploy), not a website upload."
            ),
        )


@router.post("/ingest/doctrine/upload", response_model=DoctrineUploadResultResponse)
async def upload_doctrine(
    files: list[UploadFile] = File(...),
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    """Save uploaded doctrine markdown and ingest it inline (writer or admin).

    Mirrors ``POST /api/ingest/external/upload``: the bytes land in the writable
    ``doctrine_upload_path`` (gitignored, survives redeploys) and are ingested
    immediately so the change is live for the very next agent job — the hourly
    reconcile would otherwise take up to an hour.
    """
    upload_dir = Path(settings.doctrine_upload_path)
    baked = _baked_doctrine_names()

    # Authoritative count cap. The middleware has already rejected an oversized
    # Content-Length before this ran, but that header is optional and can simply
    # be omitted, so the batch is counted here as well. Checked before any read.
    if len(files) > MAX_DOCTRINE_FILES:
        raise HTTPException(
            status_code=413,
            detail=(
                f"{len(files)} files exceeds the {MAX_DOCTRINE_FILES} file limit for one "
                "request. Send fewer documents at a time."
            ),
        )

    # Validate every name before reading a single byte, so a bad name anywhere in
    # the batch cannot leave half of it on disk for the hourly reconcile to find.
    planned: list[tuple[str, UploadFile]] = []
    for f in files:
        name = safe_filename(f.filename or "")
        if not name:
            continue
        _reject_unusable_doctrine_name(name, baked)
        planned.append((name, f))

    if not planned:
        raise HTTPException(status_code=400, detail="No usable .md files in the upload")

    # Record which active document each upload will displace, so the response
    # can name it: superseding a governing doc is the single most consequential
    # thing this endpoint does, and it is not reversible from the website.
    supersedes: dict[str, str] = {}
    for name, _ in planned:
        doc_number = extract_doc_number(name)
        current = (
            db.query(Document)
            .filter(
                Document.doc_number == doc_number,
                Document.filename != name,
                Document.status == "active",
            )
            .first()
        )
        if current:
            supersedes[name] = f"{current.doc_number} ({current.title})"

    try:
        saved = await stage_uploads(
            planned,
            upload_dir,
            max_bytes=MAX_DOCTRINE_UPLOAD_BYTES,
            max_total_bytes=MAX_DOCTRINE_TOTAL_BYTES,
        )
    except UploadTooLarge as e:
        raise HTTPException(
            status_code=413,
            detail=f"'{e.name}' exceeds the {e.limit // (1024 * 1024)} MB per-file limit",
        ) from e
    except BatchTooLarge as e:
        raise HTTPException(
            status_code=413,
            detail=(
                f"This batch exceeds the {e.limit // (1024 * 1024)} MB total limit. "
                f"Send fewer documents at a time (up to {MAX_DOCTRINE_FILES} files, "
                f"{MAX_DOCTRINE_UPLOAD_BYTES // (1024 * 1024)} MB each)."
            ),
        ) from e
    for path in saved:
        logger.info(
            "User '%s' uploaded doctrine %s (%d bytes)", user.username, path.name, path.stat().st_size
        )

    stats = ingest_files(db, saved)
    by_name = {entry["filename"]: entry for entry in stats.get("files", [])}

    resp = DoctrineUploadResultResponse(
        message=f"Uploaded and ingested {len(saved)} doctrine document(s)",
        chunks=stats["chunks"],
    )
    for filepath in saved:
        entry = by_name.get(filepath.name, {})
        status = entry.get("status", "error")
        item = DoctrineUploadItem(
            filename=filepath.name,
            doc_number=entry.get("doc_number") or extract_doc_number(filepath.name),
            title=entry.get("title") or extract_title("", filepath.name),
            status=status,
            chunks=entry.get("chunks", 0),
            superseded=supersedes.get(filepath.name),
            error=entry.get("error"),
        )
        resp.files.append(item)
        if status == "created":
            resp.created += 1
        elif status == "updated":
            resp.updated += 1
        elif status == "unchanged":
            resp.unchanged += 1
        else:
            resp.errors += 1

    log_audit(
        db,
        user=user,
        action="doctrine.upload",
        route="/api/ingest/doctrine/upload",
        detail=(
            f"{resp.created} created, {resp.updated} updated, {resp.unchanged} unchanged, "
            f"{resp.errors} errors"
            + (f"; superseded {sorted(set(supersedes.values()))}" if supersedes else "")
        ),
        status_code=200,
    )
    # The audit row is written after ingest_files, which has already committed its
    # own work, so it has no caller transaction to join and needs an explicit
    # commit of its own. Written last so a batch that raised never records a
    # success.
    db.commit()
    return resp


class ExternalFileStatus(BaseModel):
    filename: str
    source_type: str | None = None
    domain: str | None = None
    brand: str | None = None
    status: str  # "new" | "imported" | "error"
    rows: int = 0
    error: str | None = None
    deletable: bool = False


class ExternalTotals(BaseModel):
    files: int = 0
    imported: int = 0
    errors: int = 0
    rows: int = 0


class ExternalStatusResponse(BaseModel):
    external_data_path: str
    totals: ExternalTotals
    files: list[ExternalFileStatus]


class ExternalImportItem(BaseModel):
    filename: str
    source_type: str | None = None
    status: str
    rows: int = 0
    error: str | None = None


class ExternalImportResultResponse(BaseModel):
    message: str
    imported: int = 0
    skipped: int = 0
    errors: int = 0
    files: list[ExternalImportItem]


class ExternalDeleteRequest(BaseModel):
    filenames: list[str]


class ExternalDeleteItem(BaseModel):
    filename: str
    status: str  # "deleted" | "baked" | "not_found"
    message: str | None = None


class ExternalDeleteResultResponse(BaseModel):
    message: str
    deleted: int = 0
    baked: int = 0
    not_found: int = 0
    files: list[ExternalDeleteItem]


@router.get("/ingest/external/status", response_model=ExternalStatusResponse)
def external_status(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    folders = _external_folders()
    if not folders:
        raise HTTPException(
            status_code=500, detail=f"External data path not found: {settings.external_data_path}"
        )

    imported_hashes = {row[0] for row in db.query(ExternalExport.file_hash).all()}

    upload_dir = Path(settings.external_upload_path).resolve()
    seen: dict[str, ExternalFileStatus] = {}
    deletable: set[str] = set()
    for folder in folders:
        for filepath in sorted(folder.rglob("*")):
            if not filepath.is_file() or is_hidden_path(filepath, folder):
                continue
            try:
                source_type, domain, brand = classify(filepath)
                source_type = source_type.split(":", 1)[0]
                fhash = file_sha256(filepath.read_bytes())
            except Exception as e:
                status = ExternalFileStatus(filename=filepath.name, status="error", error=str(e))
            else:
                row = db.query(ExternalExport).filter(ExternalExport.file_hash == fhash).first()
                status = ExternalFileStatus(
                    filename=filepath.name,
                    source_type=source_type,
                    domain=domain,
                    brand=brand,
                    status="imported" if fhash in imported_hashes else "new",
                    rows=row.row_count if row else 0,
                )
            seen.setdefault(filepath.name, status)
            if filepath.resolve().is_relative_to(upload_dir):
                deletable.add(filepath.name)
    files: list[ExternalFileStatus] = []
    for name, f in seen.items():
        f.deletable = name in deletable
        files.append(f)

    totals = ExternalTotals(files=len(files), rows=sum(f.rows for f in files))
    totals.imported = sum(1 for f in files if f.status == "imported")
    totals.errors = sum(1 for f in files if f.status == "error")
    return ExternalStatusResponse(
        external_data_path=str(Path(settings.external_upload_path)),
        totals=totals,
        files=files,
    )


@router.post("/ingest/external", response_model=ExternalImportResultResponse)
def import_external(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    folders = _external_folders()
    if not folders:
        raise HTTPException(
            status_code=500, detail=f"External data path not found: {settings.external_data_path}"
        )
    results = []
    for folder in folders:
        results.extend(import_external_folder(folder, db))

    # Learning loop: refresh per-publication performance snapshots now that the
    # weekly numbers landed (idempotent; one snapshot per publication+export).
    learning = snapshot_publications(db)
    logger.info("Learning loop after import: %s", learning)
    seen: dict[str, dict] = {}
    for r in results:
        if r["status"] == "imported" or r["filename"] not in seen:
            seen[r["filename"]] = r
    results = list(seen.values())
    resp = ExternalImportResultResponse(message="External data import complete", files=[])
    for r in results:
        resp.files.append(
            ExternalImportItem(
                filename=r["filename"],
                status=r["status"],
                rows=r.get("rows", 0),
                source_type=r.get("source_type"),
                error=r.get("error"),
            )
        )
        if r["status"] == "imported":
            resp.imported += 1
        elif r["status"] == "skipped":
            resp.skipped += 1
        else:
            resp.errors += 1
    return resp


@router.post("/ingest/external/upload", response_model=ExternalImportResultResponse)
async def upload_external(
    files: list[UploadFile] = File(...),
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    """Save uploaded weekly exports to the writable folder and import them (any logged-in user)."""
    upload_dir = Path(settings.external_upload_path)
    if upload_dir == Path(settings.external_data_path):
        upload_dir = upload_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Authoritative count cap; see upload_doctrine for why this is not only
    # enforced in the middleware.
    if len(files) > MAX_EXTERNAL_FILES:
        raise HTTPException(
            status_code=413,
            detail=(
                f"{len(files)} files exceeds the {MAX_EXTERNAL_FILES} file limit for one "
                "request. Send fewer exports at a time."
            ),
        )

    # Staged rather than written in-loop: a size cap tripped on a later file must
    # not leave earlier ones in the upload dir, where the caller believes nothing
    # was saved and the next import sweep would ingest them anyway.
    planned: list[tuple[str, UploadFile]] = []
    for f in files:
        name = safe_filename(f.filename or "")
        if not name:
            continue
        planned.append((name, f))

    try:
        saved = await stage_uploads(
            planned,
            upload_dir,
            max_bytes=MAX_UPLOAD_BYTES,
            max_total_bytes=MAX_EXTERNAL_TOTAL_BYTES,
        )
    except UploadTooLarge as e:
        raise HTTPException(status_code=413, detail=f"{e.name} exceeds {e.limit // (1024 * 1024)} MB") from e
    except BatchTooLarge as e:
        raise HTTPException(
            status_code=413,
            detail=(
                f"This batch exceeds the {e.limit // (1024 * 1024)} MB total limit. "
                f"Send fewer exports at a time (up to {MAX_EXTERNAL_FILES} files, "
                f"{MAX_UPLOAD_BYTES // (1024 * 1024)} MB each)."
            ),
        ) from e
    for path in saved:
        logger.info("User '%s' uploaded %s (%d bytes)", user.username, path.name, path.stat().st_size)

    results = []
    for p in saved:
        try:
            results.append(import_external_file(db, p))
        except Exception as e:
            logger.warning("Failed to import uploaded %s: %s", p.name, e)
            results.append({"filename": p.name, "status": "error", "error": str(e)})
    learning = snapshot_publications(db)
    logger.info("Learning loop after upload: %s", learning)
    resp = ExternalImportResultResponse(message=f"Uploaded and imported {len(results)} file(s)", files=[])
    for r in results:
        resp.files.append(
            ExternalImportItem(
                filename=r["filename"],
                status=r["status"],
                rows=r.get("rows", 0),
                source_type=r.get("source_type"),
                error=r.get("error"),
            )
        )
        if r["status"] == "imported":
            resp.imported += 1
        elif r["status"] == "skipped":
            resp.skipped += 1
        else:
            resp.errors += 1
    return resp


@router.delete("/ingest/external/delete", response_model=ExternalDeleteResultResponse)
def delete_external(
    payload: ExternalDeleteRequest,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    """Delete old uploads from the writable folder and their DB rows (any logged-in user).

    Files baked into the image under ``external_data_path`` are read-only and can
    never be removed from the website, so only upload-folder files are unlinked;
    matching ExternalExport rows (by filename, plus by hash of any file just
    removed, which also cleans up orphans) are deleted with their detail rows.
    """
    upload_dir = Path(settings.external_upload_path)
    baked_dir = Path(settings.external_data_path)
    resp = ExternalDeleteResultResponse(message="Delete selected exports", files=[])

    # Baked (read-only image-layer) exports are never deletable from the website.
    # Policy for uploads: the weekly exports folder is a shared team resource, so
    # any writer/admin may delete any uploaded file — but baked rows/files must
    # never be touched, even when a delete targets a renamed/hash-colliding upload.
    baked_file_names: set[str] = set()
    if baked_dir.is_dir():
        baked_file_names = {p.name for p in baked_dir.iterdir() if p.is_file()}

    for raw in payload.filenames:
        name = safe_filename(raw)
        if not name:
            resp.not_found += 1
            resp.files.append(ExternalDeleteItem(filename="", status="not_found", message="Invalid filename"))
            continue

        upload_path = upload_dir / name

        # A name colliding with a baked file is refused outright — never unlink
        # a same-named upload copy nor delete any rows for it.
        if name in baked_file_names:
            resp.baked += 1
            resp.files.append(
                ExternalDeleteItem(
                    filename=name,
                    status="baked",
                    message="Part of the base baked dataset and cannot be deleted from the website.",
                )
            )
            continue

        hashes: list[str] = []
        if upload_path.is_file():
            hashes.append(file_sha256(upload_path.read_bytes()))
            upload_path.unlink()

        exports: dict = {}
        for row in db.query(ExternalExport).filter(ExternalExport.file_name == name).all():
            exports[row.id] = row
        if hashes:
            for h in hashes:
                for row in db.query(ExternalExport).filter(ExternalExport.file_hash == h).all():
                    exports[row.id] = row

        # Never delete rows that belong to baked files (e.g. an upload whose bytes
        # duplicate a baked export — the importer hash-dedupes, so only the baked
        # row exists under that hash). The upload copy (if any) is still removed.
        if baked_file_names:
            exports = {rid: row for rid, row in exports.items() if row.file_name not in baked_file_names}

        if not exports and not hashes:
            db.commit()
            resp.not_found += 1
            resp.files.append(ExternalDeleteItem(filename=name, status="not_found"))
            continue

        for row in exports.values():
            logger.info(
                "User '%s' deleted export '%s' (rows: %d)", user.username, row.file_name, row.row_count
            )
            delete_external_export(db, row)
        db.commit()
        resp.deleted += 1
        resp.files.append(ExternalDeleteItem(filename=name, status="deleted"))

    resp.message = f"Deleted {resp.deleted} file(s)"
    return resp
