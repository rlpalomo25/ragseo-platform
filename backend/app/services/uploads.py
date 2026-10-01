"""Shared helpers for browser-uploaded files.

Lives in its own module because both upload routers need the same sanitising and
the same staging discipline; importing a private ``_safe_filename`` across
routers would couple them to each other's internals.

No fastapi import here on purpose — services stay framework-free and the routers
translate these exceptions into HTTP responses.
"""

import os
import shutil
import tempfile
from pathlib import Path, PurePath

CHUNK_BYTES = 1024 * 1024

#: Prefix for the per-request staging directory. Deliberately dot-prefixed: every
#: scanner that walks an upload folder skips dot-prefixed path components, so a
#: staging dir orphaned by a hard kill is invisible to them (see
#: ``is_hidden_path`` and its two call sites).
STAGING_PREFIX = ".staging-"


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


def is_hidden_path(path: Path, root: Path) -> bool:
    """True if any component of ``path`` under ``root`` is dot-prefixed.

    Checking only the basename is not enough. Both upload-folder scanners walk
    with ``rglob("*")``, which *descends into* dot-prefixed directories, so a
    staged file inside ``.staging-abc/`` has an innocent-looking basename and
    would be ingested. Comparing every component is what actually excludes a
    staging tree — and it is the general rule, so it also covers a ``.git`` or
    editor swap dir dropped into an upload folder.
    """
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        # Not under the root; fall back to inspecting the name itself.
        return path.name.startswith(".")
    return any(part.startswith(".") for part in parts)


async def stage_uploads(
    entries: list[tuple[str, object]],
    dest_dir: Path,
    *,
    max_bytes: int,
    before_commit=None,
) -> list[Path]:
    """Validate-then-atomically-commit a batch of uploads.

    ``entries`` is ``[(name, upload_file), ...]`` with names already sanitised and
    validated by the caller — names are cheap to check and must be checked for
    the *whole* batch before anything is read, so a bad name cannot half-apply.

    Three failure modes this avoids, all of which a naive write-as-you-go loop
    gets wrong:

    * **Partial batch on disk.** Writing as you validate means a 413 on file 3
      leaves files 1-2 in the upload folder. The caller reads a 413 as "nothing
      was saved", but the next sweep would find and ingest them. Nothing is
      committed until every file has passed the cap.
    * **A partially-written file visible to a scan.** Staging must therefore live
      on the *same filesystem* as the destination. Staging in the system temp dir
      looks tidy but is wrong: ``/tmp`` and the upload bind mount are different
      devices, so ``shutil.move`` silently degrades to copy+unlink and the
      destination becomes observable part-written — a truncated doctrine file can
      then be ingested and embedded by the hourly reconcile. Staging in a
      dot-prefixed subdirectory of the destination keeps both on one filesystem,
      so the commit is an ``os.replace`` rename, which is atomic.
    * **The whole batch in memory.** ``UploadFile.size`` is hardcoded to ``0`` by
      starlette's multipart parser and never updated, so a size check has to read
      the bytes anyway — and collecting them first to measure turns a 200 MB
      endpoint into a 200 MB x N memory spike. Files are streamed in chunks, so
      peak memory is one chunk regardless of file or batch size.

    If the commit phase fails partway (a full disk, a permission error), the
    destinations already committed by *this* call are removed and the exception
    propagates, so a failed request leaves the folder as it found it.

    ``before_commit`` is a test seam: called with the staging dir just before the
    renames, so a test can assert on the intermediate state (or inject a failure)
    without racing a real 40 MB transfer.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    committed: list[Path] = []
    staging = Path(tempfile.mkdtemp(prefix=STAGING_PREFIX, dir=dest_dir))
    try:
        for name, upload in entries:
            target = staging / name
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

        if before_commit is not None:
            before_commit(staging)

        # os.replace is atomic on a single filesystem and overwrites an existing
        # destination, which is what an in-place re-upload needs. Safe because
        # the whole batch is already staged and validated by this point.
        for staged_file in sorted(staging.iterdir()):
            if not staged_file.is_file():
                continue
            final = dest_dir / staged_file.name
            os.replace(staged_file, final)
            committed.append(final)
        return committed
    except Exception:
        # Roll back what THIS call committed. The staged copies are removed by the
        # rmtree below; tracking `committed` (not the staged paths, which no
        # longer exist once renamed) is what makes the rollback authoritative.
        for final in committed:
            final.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
