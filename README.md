# RAGSEO Platform

Content-production platform that operationalizes the RAGSEO doctrine library
(`../Doc *.md`): it ingests the doctrine corpus into a searchable, chunked,
embedding-backed store and routes content requests through AI agents grounded
in retrieved doctrine.

**Stack:** FastAPI · PostgreSQL 16 + pgvector · Redis/Celery · Next.js 14 · Ollama embeddings (local, default) · Anthropic Claude

## Quick start

```bash
cp .env.example .env          # fill in ANTHROPIC_API_KEY; VOYAGE_API_KEY optional
docker compose up --build     # migrations run automatically on backend start
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/api/health
- Seed admin + ingest doctrine: `docker compose exec backend python scripts/seed.py`

Default dev login: `admin` / `changeme` (blocked in production unless
`DEFAULT_ADMIN_PASSWORD` is changed).

## Embeddings & retrieval

**Default: fully local.** docker-compose runs an `ollama` service and pulls
`nomic-embed-text` (768-dims) on first start. Ingestion
chunks every doctrine document per Doc 122 (context-independent, heading-aligned
chunks), embeds them via Ollama's local HTTP API, and search/agent-context use
hybrid retrieval (pgvector cosine + keyword, fused via RRF).
(Note: Ollama clamps every `nomic-embed-text` tag — including `v1.5` — to a
2048-token context. The backend embeds oversized doctrine chunks (kept whole per
Doc 122) using their head window only; keyword/LLM search still sees full text.
Tune `EMBEDDING_CHARS_PER_TOKEN` (default 4.0) to trade vector length for fidelity.)

**Optional Voyage AI** instead: set `EMBEDDING_PROVIDER=voyage`,
`VOYAGE_API_KEY`, `EMBEDDING_MODEL=voyage-3-lite`,
`EMBEDDING_DIMENSIONS=1024` in `.env`, restart, and re-ingest (see below).

**No provider at all** (`EMBEDDING_PROVIDER=none` or nothing configured):
everything still works — chunks are stored without vectors and retrieval falls
back to keyword-only.

**After switching providers or changing models/dimensions**, a new Alembic
migration may be required (the vector column dimension and HNSW index are fixed
at migration time) and the corpus must be re-embedded: restart, then hit
`POST /api/docs/reingest` as admin. Re-ingest re-embeds unchanged documents
whenever their chunks are missing vectors, so a provider change backfills cleanly.

## Layout

```
backend/
  app/
    models/        # User, Session, Document, DocReference, AgentTask, DocChunk, AgentJob, JobStage
    routers/       # auth, users, documents (+ hybrid search), agents, jobs
    services/      # chunking (Doc 122), embeddings (Ollama/Voyage), retrieval (RRF),
                   # doc_ingestion, agent_runner, llm_client, doctrine loader,
                   # agents/{router,writer,auditor}, orchestrator
    tasks.py       # Celery agent registry (AGENT_FUNCTIONS) + pipeline advancement
  alembic/         # migrations (0001_baseline, 0002_jobs)
  scripts/seed.py  # create tables + default admin + doctrine ingestion
frontend/          # Next.js App Router: /login /docs /jobs /agents /admin/users
doctrine/          # mount point; docker-compose bind-mounts ../ read-only
```

## Common commands

```bash
# Re-run doctrine ingestion (admin endpoint or CLI)
curl -X POST http://localhost:8000/api/docs/reingest -b "session_token=..."
docker compose exec backend python scripts/ingest_docs.py

# Migrations
docker compose exec backend alembic upgrade head

# Backend tests (unit suite runs on SQLite; integration tests need Postgres+pgvector)
cd backend && pip install -r requirements.txt && pytest -m "not integration"
```

See `REQUIREMENTS.md` for the roadmap and `IMPLEMENTATION_PLAN.md` for current
status, verification log, and next steps.

## License

**Proprietary — paid commercial software.** RAGSEO Platform is not open
source. Use, modification, and distribution are governed by the license you
purchased. You must have a valid paid license to run this software. See
`LICENSE` for the full terms; contact the maintainer for licensing.
