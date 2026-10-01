# Project Memory — RAGSEO Platform

## Objective
Ingest weekly external market data (GSC/GA4/Ubersuggest/calls/leads from `09042026/`) idempotently, and wire it into agent decision-making (SERP + Router/Writer data context). **Built and validated end-to-end (session completed 2026-09-10).**

## Important Details
- Data: **`/home/roberto/RAGv2/ragseo-platform/09042026/`** (56 files, period Aug 28–Sep 3/4 2026). Contains **3 byte-identical duplicate pairs** under different names (verified by sha256); hash-dedup correctly skips them.
- Importer runs **in-memory via Python `zipfile`** (no `unzip` binary); GSC `.csv.zip.zip` are single-level zips (test fixture built nested to prove recursion).
- Deployment: frontend is a Docker `next-server` **prod build, no bind mount → rebuild container per UI change**. Backend + celery-worker bind-mount `./backend/app:/app/app:ro` → deploy via `up -d`. DB: pgvector Postgres via compose. Migrations auto-apply on container start via `backend/docker-entrypoint.sh` (`python scripts/migrate.py`) — no manual alembic step. Full current-state notes: "Deployed state" below + `CONTEXT-2026-09-30.md`. ⚠️ `up -d` never rebuilds — see the gotcha section.
- Alembic chain (current head **0010**): 0001_baseline → 0002_jobs → 0003_local_embeddings → 0004_external_data → 0005_job_stage_idempotency → 0006_doc_number_unique → 0007_login_throttle → 0008_learning_loop → 0009_user_soft_delete → 0010_audit_logs. Conftest `ALL_TABLES` includes external + audit tables (sqlite fixture creates them).
- Tests: last green run was **204 passed / 2 failed** (both failures are the known stale-image baked-files issue, not code). ⚠️ **Not currently runnable on this host** — the `PYTHONPATH=/tmp/opencode/ragseo-deps` venv and `ruff/bin/ruff` were wiped from `/tmp/opencode`; rebuild the image and run via `docker compose exec backend python -m pytest -m "not integration"` (dev bind-mounts `app/` but **not** `tests/`). Frontend gate = `docker build ./frontend` (lint + types).
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
3. Deploy via **git** (repo = private `github.com/rlpalomo25/ragseo-platform`): commit + `git push origin main` locally, then on the VPS `cd /opt/ragseo-platform && git pull origin main && docker compose -f docker-compose.prod.yml build backend celery-worker frontend && docker compose -f docker-compose.prod.yml up -d` (VPS uses a read-only GitHub **deploy key**; `.env`/`external_uploads` are gitignored and survive pulls). Full steps: `prompts/03-push-redeploy.md`.
   - ⚠️ Never push the local dev `.env` — it's gitignored; the rsync-era incident where a bare `rsync ./` clobbered prod `.env` (DB_PASSWORD change → db recreated → backend/worker crash-loop `password authentication failed`) is now impossible. Real prod values live in the VPS `.env`; reference copy `/tmp/opencode/server.env`.
4. Import: first boot auto-runs via `RUN_EXTERNAL=1` (`docker-compose.prod.yml:64-68`); subsequent weeks → admin `POST /api/ingest/external` (auth required). Verify with `GET /api/ingest/external/status`; expect imported=files, skipped=dups, err=0.
Theme: `external_status`/`import_external` scan BOTH baked `/app/external` and upload dir (deduped by hash); uploaded files show under status. Status/import GET+POST remain admin-only; **upload AND delete are writer-open** (`require_writer`). Delete (`DELETE /api/ingest/external/delete`, writer) removes upload-dir files + their DB rows (cascades detail rows explicitly, DB-agnostic); baked files are flagged `deletable: false` and always refused.
Notes: importer is in-memory `zipfile` (no `unzip` binary); hash-dedup skips duplicates regardless of name; forced reload via `python scripts/import_external.py --path ... --force`.

## Audit fixes, wave 1 (2026-09-15, in code — DEPLOYED as of 2026-09-30)
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

## Audit fixes, wave 2 — Fixes 5/7/8 COMPLETE (2026-09-18, in code — DEPLOYED as of 2026-09-30)
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

