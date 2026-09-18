# RAGSEO Platform — Implementation Plan & Status

_Last updated: 2026-09-10. §5B closed out — pipeline reaches the human gate._

---

## 1. Where We Are

Phases 0–3 of `REQUIREMENTS.md` are **implemented and unit-tested**. The
writer token fix (max_tokens=16000) is now **deployed and live** — the writer
completes full drafts without truncation. End-to-end pipeline mechanics are
proven (router → writer → auditor → revision loop → escalation), and the
auditor's Doc 192 packaging checks have been **scoped to Phase 4** by decision.
**End-to-end human gate verified live (Sept 10, §5B):** the MasterShield
comparison job reached `awaiting_approval`, audit verdict `pass`, and the
Approve flow moved it to `approved`.

**Stack:** FastAPI · PostgreSQL 16 + pgvector · Redis/Celery · Next.js 14 ·
Anthropic Claude (`claude-sonnet-4-5`) · Voyage AI embeddings (optional, key not yet set)

---

## 2. What Is Built

### Phase 0 — Hardening ✅
- HMAC-signed session tokens (raw token in DB, signed issued; logout deletes only current session)
- Env-driven CORS, prod blocks default admin seeding, UUID path validation
- Alembic migrations: `0001_baseline` (pgvector + hnsw), `0002_jobs`
- `.gitignore` / `.dockerignore` (whitelist style — `.env` never enters images)
- Pytest scaffold: SQLite-compatible via `Uuid` type + Vector→BLOB compile hook

### Phase 1 — Real RAG ✅
- pgvector stack; `DocChunk` model; chunking per Doc 122 (heading-aligned,
  provenance headers `[Doc N: Title > Path]`, H1 excluded from paths)
- Voyage embeddings service (`voyage-3-lite`, 1024 dims) with graceful no-key fallback
- Hybrid retrieval: cosine + scored keyword + RRF fusion; powers search API,
  agent context builder (`build_retrieval_context`, token-budgeted), router sources
- Ingestion re-chunks + re-embeds changed docs. Corpus: 122 docs → 3,052 chunks.
  Oversized rubric-table chunks (~16k chars) intentionally kept whole per Doc 122.

### Phase 2 — Agents ✅
- `services/doctrine.py`: governing-doc loader, provenance stamps, brand config
  (mastershield→316/130, kleangutter→320/131, mmgg→324/132), structure-companion map
- `agents/router.py`: intent/brand/content_type/applicable_docs routing
- `agents/writer.py`: governing docs full-text + supplementary retrieval;
  `===RAGSEO_META===` / `===RAGSEO_CONTENT===` protocol; validated `WriterMeta`;
  honors `revision_feedback` on audit-fail loops
- `agents/auditor.py`: Doc 328 rubric loaded live; strict JSON verdict;
  mechanical critical-fail→FAIL enforcement; `source_task_id` support
- Shared parsing in `agents/llm_output.py`

### Phase 3 — Orchestration ✅
- Models: `AgentJob` (running→awaiting_approval→approved/failed/cancelled),
  `JobStage` (sequence, task FK, feedback); migration `0002_jobs`
- `services/orchestrator.py`: state machine — router→writer→auditor chaining,
  max 2 auto-revisions on audit FAIL (findings fed back as `revision_feedback`),
  human approval gate, cancel semantics, standalone-task no-op guard
- `tasks.py`: `advance_job` hook after every agent run (orchestration errors
  never lose persisted task results)
- API `/api/jobs`: create/list/detail/approve/cancel (writer role required)
- Frontend: `/jobs` list + New Job modal, `/jobs/[jobId]` stage timeline +
  draft preview + audit findings + Approve/Cancel; "Pipeline" nav item

### Config added today
- `LLM_MODEL` (default `claude-sonnet-4-5`) and `LLM_MAX_TOKENS` in Settings
- Token budgets: writer 16000, auditor 16384, router 2048
- `call_llm` raises explicit error on `stop_reason == "max_tokens"` (truncation
  guard — no more mysterious JSON parse failures)

---

## 3. Live Verification Log (Aug 21)

