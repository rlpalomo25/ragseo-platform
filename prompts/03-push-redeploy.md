# Prompt 3 — Deploy via Git (push → pull → rebuild)

Deployment is git-driven: commit on the dev machine, push to GitHub, then pull
+ rebuild on the VPS. No rsync needed — the VPS is a git checkout of the private
repo, and `.env` / `external_uploads` / build artifacts are gitignored, so a
pull can never clobber prod secrets (the old rsync `.env` incident is
impossible by construction).

## On the dev machine

```
cd /home/roberto/RAGv2/ragseo-platform
git add -A
git commit -m "what changed"
git push origin main
```

## On the VPS (root@157.230.2.51, path `/opt/ragseo-platform`)

```
cd /opt/ragseo-platform
git pull origin main
docker compose -f docker-compose.prod.yml build backend celery-worker frontend
docker compose -f docker-compose.prod.yml up -d
```

Wait for the backend container to become healthy before continuing.

`celery-worker` is a **required** build target, not an optional one. It shares the
`ragseo-backend:local` tag with `backend`, so listing both keeps the API and the
worker on the same app code; omitting it risks a split-brain where the worker runs
a stale `app/services/orchestrator.py`. Verify convergence after the deploy:

```bash
docker compose -f docker-compose.prod.yml ps
docker inspect -f '{{.Image}}' ragseo-platform-backend-1 ragseo-platform-celery-worker-1
```

Both image IDs must match.

## Backups (once per host — not per deploy)

The database alone is not the recoverable state. `scripts/backup_db.sh` archives
the `pg_dump` **plus** `doctrine/`, `doctrine_uploads/` and `external_uploads/`;
losing the host without those files loses uploaded doctrine permanently, because
nothing else holds those bytes.

Nothing invokes the script automatically. Install it once, on the VPS:

```bash
mkdir -p /opt/ragseo-platform/backups   # the log redirect below needs it to exist first
# prove it works BEFORE scheduling it:
PATH=/usr/local/bin:/usr/bin:/bin /opt/ragseo-platform/scripts/backup_db.sh
tail -3 /opt/ragseo-platform/backups/backup.log
ls -la /opt/ragseo-platform/backups

crontab -e   # then add:
15 2 * * * PATH=/usr/local/bin:/usr/bin:/bin /opt/ragseo-platform/scripts/backup_db.sh >> /opt/ragseo-platform/backups/backup.log 2>&1
```

- Set `PATH` explicitly: cron runs with a minimal environment and `docker` is
  often not on the default path, which fails the run in a way that only shows up
  as an empty log.
- The run line carries the off-box verdict — `OFFBOX NOT CONFIGURED`,
  `offbox ok`, or `OFFBOX COPY FAILED`. **Unset means the backups are on the same
  disk as the data they protect.** To copy off-host, set `OFFBOX_CMD` in the
  crontab and reference the backup dir as `"$1"`, e.g.
  `OFFBOX_CMD='rclone copy "$1" gdrive:ragseo'`.
- Recovery, no rebuild needed: `scripts/restore_doctrine.sh`.

## Smoke test

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://157.230.2.51/api/health          # 200
curl -s http://157.230.2.51/openapi.json | grep -oE '"/api/ingest/external/(upload|delete)"'
curl -s -o /dev/null -w "%{http_code}\n" -L http://157.230.2.51/exports          # 200
# routes protected as writer-only?
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE http://157.230.2.51/api/ingest/external/delete   # 401
# /docs must reach the frontend (Doctrine Reference), NOT FastAPI's Swagger UI.
# Caddy `handle` blocks are first-match-wins, so a /docs route pointing at the
# backend silently shadows the whole Doctrine section.
curl -s -o /dev/null -w "%{http_code}\n" http://157.230.2.51/docs                  # 200
curl -s http://157.230.2.51/docs | grep -q "swagger-ui" && echo "REGRESSION: /docs is Swagger, not Doctrine"
curl -s -o /dev/null -w "%{http_code}\n" http://157.230.2.51/api/meta/docs        # 200 (Swagger moved here)
```

`docker compose -f docker-compose.prod.yml up -d` restarts Caddy only if its
config changed. Caddy refuses to start on a malformed config, so a bad edit
takes the site down entirely — validate first:

```bash
docker compose -f docker-compose.prod.yml exec caddy caddy validate --config /etc/caddy/Caddyfile
```

<details>
<summary>Details for the operator</summary>

- Repo: private `github.com/rlpalomo25/ragseo-platform` (branch `main`).
- VPS auth: read-only **deploy key** at `/root/.ssh/id_ed25519_ragseo` (pubkey
  registered in repo → Settings → Deploy keys); `/root/.ssh/config` forces
  `Host github.com` to that key (`IdentitiesOnly yes`). No PATs involved.
- `git pull` runs as root; the repo at `/opt` was tuned with
  `git config --global --add safe.directory /opt/ragseo-platform`.
- `.env` on the VPS holds real prod secrets and is **untracked** — git never
  touches it. If a fresh server needs it, copy it from another host you trust
  (values are `DB_PASSWORD`, `SECRET_KEY`, `SESSION_SECRET`, the Voyage/OpenAI
  keys, and prod overrides of `DOCTRINE_*` / `*_UPLOAD_PATH`); then `up -d`.
  **Never** rsync the local dev `.env`. The old reference copy at
  `/tmp/opencode/server.env` is **gone** — that path no longer holds anything.
- `external_uploads/` (user uploads) and `frontend/node_modules|.next` are
  untracked and persist across pulls.
- Baked content (`backend/doctrine`, `backend/external`) is now **tracked**, so
  a fresh clone builds self-contained. The raw weekly dump `09042026/` stays out
  of git; to refresh the baked seed run `cd backend && ./scripts/sync_doctrine.sh`
  then commit the resulting `backend/external` + `backend/doctrine` changes.
- Rebuild `backend` **and** `celery-worker` when requirements/app code changes
  (e.g. `python-multipart`, new routes). Both build the same `./backend` context
  and share the `ragseo-backend:local` tag, so they always run identical code.
- Rebuild `frontend` on any UI/pages change — prod frontend has no bind mount.
- `up -d` applies changes idempotently; unchanged services keep running.
- Add `sudo` to the docker commands if the VPS docker context needs elevation.
</details>