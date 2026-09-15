# Project Memory — RAGSEO Platform

## Objective
Ingest weekly external market data (GSC/GA4/Ubersuggest/calls/leads from `09042026/`) idempotently, and wire it into agent decision-making (SERP + Router/Writer data context). **Built and validated end-to-end (session completed 2026-09-10).**

## Important Details
- Data: **`/home/roberto/RAGv2/ragseo-platform/09042026/`** (56 files, period Aug 28–Sep 3/4 2026). Contains **3 byte-identical duplicate pairs** under different names (verified by sha256); hash-dedup correctly skips them.
- Importer runs **in-memory via Python `zipfile`** (no `unzip` binary); GSC `.csv.zip.zip` are single-level zips (test fixture built nested to prove recursion).
- Deployment: frontend is a Docker `next-server` **prod build, no bind mount → rebuild container per UI change**. Backend + celery-worker bind-mount `./backend/app:/app/app:ro` → deploy via `up -d`. DB: pgvector Postgres via compose.
- Alembic chain: 0001_baseline → 0002_jobs → 0003_local_embeddings → **0004_external_data**. Conftest `ALL_TABLES` now includes external tables (sqlite fixture creates them).
- Test runner: `cd backend && PYTHONPATH=/tmp/opencode/ragseo-deps python3 -m pytest` → **130 passed** (was 121; +9 external tests). Frontend: lint clean, build clean (11 routes, `/ingest` 5.2 kB).
- Compose mount for backend + worker: `./09042026:/app/external:ro`; `settings.external_data_path=/app/external`.
- Writer provenance contract kept intact: market data exposed via new `market_sources` key (NOT `provenance`) to preserve `{"100":..,"130":..,"316":..,"316-C":..}` assertion.

## External-data build (completed)
- **Models + migration**: `backend/app/models/external.py` + `backend/alembic/versions/0004_external_data.py` — `external_exports` (registry, `file_hash` unique), `search_console_dim`, `search_console_daily`, `ai_overview_impressions`, `keyword_estimate`, `backlink`, `top_page`, `call_tracking`, `lead_summary`, `ga4_event`, `domain_report`, `domain_metric`. Registered in `models/__init__.py`.
- **Importer** `app/services/external_ingest.py`: `classify()` (10 types incl. messy names/renamed dups, header-sniff for `_KBT`/`ubersuggest`), parsers, `DOMAIN_ALIASES`+`BRAND_DOMAINS` (kleangutter/mastershield/mmgg; rest = competitors), duration/percent/MDY/MDDD coercers, per-file transactions, `import_external_folder(db, path, force)`. `_read_zip` recursively unwraps nested archives (probe, not extension).
- **API** `app/routers/ingest.py`: `GET /api/ingest/external/status`, `POST /api/ingest/external` (admin). Verified 401/403 + flow in tests.
- **Agent wiring**: `app/services/external_data.py` `build_market_context(db, brand)` → GSC queries/AI-impressions/GA4/calls/leads/backlink-health/top-pages/competitor snapshot. Injected into `app/services/agents/writer.py` (`## Supporting Market Data` block, `market_sources`), `app/services/agents/router.py` (pre-brand context). NOTE: scalar queries use `.scalar()` not `.first()`; Row access via `kw[1]` tuple index.
- **CLI**: `backend/scripts/import_external.py` (`--path`, `--force`).
- **Frontend**: External market data card on `/ingest` (tiles: exports/imported/errors/rows; import button; per-file table w/ type labels) — `frontend/src/types/ingest.ts` ext + `frontend/src/lib/hooks/useIngest.ts` hooks.
- **Live validation**: real folder → **56 files: 53 imported, 3 skipped (dups), 0 errors**; rows by type: search_console 16,875 · keyword_estimate 17,397 · top_page 13,050 · backlink 19,646 (+78 metrics) · calls 375 · GA4 210 · ai_overview 1,155 · leads 12 · traffic reports 55.
  (Skipped rows shown = full counts of the originals: 270/2250/3000.)

