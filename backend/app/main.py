from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, documents, agents, jobs, stats, ingest
from app.config import get_settings

settings = get_settings()
app = FastAPI(title="RAGSEO Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(documents.router, prefix="/api/docs", tags=["documents"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(ingest.router, prefix="/api", tags=["ingest"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
