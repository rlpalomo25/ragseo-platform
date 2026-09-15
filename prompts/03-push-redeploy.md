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
docker compose -f docker-compose.prod.yml build backend
docker compose -f docker-compose.prod.yml build frontend
docker compose -f docker-compose.prod.yml up -d
```

Wait for the backend container to become healthy before continuing.

## Smoke test

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://157.230.2.51/api/health          # 200
curl -s http://157.230.2.51/openapi.json | grep -oE '"/api/ingest/external/(upload|delete)"'
curl -s -o /dev/null -w "%{http_code}\n" -L http://157.230.2.51/exports          # 200
# routes protected as writer-only?
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE http://157.230.2.51/api/ingest/external/delete   # 401
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
  touches it. If a fresh server needs it, the reference copy is
  `/tmp/opencode/server.env` (on the dev machine); copy it, then `up -d`.
  **Never** rsync the local dev `.env`.
- `external_uploads/` (user uploads) and `frontend/node_modules|.next` are
  untracked and persist across pulls.
- Baked content (`backend/doctrine`, `backend/external`) is now **tracked**, so
  a fresh clone builds self-contained. The raw weekly dump `09042026/` stays out
  of git; to refresh the baked seed run `cd backend && ./scripts/sync_doctrine.sh`
  then commit the resulting `backend/external` + `backend/doctrine` changes.
- Rebuild `backend` when requirements/app code changes (e.g. `python-multipart`,
  new routes). `celery-worker` shares the `build: ./backend` recipe.
- Rebuild `frontend` on any UI/pages change — prod frontend has no bind mount.
- `up -d` applies changes idempotently; unchanged services keep running.
- Add `sudo` to the docker commands if the VPS docker context needs elevation.
</details>