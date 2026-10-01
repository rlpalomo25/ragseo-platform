"""Shared helpers for browser-uploaded files.

Lives in its own module because both upload routers need the same sanitising
and the same per-request byte budget; importing a private ``_safe_filename``
across routers would couple them to each other's internals.
"""

from pathlib import PurePath


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
