"""Read-only dashboard aggregates: doctrine, embedding health, pipeline."""

from collections import Counter
from datetime import UTC, datetime
from statistics import mean

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.chunk import DocChunk
from app.models.document import Document
from app.models.job import AgentJob, JobStage
from app.models.user import User

router = APIRouter()


class DocumentsStats(BaseModel):
    total: int
    active: int
    by_doc_type: dict[str, int]
    by_series: dict[str, int]
    by_status: dict[str, int]


class ChunksStats(BaseModel):
    total: int
    embedded: int
    coverage: float


class JobsStats(BaseModel):
    total: int
    by_status: dict[str, int]
    avg_revisions: float
    with_revisions: int
    created_last_7d: int
    created_last_30d: int
    failed_stages: int


class StatsResponse(BaseModel):
    documents: DocumentsStats
    chunks: ChunksStats
    jobs: JobsStats


def _aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


@router.get("/stats", response_model=StatsResponse)
def get_stats(user: User = Depends(get_current_user), db: DBSession = Depends(get_db)):
    type_rows = db.query(Document.doc_type, func.count(Document.id)).group_by(Document.doc_type).all()
    series_rows = db.query(Document.series, func.count(Document.id)).group_by(Document.series).all()
    status_rows = db.query(Document.status, func.count(Document.id)).group_by(Document.status).all()

    chunks_total = db.query(func.count(DocChunk.id)).scalar() or 0
    chunks_embedded = db.query(func.count(DocChunk.id)).filter(DocChunk.embedding.isnot(None)).scalar() or 0

    jobs = db.query(AgentJob).all()
    now = datetime.now(UTC)
    created_times = [dt for j in jobs if (dt := _aware(j.created_at)) is not None]

    return StatsResponse(
        documents=DocumentsStats(
            total=db.query(func.count(Document.id)).scalar() or 0,
            active=db.query(func.count(Document.id)).filter(Document.status == "active").scalar() or 0,
            by_doc_type={t or "misc": n for t, n in type_rows},
            by_series={s or "misc": n for s, n in series_rows},
            by_status={s or "misc": n for s, n in status_rows},
        ),
        chunks=ChunksStats(
            total=chunks_total,
            embedded=chunks_embedded,
            coverage=round(chunks_embedded / chunks_total, 4) if chunks_total else 0.0,
        ),
        jobs=JobsStats(
            total=len(jobs),
            by_status=dict(Counter(j.status for j in jobs)),
            avg_revisions=round(mean(j.revision_count for j in jobs), 2) if jobs else 0.0,
            with_revisions=sum(1 for j in jobs if j.revision_count > 0),
            created_last_7d=sum(1 for dt in created_times if (now - dt).days < 7),
            created_last_30d=sum(1 for dt in created_times if (now - dt).days < 30),
            failed_stages=db.query(func.count(JobStage.id)).filter(JobStage.status == "failed").scalar() or 0,
        ),
    )
