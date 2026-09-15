# RAGSEO Platform — Requirements Document

**Version:** 0.1 (initial draft, August 20, 2026)
**Source of truth for product intent:** the RAGSEO doctrine library (`/home/roberto/RAGv2/*.md`, 122 docs), especially Doc 230 (System Governor & Pipeline Orchestration), Docs 300–358 (Agent Instructions), Doc 122 (Retrieval & Chunking Doctrine).
**Codebase:** `ragseo-platform/` — FastAPI + PostgreSQL + Celery backend, Next.js 14 frontend.

---

## 1. Purpose

A web platform that operationalizes the RAGSEO content-production doctrine: it ingests the doctrine library as a queryable corpus, routes content requests through an orchestrated multi-agent pipeline (routing → analysis → strategy → architecture → writing → audit → publishing), and enforces the doctrine's quality gates automatically instead of relying on manual process discipline.

## 2. Current State (as built)

### Implemented and working
| Area | Detail |
|---|---|
| Auth | Login/logout/me, bcrypt, opaque session tokens (24h), roles (`admin`/`writer`), cookie + bearer support |
| User admin | CRUD with role/is_active management, soft delete |
| Doctrine ingestion | Filesystem scan → `documents` table; filename parsing (doc number/title/series/type/version), sha256 dedup, cross-reference graph (`doc_references`) |
| Doctrine browsing | List w/ filters + pagination, ILIKE search, detail view, references endpoint, re-ingest trigger |
| Agent infrastructure | Celery task queue, `AgentTask` lifecycle (pending→running→completed/failed) with output/error persistence |
| Router agent | The single implemented agent: intent + brand classification, returns JSON with `applicable_docs`, `next_agent`, confidence |
| Frontend | Login, docs browser (search/filter/pagination), doc viewer (markdown + TOC + references), agents page (run modal + task polling), admin users page |

### Key gaps (structural, not annotated in code)
1. **No actual RAG.** Despite the name: no embeddings, no vector store, no chunking. Agent context = whole documents concatenated and truncated at 15,000 chars (`agent_runner.py`). This directly violates Doc 122's retrieval doctrine.
2. **1 of ~30 agents implemented.** Doctrine defines a full agent roster (Docs 300–358). The router prompt already references `gap_analyzer`, `writer`, `validator` agents that don't exist.
3. **No pipeline orchestration.** Doc 230 requires staged routing (main pipeline + SOT branch) with failure re-routing; today each agent run is one-shot and disconnected.
4. **Zero tests.** `backend/tests/` is empty.
5. **Alembic configured but never used** — schema comes from `create_all()`; no migration history.
6. **Security debt:** default admin `admin/changeme` auto-seeded; `SECRET_KEY` setting exists but is unused by auth; CORS hardcoded to localhost:3000; no rate limiting; document IDs not UUID-validated.
7. **Portability debt:** hardcoded fallback path `/home/roberto/RAGv2` in `doc_ingestion.py`; no README, `.gitignore`, or `.dockerignore` (node_modules shipped in Docker build context).
8. **Dead weight:** `content_html` column never populated; unused deps (`asyncpg`, `httpx`, `python-multipart`, `markdown`, `beautifulsoup4`); unused `Toast`/`Card` components; logout deletes only first matching session row.

---

## 3. Functional Requirements

### FR-1 — Doctrine Corpus & Retrieval (RAG layer)
- FR-1.1: Chunk all doctrine documents per Doc 122 (context-independent chunks that preserve page strategy; heading-aligned, never artificially fragmented).
- FR-1.2: Generate embeddings per chunk; store in PostgreSQL via **pgvector** (keeps single-DB architecture).
- FR-1.3: Semantic retrieval endpoint(s): top-k chunk retrieval with doc-number and series filtering; hybrid search (vector + existing keyword/ILIKE) preferred.
- FR-1.4: Agent context builder consumes retrieved chunks (with doc provenance) instead of truncated whole-doc concatenation; enforce a token budget.
- FR-1.5: Re-ingestion must re-chunk/re-embed only changed documents (file_hash already supports this).