## TSR refactor wave — soft-delete, RBAC audit, retry, dark mode (2026-09-23)
Objective: implement the TSR (landing page Tailwind, RBAC audit, vector, user soft-delete) with risk gates.
Scope decisions: **vector/HNSW SKIPPED** (keep `vector(768)` + `ix_doc_chunks_embedding_hnsw`); partial unique index on **username** (no email column); Doctrine gating = harden existing (`/docs` stays writer-open, `/ingest` admin-only) + backend 403 audit; **added a real retry endpoint** with in-flight guard; dark mode = app-coherent.
- **GATE-1 PASSED**: global soft-delete filter in `app/database.py` — `do_orm_execute` listener + `with_loader_criteria(User, deleted_at IS NULL, include_aliases=True)`; bypass via `disable_soft_delete_filter()` contextvar; deferred User import (circular-import safe). Works on legacy `db.query()`. `.query().get()` path unused (removed in cleanup wave).
- **`models/user.py`**: `deleted_at` column; username no longer `unique`; `__table_args__` = `uq_users_username_active` (dialect-branched partial unique, pattern from 0006) + `ix_users_deleted_at`. Migration **`0009_user_soft_delete`** (add col → drop `ix_users_username` → partial unique → deleted_at index; symmetric downgrade). Head chain: 0008 → **0009** → **0010_audit_logs**.
- **Audit**: `models/audit.py` (AuditLog), `services/audit.py` (`log_audit`, commits), `routers/audit.py` (`GET /api/audit`, admin), migration `0010_audit_logs`; registered in `models/__init__.py`, `main.py`, conftest `ALL_TABLES`. `dependencies.py` `require_admin`/`require_writer` now take `request` + `db` and write an `access_denied` row on 403; **anonymous 401s are NOT audited** (test asserts).
- **Users router**: `user_id: UUID` (was `str` → pre-existing bug `'str' object has no attribute 'hex'`, same pattern as jobs.py); DELETE = soft-delete (`deleted_at`+`is_active=False`+revoke all sessions, `synchronize_session="fetch"`) + audit `user.delete`; new `POST /api/users/{user_id}/restore` (audited, 404 unless deleted). Soft-deleted usernames re-creatable (partial unique). `schemas/user.py` + `UserResponse.deleted_at`.
- **Retry (Phase 3)**: `retry_job(db, job)` in `services/orchestrator.py` — only `failed`/`cancelled`; **in-flight guard** (any linked AgentTask still `running` → 409, refuses double-dispatch after sweeper-zombie races); prior failed stages → `skipped` (rows preserved); reset `status=running`, `revision_count=0`, `notes=None`; re-dispatch router at `max(sequence)+1`. Route `POST /api/jobs/{id}/retry` in `routers/jobs.py` (writer, 404/409). **GATE-2 PASSED**: `advance_job` failed-task branch now no-ops if a newer stage exists (stale crash-window resume can't re-fail a retried job).
- **Stats `system` block** (`routers/stats.py` + `types/stats.ts`): `active_users` (unexpired Session.user_id distinct — sqlite compares tz-aware ISO strings fine), `queued_jobs` (`running`), `avg_latency_seconds` (**completed-only** tasks), `health` (degraded if failed_stages>0 or latency>300s; warning if chunk coverage<1; else healthy).
- **Frontend (Phase 4)**: `tailwind.config.ts` `darkMode:"class"`; new `src/lib/hooks/useTheme.ts` (localStorage only inside `useEffect` → no hydration mismatch); Header toggle (sun/moon) + dark shell (layout body, Sidebar, Header); `dark:` variants on Card/Badge/Button/Input/Modal; landing `DashboardContent.tsx` rewritten: `gap-6` 4-tile metrics grid (Documents, Chunks indexed w/ CoverageBar, Awaiting review, Avg agent latency), SystemHealth strip (badge + active users + queued jobs + degraded message), **Recent Jobs grid** (`useJobs({ limit: 6 })`, `grid-cols-1 xl:grid-cols-2 gap-6`) with **View Logs → `/jobs/[id]`** and **Retry** on failed/cancelled. `useJobs` gained `limit` param; `jobAction` supports `"retry"`; Retry buttons on `/jobs` list + detail; admin users page: **Deactivate** (soft-delete w/ `window.confirm`) / **Restore** + Deleted badge. `JobSummary`/`User` types extended.
- **Tests**: `tests/test_soft_delete.py` (8), `tests/test_rbac.py` (5 — incl. **403 rows are audited, 401s are not**), retry + GATE-2 + stats-system tests. Full suite on this wave: **204 passed, 2 failed**. Both failures are `tests/test_external_ingest.py` (upload-status file counts) and are **pre-existing, not from this wave** — verified by re-running them with the whole wave stashed (identical 2 failures on clean HEAD). Cause: the locally running container image is **stale** (built before the 2026-09-14 external-baseline purge), so it still carries 56 baked files in `/app/external` while the repo's `backend/external` is empty and the tests assert the post-purge count of 0. Rebuild the image to clear them. `ruff check` clean; `ruff format` applied to 3 new/modified files (`routers/stats.py`, `services/orchestrator.py`, `tests/test_soft_delete.py`).
- **Post-review fixes applied before commit**: (1) `routers/users.py` `delete_user` had lost its explicit `db.commit()` and persisted only as a side effect of `log_audit`'s internal commit — restored an explicit `db.commit()` *after* the `log_audit` call, mirroring `restore_user` in the same file; this keeps the action + audit row atomic while removing the hidden coupling (had it been placed *before* `log_audit`, a crash in between would delete a user with no audit entry). (2) `useTheme.ts` read localStorage in a `useEffect` that ran *after* the write-effect's first pass, clobbering a stored `"dark"` back to `"light"` and flashing dark-mode users; replaced with a lazy `useState` initializer behind a `typeof window === "undefined"` guard.
- **Frontend verified via `docker build ./frontend`** — no Node/npm on this host, so `tsc --noEmit`/`npm run lint` still cannot run directly here (standing caveat below), but `next build` (which fails on TS errors) completed, so the frontend type-checks inside the image.

## HANDOFF — outstanding fixes (verified 2026-10-01)
Read this first when resuming, especially **on a different machine**. Every line
reference below was re-read in the code on 2026-10-01, not copied from memory.

> ⚠️ **`CONTEXT-*.md` is gitignored** (`.gitignore:29` — session notes carry live prod
> passwords), so the `CONTEXT-*` files do **not** exist on a fresh clone. This section
> is the tracked, portable copy of the outstanding-work list. The last session's
> narrative (`CONTEXT-2026-10-01.md`) is local-only; everything needed to keep going
> is here or below.

### First steps on a new machine
- `git clone` needs GitHub access. The dev box used a manually-installed `gh` 2.102.0
  (`~/.local/opt/gh` symlinked into `~/.local/bin`) — **not** a pacman package, because
  pacman needed a sudo password; upgrading means re-downloading the tarball.
- **`/tmp/opencode` is empty** and was wiped: the `ragseo-deps` PYTHONPATH venv and
  `ruff/bin/ruff` are gone, and backend deps are not installed system-wide. The prod
  `.env` reference copy at `/tmp/opencode/server.env` is **also gone** — get real values
  from the VPS `.env`.
- **No Node/npm on the dev host.** The working gates are Docker builds, not local tooling:
  frontend → `docker build ./frontend` (full lint **and** type gate); backend → rebuild
  the image, then `docker compose exec backend python -m pytest -m "not integration"`.

### 1. Live prod bugs — one deploy closes both (already fixed in tree, just undeployed)
1. **`celery-worker` split-brain** — prod's worker runs the pre-TSR image (old
   `orchestrator.py`, no `retry_job()`, no GATE-2 guard) while the API serves
   `POST /api/jobs/{id}/retry`. **HTTP smoke tests cannot detect it** (they only hit the
   API container). Fixed by `af08d60` (both services now `image: ragseo-backend:local`).
