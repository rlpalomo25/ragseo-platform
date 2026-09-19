"""Admin ingest control panel: preview doctrine folder vs DB, then reingest."""

import logging
from pathlib import Path, PurePath

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
from app.services.doc_ingestion import (
    extract_doc_number,
    extract_doc_type,
    extract_series,
    extract_title,
    extract_version,
    file_hash,
    ingest_all_docs,
)
from app.services.external_ingest import (
    classify,
    delete_external_export,
    file_sha256,
    import_external_file,
    import_external_folder,
)
from app.services.learning_loop import snapshot_publications

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()

MAX_UPLOAD_BYTES = 200 * 1024 * 1024  # 200 MB per uploaded export file


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


def _safe_filename(name: str) -> str:
    """Basename only, cross-platform (strips any directory components)."""
    clean = name.replace("\\", "/").strip().rstrip(".")
    stem = clean.rsplit("/", 1)[-1]
    if not stem or stem in (".", ".."):
        return ""
    return PurePath(stem).name


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


def _scan_doctrine(doctrine_path: Path, db: DBSession) -> list[IngestFileStatus]:
    files: list[IngestFileStatus] = []
    for filepath in sorted(doctrine_path.glob("*.md")):
        if filepath.name.startswith(".") or ":Zone.Identifier" in filepath.name:
            continue
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
    doctrine_path = Path(settings.doctrine_path)
    if not doctrine_path.exists():
        raise HTTPException(status_code=500, detail=f"Doctrine path not found: {doctrine_path}")

    files = _scan_doctrine(doctrine_path, db)
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
        doctrine_path=str(doctrine_path),
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
            if not filepath.is_file() or filepath.name.startswith("."):
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

    saved: list[Path] = []
    for f in files:
        name = _safe_filename(f.filename or "")
        if not name:
            continue
        content = await f.read()
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413, detail=f"{name} exceeds {MAX_UPLOAD_BYTES // (1024 * 1024)} MB"
            )
        (upload_dir / name).write_bytes(content)
        saved.append(upload_dir / name)
        logger.info("User '%s' uploaded %s (%d bytes)", user.username, name, len(content))

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
        name = _safe_filename(raw)
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
