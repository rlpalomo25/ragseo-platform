#!/usr/bin/env bash
# Rebuild the doctrine markdown library from the database, without a rebuild.
#
# Emergency repair for a lost/empty doctrine/ folder. The baked image cannot be
# used for this: `restore_doctrine.py` lives in the repo, and the running image
# predates it, so `docker compose run backend /app/scripts/...` fails with
# "No such file or directory" until the image is rebuilt. This script needs
# nothing but psql and python3, both of which are on the VPS already.
#
# The markdown bodies live in documents.content, written at ingest time from the
# file via read_text(encoding="utf-8"), so encoding back to UTF-8 must reproduce
# the original bytes. That is verified per file against the stored file_hash,
# because a file that fails to reproduce its hash makes the next hourly
# reconcile decide the whole library changed and re-ingest and re-embed all of it.
#
#   ./restore_doctrine.sh                 # dry run, writes to /tmp only
#   ./restore_doctrine.sh --apply         # write into ./doctrine (needs 100%)
set -euo pipefail

cd "$(dirname "$0")"
COMPOSE="docker compose -f docker-compose.prod.yml"
OUT=/tmp/doctrine-restore
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

mkdir -p "$OUT"

# encode(...) wraps base64 at 76 chars, so the newlines must be stripped or every
# row becomes several lines. -A -t for unaligned tuples-only, | as the separator
# (it cannot appear in a filename or in base64).
echo "  reading documents from the database..."
$COMPOSE exec -T db psql -U ragseo -d ragseo -At -F '|' -c \
  "SELECT filename,
          replace(replace(encode(convert_to(content,'UTF8'),'base64'), E'\n',''), E'\r',''),
          coalesce(file_hash,'')
   FROM documents WHERE status = 'active'
   ORDER BY doc_number" > "$OUT/docs.b64"

python3 - "$OUT" "$APPLY" <<'PY'
import base64, hashlib, sys
from pathlib import Path

out = Path(sys.argv[1])
apply = sys.argv[2] == "1"
scratch = out / "files"
scratch.mkdir(exist_ok=True)

rows = 0
matched, mismatched, unhashed = [], [], []
for line in (out / "docs.b64").read_text().splitlines():
    if not line.strip():
        continue
    name, b64, expected = line.split("|", 2)
    data = base64.b64decode(b64)
    (scratch / name).write_bytes(data)
    rows += 1
    if not expected:
        unhashed.append(name)
    elif hashlib.sha256(data).hexdigest() == expected:
        matched.append(name)
    else:
        mismatched.append(name)

print(f"  active documents:   {rows}")
print(f"  hash match:         {len(matched)}")
print(f"  hash MISMATCH:      {len(mismatched)}")
print(f"  no stored hash:     {len(unhashed)}")
for name in mismatched[:10]:
    print(f"    MISMATCH: {name}")

if not apply:
    print(f"\n  DRY RUN — reconstructed files are in {scratch}")
    print("  re-run with --apply once the numbers above are clean")
    sys.exit(0)

if mismatched or unhashed:
    print("\n  REFUSING to apply: not every file reproduced its stored hash.")
    print("  Applying would make the next reconcile re-ingest the entire library.")
    sys.exit(1)

live = Path("doctrine")
live.mkdir(parents=True, exist_ok=True)
for name in matched:
    (live / name).write_bytes((scratch / name).read_bytes())
on_disk = len(list(live.glob("*.md")))
print(f"\n  APPLIED — {on_disk} .md file(s) now in {live.resolve()}")
print("  safe to restart the celery worker")
PY
