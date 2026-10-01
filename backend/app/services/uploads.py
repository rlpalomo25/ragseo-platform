"""Shared helpers for browser-uploaded files.

Lives in its own module because both upload routers need the same sanitising and
the same staging discipline; importing a private ``_safe_filename`` across
routers would couple them to each other's internals.

No fastapi import here on purpose — services stay framework-free and the routers
translate these exceptions into HTTP responses.
"""

import shutil
import tempfile
from pathlib import Path, PurePath

CHUNK_BYTES = 1024 * 1024


class UploadTooLarge(Exception):
    """An upload exceeded its per-file byte cap. Carries the offending name."""

    def __init__(self, name: str, limit: int):
        super().__init__(f"{name} exceeds {limit} bytes")
        self.name = name
        self.limit = limit


def safe_filename(name: str) -> str:
    """Basename only, cross-platform (strips any directory components).

    Browsers send the client-side name in the multipart part, so it can contain
    ``../`` segments, Windows separators, or ``:Zone.Identifier`` suffixes.
    Returns "" for anything that does not reduce to a usable basename.
    """
    clean = name.replace("\\", "/").strip().rstrip(".")
    stem = clean.rsplit("/", 1)[-1]
    if not stem or stem in (".", ".."):
        return ""
    return PurePath(stem).name


async def stage_uploads(entries: list[tuple[str, object]], dest_dir: Path, *, max_bytes: int) -> list[Path]:
    """Stream uploads to a temp dir under a byte cap, then move them into place.

    ``entries`` is ``[(name, upload_file), ...]`` with names already sanitised and
    validated by the caller — names are cheap to check and must be checked for
    the *whole* batch before anything is read, so a bad name cannot half-apply.

    Two failure modes this avoids, both of which a naive loop gets wrong:

    * **Partial batch on disk.** Writing as you validate means a 413 on file 3
      leaves files 1-2 in the upload folder. The caller reads a 413 as "nothing
      was saved", but the next import sweep would find and ingest them. Nothing
      is moved into ``dest_dir`` until every file has passed.
    * **The whole batch in memory.** ``UploadFile.size`` is hardcoded to ``0`` by
      starlette's multipart parser and never updated, so a size check has to read
      the bytes anyway — and collecting them first to measure turns a 200 MB
      endpoint into a 200 MB x N memory spike. Files are streamed in chunks
      instead, so peak memory is one chunk regardless of file or batch size.

    Staging lives in the system temp dir rather than beside the destination,
    because ``import_external_folder`` walks its folder with ``rglob("*")`` and
    would happily ingest a half-written staging file left there by a crash.

    Files are moved rather than copied, so a rollback of the temp dir is
    authoritative: nothing to clean up in the upload folder.
    """
    staged: list[tuple[str, Path]] = []
    try:
        with tempfile.TemporaryDirectory(prefix="ragseo-upload-") as tmp:
            tmp_dir = Path(tmp)
            for name, upload in entries:
                target = tmp_dir / name
                written = 0
                with target.open("wb") as fh:
                    while True:
                        chunk = await upload.read(CHUNK_BYTES)  # type: ignore[attr-defined]
                        if not chunk:
                            break
                        written += len(chunk)
                        if written > max_bytes:
                            raise UploadTooLarge(name, max_bytes)
                        fh.write(chunk)
                staged.append((name, target))

            dest_dir.mkdir(parents=True, exist_ok=True)
            saved = []
            for name, path in staged:
                final = dest_dir / name
                shutil.move(str(path), str(final))
                saved.append(final)
            return saved
    except Exception:
        # Belt and braces: the TemporaryDirectory context already removed the
        # staging files, but if anything was moved before the failure those
        # copies are ours to remove.
        for _name, path in staged:
            if path.exists():
                path.unlink(missing_ok=True)
        raise