## Weekly Import SOP (standard operating procedure)
Full runnable prompts: **`WEEKLY_GSC_IMPORT_PROMPT.md`** (master) + **`prompts/01..05`** (per-step), all addressed to a coding agent.
- **Upload via website (regular users)**: log in → **Weekly Exports** `/exports` → select files → **Upload & Import**. Backend `POST /api/ingest/external/upload` saves to writable `external_upload_path` (`/app/uploads/external`, bind-mounted to `./external_uploads`) and imports immediately; any logged-in user (writer/admin). Per-file error isolation, basename-sanitized filenames, 200 MB/file cap, hash-deduped.
- **Ops/admin offline flow** (or to refresh baked seed folder):
1. Copy fresh exports → `09042026/` (same filename format).
2. `cd backend && ./scripts/sync_doctrine.sh` (mirrors weekly folder → `backend/external/`, doctrine → `backend/doctrine/`; runs before any backend image build).
3. `rsync -a /home/roberto/RAGv2/ragseo-platform/ root@157.230.2.51:/opt/ragseo-platform/ --exclude frontend/node_modules --exclude frontend/.next --exclude external_uploads --exclude .env` then `cd /opt/ragseo-platform && docker compose -f docker-compose.prod.yml build backend && docker compose -f docker-compose.prod.yml up -d`.
   - ⚠️ Never push the local dev `.env` (root `.env` = dev values). Once clobbered it changed DB_PASSWORD on the VPS → db recreated, backend/worker crash-loop `password authentication failed` (pgdata volume was NOT wiped; restoring the real prod `.env` + `up -d` fixes it).
4. Import: first boot auto-runs via `RUN_EXTERNAL=1` (`docker-compose.prod.yml:64-68`); subsequent weeks → admin `POST /api/ingest/external` (auth required). Verify with `GET /api/ingest/external/status`; expect imported=files, skipped=dups, err=0.
Theme: `external_status`/`import_external` scan BOTH baked `/app/external` and upload dir (deduped by hash); uploaded files show under status. Status/import GET+POST remain admin-only; only the upload endpoint is writer-open.
Notes: importer is in-memory `zipfile` (no `unzip` binary); hash-dedup skips duplicates regardless of name; forced reload via `python scripts/import_external.py --path ... --force`.

## Next Move
1. **Ship it**: `sudo docker compose -f docker-compose.yml build frontend && sudo docker compose -f docker-compose.yml up -d` (runs `alembic upgrade head` → 0004; mounts external folder; rebuilds stale frontend).
2. Verify `/api/ingest/external/status` 200 + run `POST /api/ingest/external` (imp: 53, skip: 3, err: 0) → `/ingest` shows imported tiles.
3. Weekly routine: use WEEKLY_GSC_IMPORT_PROMPT.md + prompts/01-04.
4. Optional future: Doc 307 dedicated SERP agent via `app/tasks.py:AGENT_FUNCTIONS`; `force` re-import path tested implicitly only.

## Relevant Files
- Importer: `backend/app/services/external_ingest.py` · service: `backend/app/services/external_data.py` · models: `backend/app/models/external.py` · migration: `backend/alembic/versions/0004_external_data.py` · router: `backend/app/routers/ingest.py` · CLI: `backend/scripts/import_external.py` · agents: `backend/app/services/agents/{writer,router}.py`
- Upload: `POST /api/ingest/external/upload` in `backend/app/routers/ingest.py` (writes `external_upload_path`), UI `frontend/src/components/ingest/ExternalDataCard.tsx` (upload form), page `frontend/src/app/exports/page.tsx`, hook `frontend/src/lib/hooks/useIngest.ts` (`uploadExternalFiles`), helper `frontend/src/lib/api.ts` (`apiUpload`). Mount `./external_uploads:/app/uploads/external` in both compose files (dev backend+worker, prod backend). Needs `python-multipart`.
- Config/mount: `backend/app/config.py` (`external_data_path`, `external_upload_path`), `frontend/../docker-compose.yml` (backend+worker `./09042026:/app/external:ro` + `./external_uploads:/app/uploads/external`)
- Tests: `backend/tests/test_external_ingest.py` (9 tests), `backend/tests/conftest.py` (ALL_TABLES + imports)
- Frontend: `frontend/src/app/ingest/page.tsx` (ExternalDataCard), `frontend/src/types/ingest.ts`, `frontend/src/lib/hooks/useIngest.ts`