2. **`/docs` serves Swagger, not Doctrine** — Caddy `handle` is first-match-wins, so
   `handle /docs` + `handle /docs/*` silently replaced the frontend's Doctrine Reference
   section. Fixed by `0fa1b6b` (Swagger → `/api/meta/docs`, Caddy handlers deleted).
   Smoke after deploy: `/docs` body must **not** contain `swagger-ui`; a 200 is **not**
   sufficient, a regression still serves 200.

### 2. Real code defects still in `main`
- 🔴 **`reconcile_doctrine` would mark every upload `missing`** — the blocker for all
  doctrine-upload work. `doc_ingestion.py:287` globs **only** `settings.doctrine_path`,
  but the sweep at `:367-376` marks every `active` doc whose filename isn't in that scan,
  and it runs **hourly** (`celery_app.py:39-42`, `crontab(minute=0)`). Fix: a
  `doctrine_folders()` + `scan_doctrine_files()` union (model on `_external_folders`,
  `routers/ingest.py:44-55`) used by **both** `ingest_all_docs` (`:129`) and
  `reconcile_doctrine` (`:287`).
- 🔴 **Prod `celery-worker` has no `volumes:` block** — `docker-compose.prod.yml:117`,
  confirmed: no `volumes:` key anywhere in the block (the backend's is at `:93`). 2's
  first item is not actually fixed until this exists, since the worker runs the hourly
  reconcile and must see the same writable dir the API writes to. Prod `doctrine_path`
  is the image layer (`backend/Dockerfile:15`, no volume) = ephemeral; dev is `:ro`.
  Needs `doctrine_upload_path` in `config.py` (beside `:28-30`) plus a
  `./doctrine_uploads:/app/uploads/doctrine` mount in **four** places: dev backend +
  dev worker (`docker-compose.yml:88,121`) and prod backend + **prod celery-worker**.
- 🟡 **`extract_doc_number` mangles non-conforming names** — `doc_ingestion.py:29-33`
  falls back to `filename.split("_")[0].split(".")[0]`, and `extract_series` (`:36-41`)
  returns `"misc"` for anything not starting with a digit. Verified: `Doc 100_Something.md`
  → `100`/`100` ✅ and `Doc 316:Something.md` → `316`/`300` ✅, but
  `Doc 100 - Something.md` → `"Doc 100 - Something"`/`misc` ❌ and `random.md` →
  `"random"`/`misc` ❌. The fallback splits only on `_` and `.`, and that garbage is
  **permanent** under `uq_documents_doc_number_active`, so a later legitimate `Doc 100 …`
  can never take that number. Gate the upload path on `DOC_PATTERN` (`:18`), `.md`,
  `len(filename) <= 255` (`Document.filename` is `String(255)`), ~10 MB cap, and 409 on
  a name already in the baked `doctrine_path` (same reasoning as the baked-name refusal
  at `routers/ingest.py:434-458`).
- 🟡 **`log_audit` commits the surrounding transaction** (`services/audit.py:6-15`) —
  harmless on read-only routes but not side-effect free, and it already caused one real
  bug: `delete_user` lost its explicit `db.commit()` and persisted only as a side effect
  of `log_audit`. It was restored **after** the `log_audit` call on purpose — placing it
  before would let a crash in between delete a user with no audit row.

### 3. Unverified work
**`backend/tests/test_jobs_export.py` (364 lines, `0fa1b6b`) has never been run.** Dev
bind-mounts only `./backend/app` (`docker-compose.yml:96`), **not `tests/`**, and
`/tmp/opencode` was wiped. `pytest==8.3.3` *is* in the image (`requirements.txt:17`), so
rebuild the image and run the suite. The same rebuild should clear the **2 known
`test_external_ingest` failures** (stale image still carrying the 56 pre-purge baked
files). Last green run: **204 passed / 2 failed**. `ruff check` also can't run locally
(the binary was in `/tmp/opencode`) — re-fetch 0.16.8 to match `backend/pyproject.toml`.

### 4. Debt, not defects
- **10 pages duplicate the shell** (`AuthGuard` + `Sidebar` + `Header`) —
  `app/{page,jobs/page,jobs/[jobId]/page,exports,agents,ingest,docs/page,docs/[docId],admin/users,learning}/page.tsx`.
- **`lib/api.ts` has three request shapes** — `apiFetch`, `apiUpload`, `apiDownload`.
- **Status-variant maps** duplicated across components.
- Optional: dedicated Doc 307 SERP agent → add to `AGENT_FUNCTIONS`, `tasks.py:16-20`
  (currently router/writer/auditor only).

## Next Move

0. **⛔ DEPLOY `0fa1b6b` TO THE VPS — still outstanding, do this first.**
   Three commits are pushed but prod is still on `9df8ea5`, so **two live prod
   bugs are unfixed**:
   - the **`celery-worker` split-brain** — it runs the pre-TSR image (old
     `orchestrator.py` — no `retry_job()`, no GATE-2 guard) while the API serves
     `POST /api/jobs/{id}/retry`. HTTP smoke tests cannot detect this because
     they only exercise the API container.
   - **`/docs` serves Swagger, not Doctrine** — Caddy shadows the frontend's
     Doctrine Reference section. This also blocks the doctrine-upload UI, which
     is planned for `/docs`.
   ```bash
   cd /opt/ragseo-platform
   git pull origin main
   docker compose -f docker-compose.prod.yml build backend celery-worker frontend
   docker compose -f docker-compose.prod.yml up -d
   # convergence — both IDs must now be identical (shared ragseo-backend:local tag)
   docker inspect -f '{{.Image}}' ragseo-platform-backend-1 ragseo-platform-celery-worker-1
   docker compose -f docker-compose.prod.yml exec db psql -U ragseo -d ragseo \
     -c "SELECT version_num FROM alembic_version;"      # expect 0010_audit_logs
   ```
   Then smoke-test: log in → must land on `/` (Dashboard) and Back must not
   return to `/login`; `/docs` must render Doctrine (body must **not** contain
   `swagger-ui`) and `/api/meta/docs` must be the Swagger UI.
1. ~~**Commit the working tree**~~ ✅ done — `0fa1b6b` pushed, tree clean.
2. **Run the backend suite.** `tests/test_jobs_export.py` (364 lines) is
   committed but its run is **unverified** — see the "Backend tests" note below.
3. **Doctrine upload (Part B) — designed, not started.** Full plan in
   "Doctrine upload — planned, NOT started" above. Two things to settle first:
   the `reconcile_doctrine` blocker and the missing prod `celery-worker` volume.

## Deployed state — ⚠️ prod is STILL on `9df8ea5`; three commits are deployed-nowwhere
- 📄 **The "HANDOFF — outstanding fixes" section above is the canonical work list**
  (verified 2026-10-01, portable across machines — `CONTEXT-*.md` is gitignored).
- **VPS (`157.230.2.51`) still runs `9df8ea5`.** Nothing has been redeployed since
  the earlier 2026-09-30 session (smoke tests were 200 at that point).
  Sessions: `CONTEXT-2026-09-30.md`, `CONTEXT-2026-10-01.md`.
- **Local == `origin/main` == `0fa1b6b` — in sync, pushed.** So these are in the
  tree and on GitHub but **not** on prod:
  - `af08d60` shared image tag (`docker-compose.prod.yml`)
  - `dff3578` post-login landing at `/` (frontend only)
  - `0fa1b6b` Markdown export + the `/docs` unblock (Caddyfile + FastAPI doc URLs)
- Both prod bugs named in **Next Move 0** are therefore **still live**.
- ~~All previously-undelivered work shipped.~~ Superseded by the above.
- **`2738159`** best-practice cleanup — *deployed* (was "NOT deployed" in the
  2026-09-19 notes below; that status is superseded).
- **`653f9aa`** deploy hardening — fail-fast secrets in `config.py`, compose
  healthchecks, log limits (`json-file` caps), pinned image tags, Caddy security
  headers, `scripts/backup_db.sh`. Deployed.
- **`809c7a8`** user soft-delete + RBAC audit trail + job retry + system stats. Deployed.
- **`9df8ea5`** dark mode + dashboard landing rewrite + job retry/user restore UI. Deployed.

### New backend surface from `809c7a8`
Implementation detail for this wave is documented in full under
**"TSR refactor wave — soft-delete, RBAC audit, retry, dark mode (2026-09-23)"**
above. Only the deploy-relevant facts repeated here:
- Alembic chain gains **`0009_user_soft_delete`** (adds `users.deleted_at`, drops
  `ix_users_username`, adds dialect-branched partial unique
  `uq_users_username_active` + `ix_users_deleted_at`) and **`0010_audit_logs`**.
- `retry_job()` in `services/orchestrator.py` → `POST /api/jobs/{job_id}/retry`.
- `GET /api/stats` gains the `system` block (`active_users`, `queued_jobs`,
  `avg_latency_seconds`, `health`).
- Migrations apply automatically on container start — see the note in
  "Deploy mechanics" below.

### Deploy mechanics worth remembering
- **Migrations auto-apply on container start** — `backend/docker-entrypoint.sh`
  runs `python scripts/migrate.py` before `exec "$@"`. So `0009`/`0010` applied
  during `up -d`; there is **no** manual alembic step. `RUN_SEED` / `RUN_EXTERNAL`
  gates follow it, off by default.
- **Alembic chain now**: 0001_baseline → 0002_jobs → 0003_local_embeddings →
  0004_external_data → 0005_job_stage_idempotency → 0006_doc_number_unique →
  0007_login_throttle → 0008_learning_loop → **0009_user_soft_delete** →
  **0010_audit_logs**.
- **✅ FIXED 2026-09-30 — `backend` and `celery-worker` share one image tag.**
  They previously both declared `build: ./backend` with no `image:` key, so
  Compose built two independent tags (`ragseo-platform-backend:latest` vs
  `ragseo-platform-celery-worker:latest`); `build backend` alone left the worker
  on the old `orchestrator.py` — where `retry_job()` and the GATE-2
  `advance_job` guard live — i.e. a split-brain API/worker that HTTP smoke tests
  cannot detect (they only exercise the API container).
  **Now:** both services carry `image: ragseo-backend:local`, so they cannot
  diverge. Keep listing both in the build command anyway — it's harmless and
  correct. Verify with
  `docker inspect -f '{{.Image}}' ragseo-platform-backend-1 ragseo-platform-celery-worker-1`
  (IDs must match).
- **Frontend is a baked prod build** (no bind mount) → any UI change requires
  `docker compose -f docker-compose.prod.yml build frontend`. That's what made
  `9df8ea5` (`frontend/Dockerfile` +6, compose +12) a full-image deploy.

## Post-login landing page + doctrine upload design (2026-09-30, later session)
### `dff3578` — `/` is now the post-login landing page (frontend only, PUSHED, not deployed)
`/` already rendered the Dashboard since `9df8ea5`; only the redirect target was wrong.
- `app/login/page.tsx:32`: `router.push("/docs")` → `router.replace("/")`.
- `components/layout/AuthGuard.tsx:14,18`: both redirects `push` → `replace`. With `push`,
  `/login` stayed in the back-stack so Back after signing in bounced to a login-gated URL.
- `app/login/page.tsx`: added an effect bouncing an already-authenticated visitor off `/login`.
- **Naming trap:** the new effect needs auth-loading, but the page already binds `loading`
  to the *submit button's* pending state (`:14`). Must alias — `const { user, loading: authLoading, refresh }`.
  A same-name destructure is a hard `Failed to compile`, not a lint warning.
- Verified in the built bundle, not by HTTP (the redirect is client-side, so a 200 proves
  nothing): the login chunk has 2 `replace` call sites, 0 `push`, 0 `"/docs"`; every
  AuthGuard copy across all 7 page chunks uses `replace` for both branches.
- No backend change, no migration, no `docs` route change. Writers/admins both reach `/`
  (`page.tsx:11` has no `requireAdmin`).

### ⚠️ `docker compose up -d <svc>` does NOT rebuild — even with a `build:` key
Hit live this session: `docker compose up -d frontend` reported "Container … Running" and
changed nothing, because the image already existed. Same class of bug as the `celery-worker`
trap, and it applies to **every** service including the frontend. Always:
```bash
docker compose build frontend && docker compose up -d --force-recreate frontend
```
Check with `docker inspect -f '{{.Image}}' <container>` against `docker images <tag> --format '{{.ID}}'`.

### ✅ The standing "lint unverified" caveat is now RESOLVED
`next build` (step 8 of the frontend Dockerfile) prints `Linting and checking validity of types`
and **fails on lint errors too**, not just TS. So `docker build ./frontend` is a full
lint+type gate. This closes a caveat carried in four separate sections of this file.
It also *caught* the `loading` collision above. Node is still absent on the host, so
`npx tsc --noEmit` / `npm run lint` still need a Node machine for interactive iteration —
but nothing needs to be pushed unverified.

### ⚠️ Backend tests are NOT runnable on this host right now
`/tmp/opencode` was wiped: `ragseo-deps` (the `PYTHONPATH` venv) and `ruff/bin/ruff` are gone,
and no backend packages are installed system-wide (`import fastapi` fails). The recorded
command no longer works. `pytest==8.3.3` *is* in the image (`requirements.txt:17`), but dev
bind-mounts only `./backend/app` (`docker-compose.yml:96`) — **not `tests/`** — so tests need
an image rebuild before `docker compose exec backend python -m pytest -m "not integration"`.
The 2 known `test_external_ingest` failures (stale local image carrying the pre-purge 56
baked files) are still unverified. **Consequence:** `tests/test_jobs_export.py` (364 lines,
`0fa1b6b`) is committed but **its run is unverified** — rebuild the image, then run the
suite and clear both items at once.

## Markdown export + `/docs` unblock — `0fa1b6b` (2026-09-30 night, PUSHED, not deployed)
### `GET /api/jobs/{id}/export.md` — the approved draft as a Markdown file
`services/markdown_export.py` (new, 104 lines) + route at `routers/jobs.py:181`.
- Renders the approved writer draft with YAML front matter (`title`, `meta_title`,
  `meta_description`, `brand`, `content_type`, `archetype`) and the body **verbatim**.
  The body already lives in the writer task's `output_data["output"]["content_markdown"]`,
  so this is read + format — **no model call, nothing regenerated**.
- **Values quoted with `json.dumps`**, which is a valid YAML double-quoted scalar →
  colons, quotes, `#`, newlines and leading dashes need no hand-rolled escaping.
  Optional fields are omitted when empty rather than emitted blank.
- 409 unless `job.status == "approved"`; 404 if no job or no completed draft.
- **Audited as `job.export`**, written *last* so rejected exports leave no row.
  `log_audit` commits the surrounding transaction — harmless here, but not side-effect free.
- **Draft selection** (`select_writer_output`): newest writer stage that *has* content, not
  the newest writer stage outright — revision loops create several and `retry_job` keeps
  earlier ones as `skipped`, so `max(sequence)` can land on an empty output. The scan also
  drops failed tasks (`run_agent` only writes `output_data` on success). Explicit
  `join(JobStage)` because the models declare no ORM `relationship()`.
- Filename: `_slug(title)` → `_slug(job.title)` → `job.id`, stem ≤ 80 chars, as a
  **chain not a nest** so an all-punctuation title can't swallow the job id.
- Frontend: `apiDownload()` in `lib/api.ts` (blob + object URL, `Content-Disposition`
  name with a JS fallback) + **Export .md** on `jobs/[jobId]/page.tsx`, approved jobs only.
- `expose_headers=["Content-Disposition"]` on CORS is **required**, not cosmetic: dev is
  `:3000` → `:8000` and the browser hides the header cross-origin without it.

### 🔴 The `/docs` fix — Caddy was shadowing the whole Doctrine Reference section
**Caddy `handle` blocks are mutually exclusive and first-match-wins.** The Caddyfile had
`handle /docs` + `handle /docs/*` → backend for Swagger, which **silently replaced the
frontend's `/docs`** (`Sidebar -> /docs`) in prod. Not cosmetic: the doctrine-upload UI is
planned for `/docs`, so this had to be cleared first.
- `main.py`: `docs_url="/api/meta/docs"`, `redoc_url="/api/meta/redoc"` — no Caddy change
  needed, the existing `/api/*` block already forwards it.
- Caddyfile: the two `/docs` handlers **deleted**, with a comment recording why.
- **`/openapi.json` stays at the root on purpose** — both UIs reference it by absolute
  path and the deploy smoke check curls it; moving it breaks all three.
- **General rule this exposes: only `/api/*` belongs to the backend.** Any `handle` pointing
  a frontend-owned path at FastAPI replaces that page, with no error the user can diagnose.
- **A malformed Caddyfile takes the whole site down**, and `up -d` only restarts Caddy when
  the config actually changed. Validate first:
  `docker compose -f docker-compose.prod.yml exec caddy caddy validate --config /etc/caddy/Caddyfile`
- The 200 in the deploy smoke check is **not** enough for this route — a regression still
  serves a 200 (Swagger). `prompts/03-push-redeploy.md` now greps the `/docs` body for
  `swagger-ui` and fails loudly.

## Doctrine upload — planned, NOT started
Goal: a logged-in user can upload new doctrine `.md` files through the web UI. Mirrors the
proven `POST /api/ingest/external/upload` pattern (`routers/ingest.py:358-410`). Nothing
written yet; decisions taken with the user: **`require_writer`** (admin+writer, so the UI
goes on `/docs` — `/ingest` is admin-gated at `app/ingest/page.tsx:31`), **keep auto-supersede
but return which active doc was superseded**, and **inline but scoped** to the uploaded files.
- **`/docs` now resolves to the frontend in the tree** (`0fa1b6b` removed the Caddy
  shadowing) — so the target page for this feature is reachable. **But prod still serves
  Swagger there** until that commit is deployed, so this work must not ship before the
  deploy in Next Move 0 or the feature lands on a 404-ish page.
- **🔴 BLOCKER — `reconcile_doctrine` would mark every upload `missing`.** It globs **only**
  `settings.doctrine_path` (`services/doc_ingestion.py:287`) yet sweeps every active doc whose
  filename isn't in that scan to `status="missing"` (`:370-376`), and it runs **hourly on the
  worker** (`celery_app.py:39-42`). An upload written to any other directory is ingested, then
  flipped to `missing` within the hour. Fix first: a `doctrine_folders()` + `scan_doctrine_files()`
  union (copy of `_external_folders`, `routers/ingest.py:44-55`) used by **both**
  `ingest_all_docs:129` and `reconcile_doctrine:287`.
- **No writable doctrine dir exists.** Prod `doctrine_path` is the image layer (`Dockerfile:15`,
  no volume) = ephemeral; dev is bind-mounted `:ro`. Needs `doctrine_upload_path` in `config.py`
  (beside `:28-30`) + a `./doctrine_uploads:/app/uploads/doctrine` mount in **four** places:
  dev backend + dev worker (`docker-compose.yml:88,121`) and prod backend + **prod celery-worker,
  which currently has no `volumes:` block at all** (`docker-compose.prod.yml:117-145`). The
  worker mount is what stops its hourly reconcile from mass-marking uploads `missing`.
- **Validation must reject what the parser silently mangles.** `extract_doc_number`
  (`:29-33`) returns the whole filename when there is no `_`/`:` after the number, so
  `Doc 100 - Something.md` → `doc_number="Doc 100 - Something"`, `series="misc"`, and that
  garbage becomes permanent under `uq_documents_doc_number_active`. Gate on `DOC_PATTERN`
  (`:18`), `.md`, `len(filename) <= 255` (`Document.filename` is `String(255)`), a ~10 MB cap,
  and reject a name that already exists in baked `doctrine_path` (409) so an upload can't
  silently shadow a baked doc — same reasoning as the baked-name refusal in the external
  delete handler (`ingest.py:434-458`).
- Extract the per-file body into `_ingest_one()` so `ingest_all_docs` and the new
  `ingest_files(db, paths)` share the supersede-before-`flush()` discipline (`:198-207`);
  extract `_rebuild_references(db, active_only)` from `:245-257` / `:381-393` (they differ:
  all docs vs active only).
- `python-multipart==0.0.9` is already installed (`requirements.txt:15`). No new model → no
  migration. `_safe_filename` (`ingest.py:58-64`) should be promoted to a shared
  `services/uploads.py` rather than imported privately across routers.
- Uploaded doctrine is gitignored (like `external_uploads/`), survives VPS `git pull`, not a
  from-scratch rebuild; `scripts/backup_db.sh` covers DB rows only, not the `.md` bytes.
  No delete/revert UI — removal leaves the doc `missing`, and superseding is one-way.

## Open items carried forward from 2026-09-19
- ~~**Lint is still unverified**~~ — **RESOLVED 2026-09-30**: `next build` inside
  `docker build ./frontend` fails on lint errors as well as TS errors, so the image build
  is a full lint+type gate (it caught a real bug on `dff3578`). Node is still absent on
  the dev host, so `npx tsc --noEmit`/`npm run lint` still need a Node machine for fast
  iteration, but nothing needs pushing unverified. Flagged refactors (all still open):
  shared dashboard layout (8 × duplicated AuthGuard+Sidebar+Header shell), status-variant
  maps, api.ts EXTRA DRY — the last one now has a third shape to fold in, since
  `apiDownload` (`0fa1b6b`) sits alongside `apiFetch`/`apiUpload` in `lib/api.ts`.
- **Rename ripple**: tests patch `tasks.session_scope` (was `tasks.SessionLocal`);
  `tests/test_external_data.py` imports `latest_export_ids`. Don't regress either.

## Dev-box auth notes (2026-09-30)
- **`gh` 2.102.0 installed manually** to `~/.local/opt/gh`, symlinked into
  `~/.local/bin` (already on PATH) — pacman needed a sudo password, so this is a
  tarball install, **not** a pacman package. Upgrading means re-downloading the
  release tarball, not `pacman -S gh`.
- Git credential helper now delegates to gh:
  `credential.https://github.com.helper='!gh auth git-credential'`. Token is
  **plaintext** in `~/.config/gh/hosts.yml` (gh's own warning) — fine for a dev
  box, avoid on shared/backed-up machines.
- **Unrelated to the VPS**: prod still pulls via its own read-only deploy key at
  `/root/.ssh/id_ed25519_ragseo`. Dev-box gh auth does not affect prod pulls.
- Deploy SOP is git-driven (private `github.com/rlpalomo25/ragseo-platform`, VPS
  read-only deploy key); never push dev `.env`. Prod values: `/tmp/opencode/server.env`.

## Historical — Open items captured 2026-09-19 (deploy status since resolved)
- ~~**Best-practice cleanup committed `2738159`, working tree clean, NOT deployed.
  VPS still runs `2a8edf3`**~~ — **superseded**: deployed 2026-09-23, confirmed live
  again 2026-09-30. Retained for provenance. The cleanup itself consisted of:
  `session_scope()` ctx manager (`app/database.py`, used by `tasks.py`),
  `latest_export_ids` made public & shared by `external_data`/`learning_loop`
  (killed the duplicate copy), `voyage_api_url` setting (SPOD), `print()`→logger,
  silent catches fixed (learning_loop, EditUserModal, logout), dead code removed
  (`get_doctrine_context`, `Toast.tsx`, `Modal.contentRef`), auth cookie
  `max_age` from `settings.session_expiry_hours`, alembic E501 per-file-ignored.
  Tests: **183 passed**; `ruff check` clean; `ruff format` 201 files.
- The Node-less-frontend caveat, the `session_scope` rename ripple, and the
  git-driven deploy SOP from that session are all still current and are recorded
  once, above, under "Open items carried forward" and "Dev-box auth notes".

## Relevant Files
- Importer: `backend/app/services/external_ingest.py` · service: `backend/app/services/external_data.py` · models: `backend/app/models/external.py` · migration: `backend/alembic/versions/0004_external_data.py` · router: `backend/app/routers/ingest.py` · CLI: `backend/scripts/import_external.py` · agents: `backend/app/services/agents/{writer,router}.py`
- Upload: `POST /api/ingest/external/upload` in `backend/app/routers/ingest.py` (writes `external_upload_path`); delete: `DELETE /api/ingest/external/delete` (same module, `delete_external_export` in `backend/app/services/external_ingest.py`). UI `frontend/src/components/ingest/ExternalDataCard.tsx` (upload form + per-row/bulk delete), page `frontend/src/app/exports/page.tsx`, hook `frontend/src/lib/hooks/useIngest.ts` (`uploadExternalFiles`, `deleteExternalFiles`), helper `frontend/src/lib/api.ts` (`apiUpload`). Mount `./external_uploads:/app/uploads/external` in both compose files (dev backend+worker, prod backend). Needs `python-multipart`.
- Config/mount: `backend/app/config.py` (`external_data_path`, `external_upload_path`), `frontend/../docker-compose.yml` (backend+worker `./09042026:/app/external:ro` + `./external_uploads:/app/uploads/external`)
- Tests: `backend/tests/test_external_ingest.py` (19 tests incl. upload + delete API), `backend/tests/conftest.py` (ALL_TABLES + imports)
- Frontend: `frontend/src/app/ingest/page.tsx` (ExternalDataCard), `frontend/src/types/ingest.ts`, `frontend/src/lib/hooks/useIngest.ts`
- Draft export: `backend/app/services/markdown_export.py` (`select_writer_output`, `build_markdown`, `build_filename`) · route `GET /api/jobs/{id}/export.md` in `backend/app/routers/jobs.py` (writer-gated, 409 unless `approved`, audits `job.export`) · tests `backend/tests/test_jobs_export.py` · UI `frontend/src/app/jobs/[jobId]/page.tsx` + `apiDownload` in `frontend/src/lib/api.ts` · FastAPI doc URLs `/api/meta/docs` + `/api/meta/redoc` in `backend/app/main.py` (`/openapi.json` stays at root)
