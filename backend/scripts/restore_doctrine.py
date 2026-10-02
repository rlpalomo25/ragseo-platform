"""Rebuild the doctrine markdown library from the database.

Emergency repair for a lost ``doctrine/`` folder. The markdown bodies live in
``documents.content`` — one row per document, written from the file at ingest
time by ``_ingest_one`` via ``filepath.read_text(encoding="utf-8")`` — so the
library can be reconstructed without any external source.

The load-bearing concern is ``file_hash``. ``file_hash()`` hashes the raw bytes
of the file, and ``_ingest_one`` skips re-ingesting when the hash is unchanged.
If a reconstruction does not reproduce the stored hash, the next reconcile
decides the whole library changed and re-ingests and re-embeds all 122
documents. So this script verifies every file against its stored hash and
refuses to write into the live directory unless every one matches.

Writes to a scratch directory by default; ``--apply`` is what touches the real
library, and it is gated on a 100% match rate.

    python scripts/restore_doctrine.py --out /tmp/doctrine-restore
    python scripts/restore_doctrine.py --out /tmp/doctrine-restore --apply
"""

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.document import Document


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True, help="scratch directory to write into")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="write into the live doctrine dir (requires a 100% hash match)",
    )
    args = ap.parse_args()

    from app.config import get_settings

    settings = get_settings()

    db = SessionLocal()
    try:
        # Only `active` rows: a superseded document's file is gone from the
        # library by design, and recreating it would resurrect a retired doc.
        docs = db.query(Document).filter(Document.status == "active").order_by(Document.doc_number).all()
        print(f"  active documents in DB: {len(docs)}")
        if not docs:
            print("  nothing to restore")
            return 1

        args.out.mkdir(parents=True, exist_ok=True)
        matched, mismatched, unhashed = [], [], []

        for doc in docs:
            # read_text/read_bytes round-trip: content was stored as the decoded
            # text, so encoding back to UTF-8 must reproduce the original bytes.
            data = doc.content.encode("utf-8")
            path = args.out / doc.filename
            path.write_bytes(data)

            actual = hashlib.sha256(data).hexdigest()
            if doc.file_hash is None:
                unhashed.append(doc.filename)
            elif actual == doc.file_hash:
                matched.append(doc.filename)
            else:
                mismatched.append((doc.filename, doc.file_hash, actual))

        print(f"  hash match:   {len(matched)}/{len(docs)}")
        print(f"  hash MISMATCH: {len(mismatched)}")
        print(f"  no stored hash: {len(unhashed)}")
        for name, expected, actual in mismatched[:10]:
            print(f"    {name}\n      stored {expected}\n      wrote  {actual}")
        for name in unhashed[:10]:
            print(f"    {name}: file_hash is NULL, cannot verify")

        if not args.apply:
            print(f"\n  DRY RUN — wrote {len(docs)} file(s) to {args.out}")
            print("  re-run with --apply once the match rate looks right")
            return 0

        if mismatched or unhashed:
            print("\n  REFUSING to apply: not every file reproduced its stored hash.")
            print("  Applying would make the next reconcile re-ingest the whole library.")
            return 1

        live = Path(settings.doctrine_path)
        live.mkdir(parents=True, exist_ok=True)
        for doc in docs:
            (live / doc.filename).write_bytes(doc.content.encode("utf-8"))
        on_disk = len(list(live.glob("*.md")))
        print(f"\n  APPLIED — {on_disk} .md file(s) now in {live}")
        print("  safe to restart the celery worker")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
