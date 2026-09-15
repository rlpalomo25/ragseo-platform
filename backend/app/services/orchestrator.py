"""Pipeline orchestration: jobs, stage chaining, failure routing (Doc 230).

Flow: router -> writer -> auditor -> human gate.
- Audit PASS / PASS_WITH_NOTES  => job awaits human approval.
- Audit FAIL                    => back to writer with findings as revision
                                   feedback, up to max_revisions, then the job
                                   fails with an escalation note.
- Task-level errors (infra/LLM) => job fails; content-quality failures are
                                   audit verdicts, not exceptions.
"""
import logging

from sqlalchemy.orm import Session as DBSession

from app.models.job import AgentJob, JobStage
from app.models.agent_task import AgentTask

logger = logging.getLogger(__name__)


def create_job(
    db: DBSession,
    created_by,
    request: str,
    title: str | None = None,
    brand: str | None = None,
    content_type: str | None = None,
    max_revisions: int = 2,
) -> AgentJob:
    job = AgentJob(
        title=title or (request[:80] + ("…" if len(request) > 80 else "")),
        request=request,
        brand=brand,
        content_type=content_type,
        status="running",
        max_revisions=max_revisions,
        created_by=created_by,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    _dispatch_stage(db, job, "router", {
        "request": request,
    })
    return job


def _dispatch_stage(db: DBSession, job: AgentJob, agent_type: str,
                    input_data: dict, feedback: str | None = None) -> JobStage:
    from app.tasks import run_agent_task  # deferred: avoids circular import

    last_seq = db.query(JobStage.sequence).filter(
        JobStage.job_id == job.id
    ).order_by(JobStage.sequence.desc()).first()
    sequence = (last_seq[0] + 1) if last_seq else 1

    stage = JobStage(
        job_id=job.id,
        sequence=sequence,
        agent_type=agent_type,
        status="pending",
        feedback=feedback,
    )
    db.add(stage)
    db.flush()

    task = AgentTask(
        agent_type=agent_type,
        status="pending",
        input_data=input_data,
        created_by=job.created_by,
    )
    db.add(task)
    db.flush()

    stage.task_id = task.id
    db.commit()
    db.refresh(stage)

    run_agent_task.delay(str(task.id), agent_type, input_data)
    return stage


def advance_job(db: DBSession, task: AgentTask) -> AgentJob | None:
    """Route the pipeline after a stage task finishes. No-op for standalone tasks."""
    stage = (
        db.query(JobStage)
        .filter(JobStage.task_id == task.id)
        .first()
    )
    if not stage:
        return None

    job = db.query(AgentJob).filter(AgentJob.id == stage.job_id).first()
    if not job:
        return None

    if job.status == "cancelled":
        stage.status = "skipped"
        db.commit()
        return job

    if task.status == "failed":
        stage.status = "failed"
        job.status = "failed"
        job.notes = f"Stage '{stage.agent_type}' errored: {(task.error_message or '')[:500]}"
        db.commit()
        return job

    stage.status = "completed"

    if stage.agent_type == "router":
        output = task.output_data or {}
        job.brand = job.brand or output.get("brand")
        job.content_type = job.content_type or output.get("content_type")
        _dispatch_stage(db, job, "writer", {
            "request": job.request,
            "brand": output.get("brand"),
            "content_type": output.get("content_type"),
            "intent": output.get("intent"),
            "applicable_docs": output.get("applicable_docs") or [],
        })

    elif stage.agent_type == "writer":
        _dispatch_stage(db, job, "auditor", {
            "source_task_id": str(task.id),
            "brand": job.brand,
            "content_type": job.content_type,
        })

    elif stage.agent_type == "auditor":
        _handle_audit_result(db, job, task)

    db.commit()
    db.refresh(job)
    return job


def _handle_audit_result(db: DBSession, job: AgentJob, task: AgentTask) -> None:
    output = (task.output_data or {}).get("output") or {}
    verdict = output.get("verdict")

    if verdict in ("pass", "pass_with_notes"):
        job.status = "awaiting_approval"
        return

    # FAIL -> revision loop.
    if job.revision_count < job.max_revisions:
        job.revision_count += 1
        feedback = _format_findings(output.get("findings") or [])
        router_output = _router_output(db, job) or {}
        _dispatch_stage(db, job, "writer", {
            "request": job.request,
            "brand": job.brand,
            "content_type": job.content_type,
            "applicable_docs": router_output.get("applicable_docs") or [],
            "revision_feedback": feedback,
        }, feedback=feedback)
    else:
        job.status = "failed"
        job.notes = (
            f"Audit returned FAIL after {job.max_revisions} revision(s). "
            "Escalated for human review. Last findings: "
            + _format_findings(output.get("findings") or [])[:800]
        )


def _format_findings(findings: list[dict]) -> str:
    lines = []
    for f in findings:
        lines.append(
            f"- [{f.get('severity', 'minor')}/{f.get('status', 'warn')}] "
            f"{f.get('check', 'unnamed check')}: {f.get('notes', '')}"
        )
    return "\n".join(lines) or "(no findings provided)"


def _router_output(db: DBSession, job: AgentJob) -> dict | None:
    stage = (
        db.query(JobStage)
        .filter(JobStage.job_id == job.id, JobStage.agent_type == "router")
        .order_by(JobStage.sequence.desc())
        .first()
    )
    if not stage or not stage.task_id:
        return None
    task = db.query(AgentTask).filter(AgentTask.id == stage.task_id).first()
    return task.output_data if task else None


def approve_job(db: DBSession, job: AgentJob) -> AgentJob:
    if job.status != "awaiting_approval":
        raise ValueError(f"Job is not awaiting approval (status: {job.status})")
    job.status = "approved"
    db.commit()
    db.refresh(job)
    return job


def cancel_job(db: DBSession, job: AgentJob) -> AgentJob:
    if job.status not in ("running", "awaiting_approval", "failed"):
        raise ValueError(f"Job cannot be cancelled from status: {job.status}")
    job.status = "cancelled"
    db.commit()
    db.refresh(job)
    return job
