"""Learning-loop API: publication registration + performance/flag read views."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.dependencies import require_admin, require_writer
from app.models.external import ExternalExport
from app.models.job import AgentJob
from app.models.learning import ContentPerformanceSnapshot, ContentPublication, LearningSignal
from app.models.user import User
from app.services.learning_loop import register_publication, snapshot_publications

router = APIRouter()


class PublicationCreateRequest(BaseModel):
    url: str = Field(min_length=1)
    target_keyword: str | None = None
    publish_date: date | None = None


class PublicationSnapshot(BaseModel):
    period_to: str | None = None
    position: float | None = None
    clicks: int = 0
    impressions: int = 0
    ctr: float | None = None
    ai_overview_impressions: int = 0
    calls: int = 0
    est_visits: int | None = None
    movement: float | None = None
    movement_ctr: float | None = None
    movement_impressions: int | None = None
    flags: list[str] = Field(default_factory=list)


class PublicationResponse(BaseModel):
    id: str
    job_id: str
    job_title: str
    publish_url: str
    publish_date: str | None = None
    target_keyword: str | None = None
    status: str
    created_at: str
    latest: PublicationSnapshot | None = None


class PublicationsResponse(BaseModel):
    publications: list[PublicationResponse] = Field(default_factory=list)


class SignalResponse(BaseModel):
    id: str
    publication_id: str
    publish_url: str
    source: str
    observation: str
    action_taken: str | None = None
    result: str | None = None
    created_at: str


class FlagsResponse(BaseModel):
    count: int = 0
    signals: list[SignalResponse] = Field(default_factory=list)


class RecomputeResponse(BaseModel):
    publications: int = 0
    snapshots: int = 0
    signals: int = 0


def _latest_snapshot(db: DBSession, pub_id: UUID) -> ContentPerformanceSnapshot | None:
    return (
        db.query(ContentPerformanceSnapshot)
        .join(ExternalExport, ExternalExport.id == ContentPerformanceSnapshot.source_export_id)
        .filter(ContentPerformanceSnapshot.publication_id == pub_id)
        .order_by(ExternalExport.imported_at.desc(), ExternalExport.id.desc())
        .first()
    )


def _snapshot_model(snap: ContentPerformanceSnapshot | None) -> PublicationSnapshot | None:
    if snap is None:
        return None
    return PublicationSnapshot(
        period_to=snap.period_to.isoformat() if snap.period_to else None,
        position=snap.position,
        clicks=snap.clicks,
        impressions=snap.impressions,
        ctr=snap.ctr,
        ai_overview_impressions=snap.ai_overview_impressions,
        calls=snap.calls,
        est_visits=snap.est_visits,
        movement=snap.movement,
        movement_ctr=snap.movement_ctr,
        movement_impressions=snap.movement_impressions,
        flags=snap.flags or [],
    )


def _publication_model(db: DBSession, pub: ContentPublication) -> PublicationResponse:
    job = db.query(AgentJob).filter(AgentJob.id == pub.job_id).first()
    return PublicationResponse(
        id=str(pub.id),
        job_id=str(pub.job_id),
        job_title=job.title if job else "",
        publish_url=pub.publish_url,
        publish_date=pub.publish_date.isoformat() if pub.publish_date else None,
        target_keyword=pub.target_keyword,
        status=pub.status,
        created_at=pub.created_at.isoformat() if pub.created_at else "",
        latest=_snapshot_model(_latest_snapshot(db, pub.id)),
    )


@router.get("/publications", response_model=PublicationsResponse)
def list_publications(
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    pubs = db.query(ContentPublication).order_by(ContentPublication.created_at.desc()).limit(200).all()
    return PublicationsResponse(publications=[_publication_model(db, p) for p in pubs])


@router.post("/jobs/{job_id}/publication", response_model=PublicationResponse, status_code=201)
def create_publication(
    job_id: UUID,
    body: PublicationCreateRequest,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        pub = register_publication(
            db,
            job_id=job_id,
            url=body.url,
            published_at=body.publish_date,
            keyword=body.target_keyword,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    # A publish may already be reflected in the current weekly data.
    snapshot_publications(db)
    return _publication_model(db, pub)


@router.get("/learning/flags", response_model=FlagsResponse)
def list_signals(
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db),
):
    rows = (
        db.query(LearningSignal, ContentPublication.publish_url)
        .join(ContentPublication, ContentPublication.id == LearningSignal.publication_id)
        .order_by(LearningSignal.created_at.desc())
        .limit(200)
        .all()
    )
    signals = [
        SignalResponse(
            id=str(sig.id),
            publication_id=str(sig.publication_id),
            publish_url=url or "",
            source=sig.source,
            observation=sig.observation,
            action_taken=sig.action_taken,
            result=sig.result,
            created_at=sig.created_at.isoformat() if sig.created_at else "",
        )
        for sig, url in rows
    ]
    return FlagsResponse(count=len(signals), signals=signals)


@router.post("/learning/recompute", response_model=RecomputeResponse)
def recompute_snapshots(
    admin: User = Depends(require_admin),
    db: DBSession = Depends(get_db),
):
    """Re-run the weekly performance snapshot for every registered publication."""
    stats = snapshot_publications(db)
    return RecomputeResponse(
        publications=stats.get("publications", 0),
        snapshots=stats.get("snapshots", 0),
        signals=stats.get("signals", 0),
    )
