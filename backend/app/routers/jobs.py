from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.models.user import User
from app.models.job import AgentJob, JobStage
from app.models.agent_task import AgentTask
from app.dependencies import get_current_user, require_writer
from app.services.orchestrator import create_job, approve_job, cancel_job

router = APIRouter()


class JobCreateRequest(BaseModel):
    request: str = Field(min_length=10)
    title: str | None = None
    brand: str | None = None
    content_type: str | None = None


class JobSummary(BaseModel):
    id: str
    title: str
    status: str
    brand: str | None
    content_type: str | None
    revision_count: int
    max_revisions: int
    created_at: str
    updated_at: str


class StageDetail(BaseModel):
    id: str
    sequence: int
    agent_type: str
    task_id: str | None
    status: str
    feedback: str | None
    task_status: str | None
    output_data: dict | None
    error_message: str | None


class JobDetail(JobSummary):
    request: str
    notes: str | None
    stages: list[StageDetail]


def _summary(job: AgentJob) -> JobSummary:
    return JobSummary(
        id=str(job.id),
        title=job.title,
        status=job.status,
        brand=job.brand,
        content_type=job.content_type,
        revision_count=job.revision_count,
        max_revisions=job.max_revisions,
        created_at=job.created_at.isoformat() if job.created_at else "",
        updated_at=job.updated_at.isoformat() if job.updated_at else "",
    )


@router.post("", response_model=JobSummary, status_code=201)
def create_new_job(
    body: JobCreateRequest,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    job = create_job(
        db=db,
        created_by=user.id,
        request=body.request,
        title=body.title,
        brand=body.brand,
        content_type=body.content_type,
    )
    return _summary(job)


@router.get("")
def list_jobs(
    status: str | None = None,
    brand: str | None = None,
    content_type: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    query = db.query(AgentJob).order_by(AgentJob.created_at.desc())
    if status:
        query = query.filter(AgentJob.status == status)
    if brand:
        query = query.filter(AgentJob.brand == brand)
    if content_type:
        query = query.filter(AgentJob.content_type == content_type)
    jobs = query.limit(limit).all()
    return {"jobs": [_summary(j).model_dump() for j in jobs]}


@router.get("/{job_id}", response_model=JobDetail)
def get_job(
    job_id: UUID,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    stages = (
        db.query(JobStage)
        .filter(JobStage.job_id == job.id)
        .order_by(JobStage.sequence.asc())
        .all()
    )

    stage_details = []
    for stage in stages:
        task = (
            db.query(AgentTask).filter(AgentTask.id == stage.task_id).first()
            if stage.task_id
            else None
        )
        stage_details.append(StageDetail(
            id=str(stage.id),
            sequence=stage.sequence,
            agent_type=stage.agent_type,
            task_id=str(stage.task_id) if stage.task_id else None,
            status=stage.status,
            feedback=stage.feedback,
            task_status=task.status if task else None,
            output_data=task.output_data if task else None,
            error_message=task.error_message if task else None,
        ))

    return JobDetail(
        **_summary(job).model_dump(),
        request=job.request,
        notes=job.notes,
        stages=stage_details,
    )


@router.post("/{job_id}/approve", response_model=JobSummary)
def approve_existing_job(
    job_id: UUID,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        job = approve_job(db, job)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return _summary(job)


@router.post("/{job_id}/cancel", response_model=JobSummary)
def cancel_existing_job(
    job_id: UUID,
    user: User = Depends(require_writer),
    db: DBSession = Depends(get_db),
):
    job = db.query(AgentJob).filter(AgentJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        job = cancel_job(db, job)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return _summary(job)
