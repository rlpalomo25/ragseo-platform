#!/usr/bin/env bash
# Nightly backup of the RAGSEO Postgres db AND the on-disk content directories,
# run from the VPS host via cron.
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
# Restore the content archive (overwrites those three directories):
#   tar -xzf /opt/ragseo-platform/backups/content_YYYY-MM-DD_HHMM.tar.gz \
#     -C /opt/ragseo-platform
#
# ---------------------------------------------------------------------------
# WHY THIS ARCHIVES FILES, NOT JUST THE DATABASE
#
# The database is not the whole system. On 2026-10-01 a production rebuild baked
# an empty /app/doctrine (the library had never been in git) and the hourly
# reconcile marked all 122 documents `missing`. Recovering that needed
# scripts/restore_doctrine.sh, reconstructing every file from documents.content.
# That reconstruction is verified, but it is a repair path, not a backup:
# it only covers `active` rows, and it depends on the database being intact.
#
# So the directories that hold the actual content are archived as well:
#   doctrine/           the ops-managed library, mounted read-only at /app/doctrine
#   doctrine_uploads/   markdown uploaded through the website
#   external_uploads/   market-data exports uploaded through the website
# `external/` is the baked-in weekly export set; it is tracked in git and is
# deliberately NOT archived here.
#
# ---------------------------------------------------------------------------
# OFF-BOX COPYING — CONFIGURE THIS OR READ THIS
#
# Everything below writes to the same disk as the data it protects. A host loss
# loses both, which is exactly what happened on 2026-10-01. To copy off-box, set
# OFFBOX_CMD to a shell command that receives the backup dir as its last
# argument, for example:
#
#   15 2 * * * OFFBOX_CMD='rclone copy /opt/ragseo-platform/backups gdrive:ragseo' \
#     /opt/ragseo-platform/scripts/backup_db.sh >> /opt/ragseo-platform/backups/backup.log 2>&1
#
# While OFFBOX_CMD is unset the script still succeeds, but every run logs
# "OFFBOX NOT CONFIGURED" so the gap stays visible in backup.log rather than
# being silently assumed fine.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-/opt/ragseo-platform/backups}"
COMPOSE_FILE="${COMPOSE_FILE:-$PROJECT_DIR/docker-compose.prod.yml}"
KEEP_DAYS="${KEEP_DAYS:-14}"
OFFBOX_CMD="${OFFBOX_CMD:-}"

# Directories whose contents are irreplaceable. A missing one is reported, not
# fatal: external/ and doctrine_uploads/ may legitimately be empty on a fresh
# install, and failing the whole run would silently stop the database backup.
CONTENT_DIRS=(doctrine doctrine_uploads external_uploads)

log() { echo "$*"; }
fail() {
    echo "BACKUP FAILED $(date -Iseconds) rc=$1" >> "$BACKUP_DIR/backup.log"
    exit 1
}

mkdir -p "$BACKUP_DIR"
STAMP="$(date +%F_%H%M)"
DB_DEST="$BACKUP_DIR/ragseo_${STAMP}.dump"
CONTENT_DEST="$BACKUP_DIR/content_${STAMP}.tar.gz"

# ---------------------------------------------------------------- database
log "dumping database -> $DB_DEST"
# `set +e` around the call so $? is the real exit status: inside `if ! cmd`, $?
# would be the status of the negation and always 0.
set +e
docker compose -f "$COMPOSE_FILE" exec -T db \
    pg_dump -U ragseo --format=custom ragseo > "$DB_DEST"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
    rm -f "$DB_DEST"
    fail "$rc"
fi

# A zero-byte dump means pg_dump produced nothing. Treat it as a failure, since
# a successful-looking empty backup is the worst outcome here.
if [ ! -s "$DB_DEST" ]; then
    rm -f "$DB_DEST"
    fail "empty pg_dump"
fi

# ------------------------------------------------------------ file content
# -C "$PROJECT_DIR" so the archive holds `doctrine/...` rather than absolute
# paths: extraction then lands in the right place for any PROJECT_DIR.
present=()
missing=()
for d in "${CONTENT_DIRS[@]}"; do
    if [ -d "$PROJECT_DIR/$d" ]; then present+=("$d"); else missing+=("$d"); fi
done

if [ "${#present[@]}" -eq 0 ]; then
    fail "no content directories found under $PROJECT_DIR"
fi

log "archiving content: ${present[*]}"
set +e
tar -czf "$CONTENT_DEST" -C "$PROJECT_DIR" "${present[@]}"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
    rm -f "$CONTENT_DEST"
    fail "$rc"
fi

if [ ! -s "$CONTENT_DEST" ]; then
    rm -f "$CONTENT_DEST"
    fail "empty content archive"
fi

# A tar that cannot be listed is not a backup. Cheap insurance against writing a
# truncated archive every night and only finding out when it is needed.
if ! tar -tzf "$CONTENT_DEST" >/dev/null 2>&1; then
    rm -f "$CONTENT_DEST"
    fail "content archive is not readable"
fi

file_count=$(tar -tzf "$CONTENT_DEST" | grep -c '/[^/]*$' || true)

# ----------------------------------------------------------------- off-box
if [ -n "$OFFBOX_CMD" ]; then
    if bash -c "$OFFBOX_CMD \"$BACKUP_DIR\"" >> "$BACKUP_DIR/offbox.log" 2>&1; then
        log "offbox copy ok: $OFFBOX_CMD"
    else
        echo "OFFBOX COPY FAILED $(date -Iseconds) cmd=$OFFBOX_CMD" >> "$BACKUP_DIR/backup.log"
    fi
else
    echo "OFFBOX NOT CONFIGURED $(date -Iseconds) — backups are on the same host as the data; set OFFBOX_CMD to copy them off-box" >> "$BACKUP_DIR/backup.log"
fi

# --------------------------------------------------------------- retention
find "$BACKUP_DIR" -maxdepth 1 -name 'ragseo_*.dump'     -mtime "+$KEEP_DAYS" -delete
find "$BACKUP_DIR" -maxdepth 1 -name 'content_*.tar.gz'  -mtime "+$KEEP_DAYS" -delete

log "ok $(date -Iseconds) $(basename "$DB_DEST") $(wc -c < "$DB_DEST") bytes | $(basename "$CONTENT_DEST") $(wc -c < "$CONTENT_DEST") bytes, $file_count files"
if [ "${#missing[@]}" -gt 0 ]; then
    log "note: not present, not archived: ${missing[*]}"
fi
echo "ok $(date -Iseconds) $(basename "$DB_DEST") $(wc -c < "$DB_DEST") bytes | $(basename "$CONTENT_DEST") $(wc -c < "$CONTENT_DEST") bytes, $file_count files${missing:+ (missing: ${missing[*]})}" \
    >> "$BACKUP_DIR/backup.log"
