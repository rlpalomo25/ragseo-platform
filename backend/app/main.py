from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.middleware import RequestBodyLimitMiddleware
from app.routers import agents, audit, auth, documents, ingest, jobs, learning, stats, users

settings = get_settings()
app = FastAPI(
    title="RAGSEO Platform",
    version="0.1.0",
    # The frontend owns /docs (Doctrine Reference), so FastAPI's interactive
    # explorers live under /api/meta to avoid colliding with the Caddy
    # /docs/* routes in front of the app. /openapi.json stays at the root so the
    # deploy smoke check in prompts/03-push-redeploy.md keeps working, and both
    # UIs reference it by absolute path.
    docs_url="/api/meta/docs",
    redoc_url="/api/meta/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # So the browser can read Content-Disposition and keep the server-chosen
    # filename on cross-origin dev (frontend :3000 -> API :8000).
    expose_headers=["Content-Disposition"],
)

# Added last, so it is outermost and runs before CORS: a 413 must not be delayed
# or have its headers mangled by the CORS layer, and the client still needs the
# readable body. Starlette applies middleware in reverse registration order.
app.add_middleware(RequestBodyLimitMiddleware)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(audit.router, prefix="/api", tags=["audit"])
app.include_router(documents.router, prefix="/api/docs", tags=["documents"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(ingest.router, prefix="/api", tags=["ingest"])
app.include_router(learning.router, prefix="/api", tags=["learning"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
