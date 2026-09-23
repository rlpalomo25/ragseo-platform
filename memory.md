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

## Audit fixes, wave 2 — Fixes 5/7/8 COMPLETE (2026-09-18, in code, NOT deployed)
- **Fix 7 (doctrine freshness)**: `tasks.py` now aliases the service import
  (`reconcile_doctrine_service`) so the celery task body calls the real
  `doc_ingestion.reconcile_doctrine(db)` — the old shadowed self-call TypeError
  is gone. Beat entry renamed to the registered name `doctrine.reconcile`
  (was `app.tasks.reconcile_doctrine`, which never matched).
- **Fix 8 (login throttle)**: `auth.prune_sessions` now scheduled in
  `celery_app.py` beat (`session-prune`, every 6h at :30).
- **Fix 5 (LLM retry + idempotency)**:
  - `advance_job` guard 1 (redelivery no-op) is now precise: "completed" is a
    no-op only if the NEXT stage exists OR the auditor already moved the job
    off `running`. The old guard also swallowed the window where the worker
    died after `run_agent` committed "completed" but before advance landed →
    job stuck in `running` forever; that window is now resumed.
  - NEW `sweep_stale_tasks(db, stale_after=STALE_RUNNING_AFTER)` in
    `orchestrator.py`: reclaims AgentTasks stuck in `running` past 30 min
    (celery hard limit 900s), marks them failed, and routes via `advance_job`.
    Scheduled as `pipeline.sweep_stale` (every 5 min).
  - **Dupe doc_number quirk**: `uq_documents_doc_number` (migration 0006 +
    model) was a WHOLE-TABLE unique constraint — makes the supersede flow
    impossible (superseded rows legitimately keep their doc_number). Now a
    PARTIAL unique index on ACTIVE rows only (`uq_documents_doc_number_active`,
    dialect-branched in 0006, `Index(...sqlite_where/postgresql_where)` in
    `Document.__table_args__`). `ingest_all_docs` + `reconcile_doctrine` now
    supersede-and-flush BEFORE inserting the newer take; reconcile keeps its
    `db_by_number` cache current mid-scan (a doc created earlier in the same
    run must be visible to later files) and its missing-sweep no longer
    clobbers fresh "superseded" status. reconcile stats gained missing
    `chunks`/`embedding_failures` keys (`_rechunk_document` needs them).
- Tests: **173 passed** (was 163). +3 `test_tasks.py` (task glue + beat
  registration), +5 `test_orchestrator.py` (resume-windows + sweeper),
  +2 `test_doc_ingestion.py` (dupe number supersede, reconcile status).
  conftest gained an autouse `no_celery_broker` patch so the suite runs
  WITHOUT Redis (`create_job → run_agent_task.delay` used to hit the real
  broker). Test command: `DATABASE_URL=sqlite:///:memory: PYTHONPATH=/tmp/opencode/ragseo-deps python3 -m pytest` (psycopg2 not needed; 163 baseline reproduced).

## Code cleanup for GitHub sharing per "C++ Coding Standards: 101 Rules" (2026-09-18, DONE except frontend)
User asked: apply the 101-rule book (Sutter & Alexandrescu; summary at `https://micro-os-plus.github.io/develop/sutter-101/`) to the codebase for sharing/upload, and add a private paid-software license. Completed:
- **ruff 0.16.8** at `/tmp/opencode/ruff/bin/ruff`; config `backend/pyproject.toml` `[tool.ruff]` (target py311, line-length 110, select E/W/F/I/B/UP/SIM/C4/RUF, ignore B008/C901, per-file `tests/*` B018/RUF012, double-quote format). pytest config stays in `backend/pytest.ini` (no `[tool.pytest.ini_options]` in pyproject — dual-config conflict).
- `ruff check --fix` (205 fixed), `ruff format` (47 reformatted), then 25 manual fixes done this session: E712 `== True`→truthy (`auth.py:33`, `auth_service.py:93`), B904 `raise ... from e` (`ingest.py:204`, `jobs.py:154/170`), E741 ambiguous `l`→`lv`/`line` (`chunking.py`, `external_ingest.py`), RUF059 unused unpack (`auth.py` `_`; test `brand`→`_`), RUF046 `round(float(v))` (not `int(round())`), RUF001 en-dash→hyphen (`external_data.py` week label), RUF043 raw-string match (`test_agent_auditor.py`), B017 blind `Exception`→`pydantic.ValidationError` (`test_agent_writer.py`), F841 unused `by_name` (removed), E501 line-length on long prompt prose handled via file-level `# ruff: noqa: E501` in `app/services/agents/{auditor,router,writer}.py` (prompt text is deliberately long-form). Lint: **All checks passed**; format: **66 files already formatted**.
- **`frontend/tsconfig.tsbuildinfo` removed from git** (`git rm --cached`); `.gitignore` now excludes it + `frontend/.eslintcache`.
- **`LICENSE`** (root): PROPRIETARY SOFTWARE LICENSE AGREEMENT — paid/commercial, all-rights-reserved; no copy/modify/redistribute/reverse-engineer/sublicense; confidentiality; auto-termination on breach/non-payment; "AS IS"; note placeholders `[DATE]`/contact to fill before publishing. README gained a `## License` section.
- Secrets scan across tracked files: clean; defaults in code are `changeme`/`change-this` placeholders (`.env` gitignored).
- **Tests still green: 173 passed** (after all reformat/refactors).
- Frontend `tsc --noEmit` + `next lint`: NOT run — this env has no Node/npm and `node_modules` is absent. Run locally before pushing.

