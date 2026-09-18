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
- **⚠️ Baseline purged 2026-09-14**: the baked seed was removed from `backend/external` (empty dir kept via `.gitkeep`; scanners skip dotfiles) and all **53 imported exports + detail rows were wiped** from prod. Status now zeroes out; every file listed on `/exports` is a user upload and deletable. To re-bake a baseline later: run `cd backend && ./scripts/sync_doctrine.sh`, commit `backend/external/`, rebuild image, then `RUN_EXTERNAL=1 up` on an empty DB.

## Weekly Import SOP (standard operating procedure)
Full runnable prompts: **`WEEKLY_GSC_IMPORT_PROMPT.md`** (master) + **`prompts/01..05`** (per-step), all addressed to a coding agent.
- **Upload via website (regular users)**: log in → **Weekly Exports** `/exports` → select files → **Upload & Import**. Backend `POST /api/ingest/external/upload` saves to writable `external_upload_path` (`/app/uploads/external`, bind-mounted to `./external_uploads`) and imports immediately; any logged-in user (writer/admin). Per-file error isolation, basename-sanitized filenames, 200 MB/file cap, hash-deduped.
- **Ops/admin offline flow** (or to refresh baked seed folder):
1. Copy fresh exports → `09042026/` (same filename format).
2. `cd backend && ./scripts/sync_doctrine.sh` (mirrors weekly folder → `backend/external/`, doctrine → `backend/doctrine/`; baked content is now git-tracked, so commit the staged copy).
3. Deploy via **git** (repo = private `github.com/rlpalomo25/ragseo-platform`): commit + `git push origin main` locally, then on the VPS `cd /opt/ragseo-platform && git pull origin main && docker compose -f docker-compose.prod.yml build backend frontend && docker compose -f docker-compose.prod.yml up -d` (VPS uses a read-only GitHub **deploy key**; `.env`/`external_uploads` are gitignored and survive pulls). Full steps: `prompts/03-push-redeploy.md`.
   - ⚠️ Never push the local dev `.env` — it's gitignored; the rsync-era incident where a bare `rsync ./` clobbered prod `.env` (DB_PASSWORD change → db recreated → backend/worker crash-loop `password authentication failed`) is now impossible. Real prod values live in the VPS `.env`; reference copy `/tmp/opencode/server.env`.
4. Import: first boot auto-runs via `RUN_EXTERNAL=1` (`docker-compose.prod.yml:64-68`); subsequent weeks → admin `POST /api/ingest/external` (auth required). Verify with `GET /api/ingest/external/status`; expect imported=files, skipped=dups, err=0.
Theme: `external_status`/`import_external` scan BOTH baked `/app/external` and upload dir (deduped by hash); uploaded files show under status. Status/import GET+POST remain admin-only; **upload AND delete are writer-open** (`require_writer`). Delete (`DELETE /api/ingest/external/delete`, writer) removes upload-dir files + their DB rows (cascades detail rows explicitly, DB-agnostic); baked files are flagged `deletable: false` and always refused.
Notes: importer is in-memory `zipfile` (no `unzip` binary); hash-dedup skips duplicates regardless of name; forced reload via `python scripts/import_external.py --path ... --force`.

## Audit fixes, wave 1 (2026-09-15, in code, not deployed)
- **Brand keys are canonical**: `mastershield` / `kleangutter` / `mmgg`. `detect_brand` returns `kleangutter`
  (was `klean_gutter`) for all Klean spellings incl. underscore; `BRAND_CONFIG` updated. Fixes Klean jobs
  having NO market context (`DOMAIN_FOR_BRAND` only knew `kleangutter`). See `backend/app/services/doctrine.py`.
- **`retrieval.py`**: `IN :doc_numbers` now uses `bindparam(..., expanding=True)` (raw tuple silently failed →
  applicable-docs context empty). Keyword SQL switched `ILIKE` → `lower()/LIKE` (dialect-agnostic; Postgres+SQLite).
- **Delete endpoint** (`routers/ingest.py`): baked-name files hard-rejected (never unlink/delete, even same-named upload copy);
  baked rows additionally protected when hash-matched from a differently-named upload. Policy: uploads = shared team folder,
  any writer/admin may delete. Status/import still admin-only; upload+delete writer-open.
- **`/docs/[docId]`** uses `useParams` (React 18/Next 14) — no React 19 `use()`.
- **Test-zip determinism**: `make_gsc_zip`/`make_ai_zip` pin `ZipInfo(date_time=FIXED)` — zipfile embeds wall-clock time by
  default, which made SHA-256 (and thus hash-dedup/skip assertions) flaky across second boundaries. Keep fixed timestamps.
- Tests: **154 passed** (added `tests/test_retrieval.py`, `tests/test_doctrine.py`, +2 delete-guard tests). Session: `CONTEXT-2026-09-15.md`.

## Audit fixes, wave 1b (Fix 6 — decompression limits, DONE)
Another agent attempted fixes 5–8 into the working tree (uncommitted), but Fix 6 was
**broken**: `_read_zip` referenced `_ZipBudget`/`ZipBudgetError`/`MAX_ZIP_*` that were never
defined → every external import died with `NameError` (swallowed per-file) → 9 test failures.
Now implemented + green:
- `backend/app/services/external_ingest.py`: `ZipBudgetError(ValueError)` (per-file isolation
  treats it as a skippable import error), `_ZipBudget` (`check_entry` pre-flights declared
  `ZipInfo.file_size` before read; `spend_entry(len(payload))` accounts actual bytes against
  per-entry / entry-count / total-expansion caps). Constants: `MAX_ZIP_ENTRIES=2000`,
  `MAX_ZIP_EXPANDED_BYTES=512 MB`, `MAX_ZIP_ENTRY_BYTES=100 MB`, `MAX_ZIP_DEPTH=5`.