| # | Stage reached | Outcome | Fix applied |
|---|---------------|---------|-------------|
| 1 | router | 404 — model `claude-sonnet-4-20250514` retired | Model now configurable; default `claude-sonnet-4-5` |
| 2 | auditor | Unparseable JSON — verdict truncated at 4096 tok | Truncation guard + auditor→8192 |
| 3 | auditor | Truncated again at 8192 | Brevity rules in prompt (only fail/warn findings, ≤25-word notes) + auditor→16384 |
| 4 | **revision loop** | Router ✅ Writer ✅ Auditor returned rigorous FAIL (11 critical findings citing Doc 316-C structure, component classes, metadata rules) → auto-revision dispatched, `revision_count=1` | Revision writer truncated at 8000 → **writer→16000 (in code, not yet deployed)** |

Conclusion: pipeline mechanics fully proven — chaining, doctrine-grounded
auditing, feedback-driven revisions. Only the writer token bump awaits deploy.

---

## 3B. Verification Round 2 (Sept 9)

Deployed the writer fix, then ran the MasterShield comparison verification job
four times. Each run pushed one stage further; the fixes below are **deployed
and verified live** with the exception of the three §5B items (in code, not yet
redeployed at time of writing).

| # | Failure observed live | Fix applied (deployed ✅) | Test coverage |
|---|----------------------|----------------------------|---------------|
| 1 | Auditor emitted `status="flag"` (out-of-enum) → whole job died at validation | `AuditFinding.status` before-validator coerces unknown → `"warn"` (auditor.py) | `test_auditor_coerces_non_standard_status` |
| 2 | Auditor response "not parseable JSON" (extra prose/braces) | Hardened `extract_json`: fence-aware + brace-aware `_first_json_object` scanner (llm_output.py) | 4 tests incl. braces-in-strings |
| 3 | Revision writer returned `archetype` as a dict | `WriterMeta` before-validator coerces non-string → `"primary"/"value"/first scalar`, else JSON string (writer.py) | `test_writer_coerces_dict_archetype` |
| 4 | Auditor mechanically FAILing on Doc 192 publish-readiness the writer can't produce | **Decision (Roberto): scope Doc 192 packaging to Phase 4.** Added `scope: content\|packaging` to findings; prompt boundary; `SCOPE_PACKAGING_CHECKS` config (default on); packaging criticals demoted `critical→major`, `fail→warn`, verdict recomputed to `pass_with_notes` when no content-critical remains | `test_auditor_scopes_packaging_criticals`, `test_auditor_content_critical_still_fails_with_packaging`, `test_auditor_unknown_scope_defaults_content` |

Observed on the last live run (job `4206c756`): scoping worked (packaging →
`major/warn` ✅), but the remaining "content" criticals were themselves
**render-format / Tech-QC form items** (Doc 194 callout CSS classes, Tech-Sources
`<ol><li id="src-N">` markup, YAML/URL-slug form, meta-length). Additionally the
auditor reported "meta description absent" even though the writer produced that
meta — **stale gap: the auditor never saw the writer's meta block.** Round-3
auditor also hit a transient unparseable-JSON error.

**Pipeline mechanics status:** fully proven — chaining, doctrine-grounded audit
(now scope-aware), feedback-driven revisions (max 2), escalation-fail path with
human-review note, and the mechanical critical-fail override all exercised live.

---

## 4. Environment Facts

- `.env` contains valid `ANTHROPIC_API_KEY`; gitignored + excluded from Docker builds.
  **Key was pasted into chat — rotate it when convenient.**
- `VOYAGE_API_KEY` **not set** → system runs keyword-only search. To enable
  semantic retrieval: add key, restart, `POST /api/docs/reingest` as admin.
- Default dev login: `admin` / `changeme`. Cookie jar for curl testing:
  `/tmp/opencode/ragseo-cookies.txt`.
- Tests: `cd backend && PYTHONPATH=/tmp/opencode/ragseo-deps python3 -m pytest -q`
  (deps installed to `/tmp/opencode/ragseo-deps`; the old `/tmp/opencode/ragseo-venv` was wiped) →
  last full green run: **97 passed**; the final §5B additions (retry + meta-in-context tests)
  were written after that run and the test run was aborted, so expected count ~100 — re-run to confirm.
- Rebuild: `sudo docker compose -f ragseo-platform/docker-compose.yml up -d --build backend celery-worker frontend`
  (migrations apply automatically on backend start)

---

## 5. Resume Point — superseded by §5B (Sept 9). Kept for history.
## 5B. Resume Point — Next Steps (as of Sept 9)