## Next Move
1. ✅ **DEPLOYED 2026-09-23**: pushed to `origin/main` (head `a176a9e`) via PAT and
   redeployed on the VPS — `docker compose -f docker-compose.prod.yml build backend frontend
   && up -d` ✅ **completed**. Smoke-tests pass: `/api/health` → 200, `/openapi.json`
   serves the full schema (new `/api/ingest/external/{upload,delete}` present; migrations
   0005–0008 ran on boot). VPS now runs `a176a9e`. (Writer-protected delete → 401 still
   needs an authed check; the endpoint is visible in openapi.)
2. Weekly routine: use WEEKLY_GSC_IMPORT_PROMPT.md + prompts/01-04 (website upload primary).
3. Optional future: Doc 307 SERP agent via `app/tasks.py:AGENT_FUNCTIONS`.
4. **Frontend still unverified (no Node here)**: before the next frontend
   deploy, run `cd frontend && npx tsc --noEmit && npm run lint` on a Node
   machine; optional DRY refactors still open (shared dashboard layout across the
   8 page shells, status-variant map consolidation, repeated Tailwind input class
   string, duplicated slugify + embedding-coverage bar).

## Open items captured this session (2026-09-19)
- **Best-practice cleanup committed `2738159`, working tree clean, NOT deployed.
  VPS still runs `2a8edf3`** (health verified 200 at session start). Cleanup done:
  `session_scope()` ctx manager (`app/database.py`, used by `tasks.py`),
  `latest_export_ids` made public & shared by `external_data`/`learning_loop`
  (killed the duplicate copy), `voyage_api_url` setting (SPOD), `print()`→logger,
  silent catches fixed (learning_loop, EditUserModal, logout), dead code removed
  (`get_doctrine_context`, `Toast.tsx`, `Modal.contentRef`), auth cookie
  `max_age` from `settings.session_expiry_hours`, alembic E501 per-file-ignored.
  Tests: **183 passed**; `ruff check` clean; `ruff format` 201 files.
- **Frontend has NO Node in this env** — all frontend edits were manual-review
  surgical only; `tsc --noEmit`/`next lint` must run locally before pushing the
  frontend image. Flagged refactors: shared dashboard layout (8 × duplicated
  AuthGuard+Sidebar+Header shell), status-variant maps, api.ts EXTRA DRY.
- **Rename ripple**: tests patch `tasks.session_scope` (was `tasks.SessionLocal`);
  `tests/test_external_data.py` imports `latest_export_ids`. Don't regress either.
- Deploy SOP is git-driven (private `github.com/rlpalomo25/ragseo-platform`, VPS
  read-only deploy key); never push dev `.env`. Prod values: `/tmp/opencode/server.env`.

## Relevant Files
- Importer: `backend/app/services/external_ingest.py` · service: `backend/app/services/external_data.py` · models: `backend/app/models/external.py` · migration: `backend/alembic/versions/0004_external_data.py` · router: `backend/app/routers/ingest.py` · CLI: `backend/scripts/import_external.py` · agents: `backend/app/services/agents/{writer,router}.py`
- Upload: `POST /api/ingest/external/upload` in `backend/app/routers/ingest.py` (writes `external_upload_path`); delete: `DELETE /api/ingest/external/delete` (same module, `delete_external_export` in `backend/app/services/external_ingest.py`). UI `frontend/src/components/ingest/ExternalDataCard.tsx` (upload form + per-row/bulk delete), page `frontend/src/app/exports/page.tsx`, hook `frontend/src/lib/hooks/useIngest.ts` (`uploadExternalFiles`, `deleteExternalFiles`), helper `frontend/src/lib/api.ts` (`apiUpload`). Mount `./external_uploads:/app/uploads/external` in both compose files (dev backend+worker, prod backend). Needs `python-multipart`.
- Config/mount: `backend/app/config.py` (`external_data_path`, `external_upload_path`), `frontend/../docker-compose.yml` (backend+worker `./09042026:/app/external:ro` + `./external_uploads:/app/uploads/external`)
- Tests: `backend/tests/test_external_ingest.py` (19 tests incl. upload + delete API), `backend/tests/conftest.py` (ALL_TABLES + imports)
- Frontend: `frontend/src/app/ingest/page.tsx` (ExternalDataCard), `frontend/src/types/ingest.ts`, `frontend/src/lib/hooks/useIngest.ts`