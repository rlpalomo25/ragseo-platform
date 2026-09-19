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
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session as DBSession

from app.models.agent_task import AgentTask
from app.models.job import AgentJob, JobStage

logger = logging.getLogger(__name__)

# Celery hard task limit is 900s (task_time_limit). A task still `running`
# past this is a zombie (worker lost / revoked on connection loss); the
# sweeper reclaims these. 30 min leaves comfortable drift vs. the limit.
STALE_RUNNING_AFTER = timedelta(minutes=30)


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

    _dispatch_stage(
        db,
        job,
        "router",
        {
            "request": request,
        },
    )
    return job


def _dispatch_stage(
    db: DBSession, job: AgentJob, agent_type: str, input_data: dict, feedback: str | None = None
) -> JobStage:
    from app.tasks import run_agent_task  # deferred: avoids circular import

    last_seq = (
        db.query(JobStage.sequence)
        .filter(JobStage.job_id == job.id)
        .order_by(JobStage.sequence.desc())
        .first()
    )
    sequence = (last_seq[0] + 1) if last_seq else 1

    # Guard (Fix 5B): every dispatch path funnels through here, so the
    # crash-window redelivery re-entry is handled in one place. If a prior
    # (committed) run on the SAME job already dispatched this exact next stage
    # and its AgentTask, reuse that dispatch instead of creating a duplicate —
    # which would otherwise (a) double-queue an LLM agent run and (b) violate
    # uq_job_stages_job_sequence once the worker that died was redelivered.
    existing = (
        db.query(JobStage)
        .filter(
            JobStage.job_id == job.id,
            JobStage.sequence == sequence,
        )
        .first()
    )
    if existing is not None and existing.task_id is not None:
        logger.info(
            "_dispatch_stage: seq=%s already dispatched for job %s (redelivery) — reusing",
            sequence,
            job.id,
        )
        return existing

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
    stage = db.query(JobStage).filter(JobStage.task_id == task.id).first()
    if not stage:
        return None

    job = db.query(AgentJob).filter(AgentJob.id == stage.job_id).first()
    if not job:
        return None

    # Guard 1 (Fix 5B): the pipeline runs tasks with acks_late +
    # reject_on_worker_lost, so a worker that dies around a stage completion
    # gets that agent task redelivered and `advance_job` re-entered IN THE
    # SAME job. Two distinct crash windows:
    #   (a) advance already landed  -> must NOT re-dispatch the next stage
    #       (that would double LLM spend and double revision_count bumps);
    #   (b) worker died AFTER run_agent committed "completed" but BEFORE
    #       advance_job persisted the next stage -> the pipeline would stall
    #       forever with the job stuck in "running" unless we resume it here.
    # "completed" is therefore a no-op ONLY when the advancement actually
    # landed: the next stage exists, or the auditor already moved the job off
    # "running" (awaiting_approval / failed terminal) without a next stage.
    if stage.status == "completed":
        next_exists = (
            db.query(JobStage)
            .filter(
                JobStage.job_id == job.id,
                JobStage.sequence == stage.sequence + 1,
            )
            .first()
            is not None
        )
        auditor_terminal = stage.agent_type == "auditor" and job.status in ("awaiting_approval", "failed")
        if next_exists or auditor_terminal:
            logger.info(
                "advance_job: stage %s already advanced (redelivery) — no-op",
                stage.sequence,
            )
            return job
        logger.info(
            "advance_job: stage %s completed but never advanced (crash window) — resuming",
            stage.sequence,
        )

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
        _dispatch_stage(
            db,
            job,
            "writer",
            {
                "request": job.request,
                "brand": output.get("brand"),
                "content_type": output.get("content_type"),
                "intent": output.get("intent"),
                "applicable_docs": output.get("applicable_docs") or [],
            },
        )

    elif stage.agent_type == "writer":
        _dispatch_stage(
            db,
            job,
            "auditor",
            {
                "source_task_id": str(task.id),
                "brand": job.brand,
                "content_type": job.content_type,
            },
        )

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
        _dispatch_stage(
            db,
            job,
            "writer",
            {
                "request": job.request,
                "brand": job.brand,
                "content_type": job.content_type,
                "applicable_docs": router_output.get("applicable_docs") or [],
                "revision_feedback": feedback,
            },
            feedback=feedback,
        )
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


def sweep_stale_tasks(
    db: DBSession,
    stale_after: timedelta = STALE_RUNNING_AFTER,
) -> dict:
    """Reclaim AgentTasks stuck in ``running`` and fail their jobs (Fix 5).

    With ``acks_late`` + ``reject_on_worker_lost`` Celery redelivers lost
    tasks, but ``worker_cancel_long_running_tasks_on_connection_loss`` revokes
    (never redelivers) the tasks of a worker that drops its connection, and a
    hard ``task_time_limit`` kill loses the message entirely. Either way a row
    is left permanently ``running`` with no completion — cleanly visible only
    by idleness. Celery's hard limit is 900s, so anything still running past
    ``stale_after`` (default 30 min) is a zombie.

    Each reclaimed task is marked ``failed`` (with the reason), then
    ``advance_job`` routes it: stage -> failed, job -> failed. Per-task commit
    keeps a later failure from losing earlier work.
    """
    cutoff = datetime.now(UTC) - stale_after
    stale_tasks = (
        db.query(AgentTask)
        .filter(
            AgentTask.status == "running",
            AgentTask.started_at < cutoff,
        )
        .all()
    )

    for task in stale_tasks:
        task.status = "failed"
        task.completed_at = datetime.now(UTC)
        task.error_message = (
            "sweeper: task stayed 'running' past "
            f"{int(stale_after.total_seconds())}s (celery hard limit is 900s); "
            "marked failed and routed to job failure (worker loss / revocation)."
        )
        db.commit()
        try:
            advance_job(db, task)
        except Exception:
            logger.exception("sweep_stale_tasks: advance_job failed for task %s", task.id)

    db.commit()
    return {"stale_tasks": len(stale_tasks), "stale_after_seconds": int(stale_after.total_seconds())}
