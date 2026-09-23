#!/usr/bin/env bash
# Nightly Postgres dump of the RAGSEO db, run from the VPS host via cron.
#
# Usage (VPS, from /opt/ragseo-platform):
#   chmod +x scripts/backup_db.sh
#   mkdir -p /opt/ragseo-platform/backups
#   crontab -e  # add as root:
#   15 2 * * * /opt/ragseo-platform/scripts/backup_db.sh >> /opt/ragseo-platform/backups/backup.log 2>&1
#
# Restore a dump (custom format):
#   docker compose -f docker-compose.prod.yml exec -T db pg_restore \
#     --clean --if-exists -U ragseo -d ragseo /path/to/ragseo_YYYY-MM-DD_HHMM.dump
#
# NOTE: user uploads in ./external_uploads and the baked ./doctrine + ./external
# are not covered here. Doctrine/external are recovered from git; uploads are a
# follow-up (tar + off-box copy). Keep dumps off the VPS when practical.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-/opt/ragseo-platform/backups}"
COMPOSE_FILE="${COMPOSE_FILE:-$PROJECT_DIR/docker-compose.prod.yml}"
KEEP_DAYS="${KEEP_DAYS:-14}"

mkdir -p "$BACKUP_DIR"
STAMP="$(date +%F_%H%M)"
DEST="$BACKUP_DIR/ragseo_${STAMP}.dump"

if ! docker compose -f "$COMPOSE_FILE" exec -T db pg_dump -U ragseo --format=custom ragseo > "$DEST"; then
    echo "BACKUP FAILED $(date -Iseconds) rc=$?" >> "$BACKUP_DIR/backup.log"
    rm -f "$DEST"
    exit 1
fi

echo "ok $(date -Iseconds) ragseo_${STAMP}.dump $(wc -c < "$DEST") bytes" >> "$BACKUP_DIR/backup.log"

find "$BACKUP_DIR" -maxdepth 1 -name 'ragseo_*.dump' -mtime "+$KEEP_DAYS" -delete