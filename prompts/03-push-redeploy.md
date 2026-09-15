# Prompt 3 — Push, Rebuild, Redeploy

Push the repo to the VPS, rebuild images, and redeploy:

```
rsync -a /home/roberto/RAGv2/ragseo-platform/ root@157.230.2.51:/opt/ragseo-platform/ \
  --exclude frontend/node_modules --exclude frontend/.next \
  --exclude external_uploads --exclude .env
```

> **WARNING: never push the local dev `.env`.** The repo root has `.env` with
> local-dev values; rsyncing it over `/opt/ragseo-platform/.env` changes
> `DB_PASSWORD`/`SECRET_KEY`/`ANTHROPIC_API_KEY` on the VPS, recreates the db
> container, and crash-loops backend/worker on "password authentication
> failed". Always rsync with `--exclude .env`.

```
cd /opt/ragseo-platform && docker compose -f docker-compose.prod.yml build backend && docker compose -f docker-compose.prod.yml up -d
```

Also rebuild the frontend (it has no live bind-mount in prod, and this repo
adds the user-facing `/exports` upload page):

```
cd /opt/ragseo-platform && docker compose -f docker-compose.prod.yml build frontend && docker compose -f docker-compose.prod.yml up -d
```

Wait for the backend container to become healthy before continuing.

<details>
<summary>Details for the operator</summary>

- Add `sudo` to the `docker compose` command if your VPS docker context requires
  elevation (e.g. `sudo docker compose -f ... build backend && sudo docker compose -f ... up -d`).
- When to rebuild `backend`: requirements.txt / app code changed (e.g. the
  `python-multipart` upload dependency and the `/api/ingest/external/upload`
  route). `celery-worker` shares the same `build: ./backend` recipe.
- When to rebuild `frontend`: any UI/pages change (e.g. the new `/exports`
  Weekly Exports page) — the prod frontend has no bind mount, so a rebuild is
  mandatory.
- The `./external_uploads` bind mount is auto-created by Docker on first
  `up -d`; it must be writable for the upload endpoint.
- `up -d` applies changes idempotently; unchanged services are left running.
</details>