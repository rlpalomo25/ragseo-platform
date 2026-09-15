#!/bin/sh
set -e

python scripts/migrate.py

if [ "${RUN_SEED:-0}" = "1" ]; then
    python scripts/seed.py
fi

if [ "${RUN_EXTERNAL:-0}" = "1" ]; then
    python scripts/import_external.py
fi

exec "$@"