> **Closed out (Sept 10).** All three fixes are deployed and verified live.
> The resume-point steps below are now history:
> - Deploy ✅ (rebuild ran; backend + celery-worker)
> - Verification job ✅ — job `2bcef6b8-8ab0-4edc-9af1-3152f2f401a2`
>   (MasterShield comparison) reached **`awaiting_approval`** with final audit
>   verdict **`pass`** (1 cosmetic note). Note: it took the full 2 auto-revisions
>   (rounds: FAIL → FAIL → pass) rather than the predicted single round — fine,
>   the goal was reaching the human gate, which it did.
> - Approve flow ✅ — `POST /api/jobs/{id}/approve` → `approved`; UI button
>   wired to the same endpoint (frontend `jobs/[jobId]/page.tsx:125`).

**Three final fixes are in code but NOT yet redeployed; deploy then verify.**

1. **Deploy** (in code, awaiting rebuild — run in terminal from `/home/roberto/RAGv2`):
   ```
   sudo docker compose -f ragseo-platform/docker-compose.yml up -d --build backend celery-worker
   ```
2. **Re-run the verification job** (POST /api/jobs or UI → New Job):
   brief: "Write a MasterShield vs traditional gutter guards comparison page…",
   brand `mastershield`, content_type `comparison`.
   Expected after §5B fixes: auditor audits against the writer's REAL meta
   (`Draft Metadata` section), scope-flagged render-format items (callout CSS,
   Tech-Sources `<ol>` markup, YAML/slug form, summary/meta-length) demote to
   `major/warn`, no content-critical remains → verdict `pass_with_notes` →
   job status **`awaiting_approval`** (single round, no revision needed).
3. **Verify Approve flow end-to-end**: `POST /api/jobs/{id}/approve` and the
   UI Approve button → job `approved`.
4. If the job still escalates: re-check which "content" criticals remain and
   decide whether they are substance (keep blocking) or form (extend scope).

The three §5B code fixes (all in `backend/`, not yet redeployed/verified live):
- **Auditor sees the writer's meta**: `_load_content` now returns `(content, meta)`;
  `run_auditor` renders a "Draft Metadata" block into the audit prompt — fixes
  the false "meta description absent" (auditor was auditing an assumed YAML block).
- **Broader packaging scope in prompt**: scope def now includes rendered-format /
  Tech-QC form items — Doc 194 callout CSS classes (`.callout.field`,
  `.callout.benefits`, `.askthis`, `.callout.compare`), Tech-Sources
  `<ol><li id="src-N">` anchor markup, URL slug / YAML-front-matter form,
  meta-field layout — while keeping substance checks (H2 architecture, claims/
  evidence, trust flow, CTA, voice, AEGIS) as blocking "content".
- **Auditor retry on unparseable JSON**: single LLM re-call with a
  "JSON-only" nudge when `extract_json` returns `None` (transient drift at
  round 3 killed an otherwise-passing run).

### §5C — Local embeddings via Ollama (Sept 10)

Replaced the Voyage AI cloud dependency with a **self-hosted Ollama** service
(default). In code, unit-tested (111 passing).

- `docker-compose.yml`: new `ollama` service (pulls `nomic-embed-text` on
  start), backend/worker get `EMBEDDING_PROVIDER=ollama`,
  `OLLAMA_BASE_URL=http://ollama:11434`, `EMBEDDING_MODEL=nomic-embed-text`,
  `EMBEDDING_DIMENSIONS=768`.
- `app/services/embeddings.py`: provider dispatch (`ollama` default, `voyage`
  optional, `none` = keyword-only); MTEB task prefixes for nomic
  (`search_document:`/`search_query:`); **retry/backoff** on 429/5xx/network
  (closed the old gap); dimension mismatch guard.
- `alembic 0003_local_embeddings`: `Vector(1024) → Vector(768)` — drops HNSW,
  nulls old 1024-dim vectors, rebuilds index (migration applies on backend
  start).
- `doc_ingestion.py`: re-ingest now **backfills** unchanged docs whose chunks
  lack vectors (was silently skipping) — so the dim change re-embeds cleanly.
- Tests: `test_embeddings.py` (providers, retry, dims, prefixes, **input
  truncation**) + backfill regression; suite hermetic via autouse
  `EMBEDDING_PROVIDER=none` fixture. **111 passing.**