- +8 tests in `backend/tests/test_external_ingest.py` (budget units + `_read_zip` integration
  w/ monkeypatched caps: oversized entry, too many entries, deep nesting, nested-zip unwrap,
  ValueError subclass). **Full suite: 163 passed** (was 146 pass / 9 fail).
- ⚠️ **Fix 7 in the same wave is still BROKEN — re-verified 2026-09-15, work started** (see Next Move):
  `tasks.py:10` imports `reconcile_doctrine` from `app.services.doc_ingestion`; `tasks.py:49-50`
  defines task `reconcile_doctrine` that **shadows** it → line 54 `reconcile_doctrine(db)` self-calls
  the task → TypeError on every scheduled run (real service is `doc_ingestion.reconcile_doctrine`,
  `doc_ingestion.py:229`). Beat entry (`celery_app.py:35`) names task `app.tasks.reconcile_doctrine`
  but it's registered as `doctrine.reconcile` → beat dispatch fails. Current code re-read this
  session; nothing fixed yet. `ingest_all_docs` (`doc_ingestion.py:113`) supersede-order quirk may
  supersede BOTH rows of a duplicate `doc_number` on timestamp ties — verify with a test.

## Next Move
1. **Audit fixes 1–4 + 6 DONE (2026-09-15, in code, NOT deployed/committed)**: `/docs/[docId]` React-18 fix; delete-endpoint baked-file hard-guard (+hash-row protection); `retrieval.py` `expanding=True` bind + `lower()/LIKE` (no ILIKE); Klean brand normalized `klean_gutter`→`kleangutter`; **Fix 6 zip-decompression budgets** (`ZipBudgetError`/`_ZipBudget`/`MAX_ZIP_*`, `spend_entry(len(payload))`). **163 backend tests pass; frontend tsc+lint clean.** Session notes: `CONTEXT-2026-09-15.md`.
2. **Fix 5, 7, 8 in working tree but UNVERIFIED / partly broken — review before deploy**:
   - Fix 5 (LLM retry + job idempotency): code present (retry/timeout in `llm_client.py`, idempotent `advance_job`, `uq_job_stages_job_sequence`) — but the stale-`running` sweeper is still missing.
   - Fix 7 (doctrine freshness): **BROKEN — work started, not fixed** — `tasks.py:50` `reconcile_doctrine` shadows the `doc_ingestion`
     import (line 54 self-calls → TypeError); beat entry `celery_app.py:35` points at `app.tasks.reconcile_doctrine` ≠ registered
     `doctrine.reconcile`. Migration `0006` (unique `doc_number`, newest-wins supersede) + `doc_ingestion.reconcile_doctrine()` + `last_updated` stamping look sound.
   - Fix 8 (login throttle + session pruning): code present (auth.py backoff, user fields, migration `0007`, `prune_expired_sessions`) — beat never schedules `prune_sessions_task`.
3. **Deploy fixes to VPS**: commit + `git push origin main`, VPS `git pull origin main && docker compose -f docker-compose.prod.yml build backend frontend && docker compose -f docker-compose.prod.yml up -d` (per `prompts/03-push-redeploy.md`).
4. Weekly routine: use WEEKLY_GSC_IMPORT_PROMPT.md + prompts/01-04 (website upload primary).
5. Optional future: Doc 307 dedicated SERP agent via `app/tasks.py:AGENT_FUNCTIONS`.

## Relevant Files
- Importer: `backend/app/services/external_ingest.py` · service: `backend/app/services/external_data.py` · models: `backend/app/models/external.py` · migration: `backend/alembic/versions/0004_external_data.py` · router: `backend/app/routers/ingest.py` · CLI: `backend/scripts/import_external.py` · agents: `backend/app/services/agents/{writer,router}.py`
- Upload: `POST /api/ingest/external/upload` in `backend/app/routers/ingest.py` (writes `external_upload_path`); delete: `DELETE /api/ingest/external/delete` (same module, `delete_external_export` in `backend/app/services/external_ingest.py`). UI `frontend/src/components/ingest/ExternalDataCard.tsx` (upload form + per-row/bulk delete), page `frontend/src/app/exports/page.tsx`, hook `frontend/src/lib/hooks/useIngest.ts` (`uploadExternalFiles`, `deleteExternalFiles`), helper `frontend/src/lib/api.ts` (`apiUpload`). Mount `./external_uploads:/app/uploads/external` in both compose files (dev backend+worker, prod backend). Needs `python-multipart`.
- Config/mount: `backend/app/config.py` (`external_data_path`, `external_upload_path`), `frontend/../docker-compose.yml` (backend+worker `./09042026:/app/external:ro` + `./external_uploads:/app/uploads/external`)
- Tests: `backend/tests/test_external_ingest.py` (19 tests incl. upload + delete API), `backend/tests/conftest.py` (ALL_TABLES + imports)
- Frontend: `frontend/src/app/ingest/page.tsx` (ExternalDataCard), `frontend/src/types/ingest.ts`, `frontend/src/lib/hooks/useIngest.ts`