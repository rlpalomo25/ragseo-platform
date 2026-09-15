#!/usr/bin/env bash
set -euo pipefail

# Stages doctrine and external market-data content into backend/doctrine and
# backend/external so the Dockerfile's baked COPY paths are populated at build
# time. The sources stay OUT of git (content-free baseline); run this before any
# image build on the VPS (or wherever the build context lives).

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOCTRINE_SRC="${DOCTRINE_SRC:-$(dirname "$REPO_ROOT")}"
EXTERNAL_SRC="${EXTERNAL_SRC:-$REPO_ROOT/09042026}"
DOCTRINE_DST="${DOCTRINE_DST:-$REPO_ROOT/backend/doctrine}"
EXTERNAL_DST="${EXTERNAL_DST:-$REPO_ROOT/backend/external}"

if [[ ! -d "$DOCTRINE_SRC" || ! -d "$EXTERNAL_SRC" ]]; then
    echo "Source dirs not found: DOCTRINE_SRC=$DOCTRINE_SRC EXTERNAL_SRC=$EXTERNAL_SRC" >&2
    exit 1
fi

mkdir -p "$DOCTRINE_DST" "$EXTERNAL_DST"

# Doctrine: copy .md only, dropping Windows ":Zone.Identifier" ADS twins.
find "$DOCTRINE_SRC" -maxdepth 1 -name '*.md' "!" -name '*:Zone.Identifier*' -print0 |
    while IFS= read -r -d '' f; do
        cp -f "$f" "$DOCTRINE_DST/"
    done

# External: mirror the weekly export folder exactly as the dev bind-mount did.
find "$EXTERNAL_SRC" -maxdepth 1 -type f -print0 |
    while IFS= read -r -d '' f; do
        cp -f "$f" "$EXTERNAL_DST/"
    done

echo "Doctrine: $(find "$DOCTRINE_DST" -maxdepth 1 -name '*.md' | wc -l) docs -> $DOCTRINE_DST"
echo "External: $(find "$EXTERNAL_DST" -maxdepth 1 -type f | wc -l) files -> $EXTERNAL_DST"