**Context-cap resolution (Sept 10):** Ollama clamps *every* `nomic-embed-text`
tag (incl. `v1.5`; GGUF `context_length=2048` despite `num_ctx=8192` params) —
verified by bisect (max ≈9,383 chars) and the library metadata. Rather than
splitting oversized doctrine chunks (violates Doc 122), the backend embeds full
text and, **only on an Ollama "input exceeds the context length" 500**, retries
with progressively smaller head windows (`8192→1024`, config
`EMBEDDING_CHARS_PER_TOKEN` sets the first step). Dense table/number content
runs ~2.9 chars/token, so a single char cap was unreliable; the shrink loop
handles arbitrary density. Chunks stay whole in the DB.

**Vector-cast fix (Sept 10):** semantic search (`/api/docs/search`) 500'd with
"No operator matches" — raw `text()` SQL passed the query embedding as a plain
list, never typed as `vector`, so `<=>` had no operator. `_vector_search` now
binds a vector literal string + `CAST(:embedding AS vector)` (verified live:
Doc 328/430/Rolling-Handoff now top-hit their queries).

**Deploy mechanism:** backend/celery-worker now **bind-mount** `./backend/app`
(`:ro`) — code fixes deploy on `compose up -d`/`restart` with no image builds,
avoiding the Bake COPY-layer cache trap that cost several `--no-cache` rebuilds.

**Deploy status:** migration `0003` applied; **3,052/3,052 chunks embedded,
`embedding_failures=0`**; semantic search returns sensible top hits. `112` tests
pass.

**Apply (needs sudo):**
```
# after any app code change: restart picks up the bind-mounted code
sudo docker compose -f ragseo-platform/docker-compose.yml restart backend
curl -X POST http://localhost:8000/api/docs/reingest -b /tmp/opencode/ragseo-cookies.txt
# verify: embedding_failures=0; SQL:
#   SELECT count(*) FROM doc_chunks WHERE embedding IS NULL;  -- expect 0
# semantic search: /api/docs/search?q=canonical%20entity%20library%20faq
```

### Backlog / known gaps
- Embeddings are **local now**; next quality lever is Voyage `voyage-3-lite`
  (set `EMBEDDING_PROVIDER=voyage` + key if the local model underdelivers)
  or pinning the Ollama model to `bge-base-en-v1.5` (768 dims, same migration)
- Rotate Anthropic API key (exposed in chat)
- Long drafts (~8k+ tokens): consider streaming or artifact storage before
  Phase 4 UI polish
- Old failed jobs (c29606c6, e5ffa6f4, 07613e23, 67b98f69, and the Sept 9
  verification jobs edd2e565/30242916/4206c756) can be deleted or left as history
- Auditor severity calibration vs Doc 328 can resume after §5B closes out

---

## 6. Phase 4 — UX & Artifacts (next phase per REQUIREMENTS.md)

1. **Artifact versioning**: persist each approved draft as a versioned artifact
   (job_id, sequence, content, meta, provenance) instead of living only in task output.
2. **Packaging-audit gate**: pre-approval check that required page furniture
   exists (YAML front matter, JSON-LD, entity map, appendix wrapper) — much of
   this is already enforced by the auditor; formalize as a mechanical gate and
   **flip `SCOPE_PACKAGING_CHECKS=false`** when the packaging layer lands.
3. **Dashboard**: job throughput, revision rates, common audit failures,
   doctrine coverage stats.
4. **WordPress publishing** (currently out of scope) once pipeline is stable.

---

## 7. Key Decisions Made

| Decision | Choice |
|----------|--------|
| Embedding provider | Voyage AI `voyage-3-lite` (1024 dims), keyword-only fallback |
| Auto-revisions on audit FAIL | Max 2, then job fails with escalation note |
| Human gate | writer + admin roles can approve |
| Oversized doctrine chunks | Kept intact (strategic-integrity rule, Doc 122) |
| Auditor truncation strategy | Prompt-side brevity + high ceiling + hard truncation error |
| LLM model | `claude-sonnet-4-5` via `LLM_MODEL` env override |
| Doc 192 publish-readiness (Sept 9) | Scoped to Phase 4 until packaging lands: `scope: content\|packaging` findings, demote packaging criticals, recompute verdict (`SCOPE_PACKAGING_CHECKS`=true) |
| LLM schema drift (Sept 9) | Lenient coercion over hard failure for enum/type drift (auditor status/scope, writer meta); retry once on unparseable JSON |
| Writer meta visibility (Sept 9) | Auditor is given the writer's actual meta block ("Draft Metadata") instead of assuming YAML front matter |