### FR-2 — Agent Fleet
Implement doctrine agents incrementally behind the existing `AGENT_FUNCTIONS` registry pattern:
- FR-2.1: Priority order driven by the router's own declared handoffs: `writer` (Doc 316/320/324 instructions), `validator`/auditor (Doc 328/329 gates), then Analyst (300), Strategist (304), Architect (312).
- FR-2.2: Each agent loads its governing doctrine doc as its system-prompt source of truth (versioned — agents must stamp which doc versions they ran against, per the provenance rule in Doc 329/C17).
- FR-2.3: Structured JSON outputs persisted in `agent_tasks.output_data`; schema validated (Pydantic) before persistence.
- FR-2.4: Brand context injection from brand modules (Docs 130/131/132) when brand is detected.

### FR-3 — Pipeline Orchestration (Doc 230)
- FR-3.1: Multi-step workflows: a request enters as a "job" that chains agent tasks (router → … → writer → auditor) with state tracked per stage.
- FR-3.2: Failure routing: failed stage re-routes to the correct earlier stage (per Doc 230 If/Then rules), not simply marked failed.
- FR-3.3: Human gate: audit results (Doc 328/329-style PASS/FAIL) require explicit human approval before publish-stage steps.
- FR-3.4: Job timeline visible in frontend (stage status, artifacts, errors).

### FR-4 — Content Production Artifacts
- FR-4.1: Generated pages conform to Doc 192 (Publish-Readiness Manifest, exactly-one-file-per-version, visible JSON-LD, archetype stamp).
- FR-4.2: Pre-publication packaging audit (Doc 195 PKG checks) as an automated gate.
- FR-4.3: Artifact storage with version history (new table; do not overload `agent_tasks`).

### FR-5 — Platform UX
- FR-5.1: Dashboard replaces stub: recent jobs/tasks, corpus stats, failed-task alerts.
- FR-5.2: Doctrine search upgraded to semantic (FR-1.3) with highlighted chunk-level results.
- FR-5.3: Server-side markdown rendering (populate `content_html` at ingestion) to drop client-side react-markdown dependency on the viewer.

---

## 4. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | Security: sessions signed with `SECRET_KEY`; no default-admin auto-seed in non-dev environments (force password rotation); CORS from env config; UUID validation on all path params; rate limiting on login and agent-run endpoints |
| NFR-2 | Migrations: adopt Alembic properly (baseline revision + all future changes); `create_all()` only in seed script for fresh dev envs |
| NFR-3 | Tests: pytest suite covering auth, ingestion parsing, reference graph, agent task lifecycle, retrieval; CI-runnable |
| NFR-4 | Portability: no host-specific paths; doctrine path strictly from config; add README, `.gitignore`, `.dockerignore` |
| NFR-5 | Observability: structured logging for agent runs (model, tokens, latency, doc versions used) |
| NFR-6 | Cost control: per-task max-token budgets and model selection configurable per agent |

---

## 5. Out of Scope (for now)

- WordPress publishing automation (Doc 260) — manual publish continues until pipeline is stable.
- External seeding/distribution agents (332/336/337) — depend on live site relaunch completing.
- Multi-tenant anything — single deployment, known user base.

---

## 6. Suggested Phasing

**Phase 0 — Hardening (do first, small effort, unblocks everything)**
Fix NFR-1..4 security/portability items, Alembic baseline, minimal test scaffold, README/.gitignore/.dockerignore, remove dead deps/code.

**Phase 1 — Real RAG (FR-1)**
pgvector + chunking per Doc 122 + hybrid search + agent context rewrite. This is the highest-leverage change: every future agent inherits better grounding.

**Phase 2 — Writer + Auditor agents (FR-2.1)**
Close the loop the router already promises: router → writer → validator, with provenance stamps.

**Phase 3 — Orchestration (FR-3)** ✅ Implemented
Job model chaining tasks with failure re-routing and human gates. `AgentJob`/`JobStage` models, `orchestrator.py` state machine (router → writer → auditor, max 2 auto-revisions on audit FAIL, awaiting_approval gate), `/api/jobs` endpoints, `/jobs` + `/jobs/[jobId]` frontend.

**Phase 4 — UX & artifacts (FR-4, FR-5)**
Dashboard, artifact versioning, packaging-audit gate.

---

## 7. Open Questions

1. Which LLM models per agent tier (drafting vs. auditing)? Cost/quality tradeoff to confirm.
2. Embedding provider: Anthropic doesn't ship embeddings — pick Voyage/OpenAI/local (e.g., nomic/bge) for FR-1.2.
3. Should auditor agents hard-block (FAIL stops the job) or advisory-only initially?
4. Single Postgres instance for vectors is assumed — confirm no requirement for a dedicated vector DB at current corpus size (~700KB text; pgvector is comfortably sufficient).
