import json
import pytest

from app.models.agent_task import AgentTask
from app.models.job import AgentJob, JobStage
from app.services import orchestrator
from app.services.orchestrator import (
    create_job,
    advance_job,
    approve_job,
    cancel_job,
)


@pytest.fixture(autouse=True)
def no_celery(monkeypatch):
    """Stage dispatch must not hit Redis in unit tests."""
    recorded = []
    monkeypatch.setattr(
        "app.tasks.run_agent_task.delay",
        lambda *args, **kwargs: recorded.append(args),
    )
    return recorded


def complete_stage(db, task: AgentTask, output: dict | None = None,
                   status: str = "completed", error: str | None = None):
    task.status = status
    task.output_data = output
    task.error_message = error
    db.commit()
    return advance_job(db, task)


def latest_stage(db, job: AgentJob, agent_type: str | None = None) -> JobStage:
    query = db.query(JobStage).filter(JobStage.job_id == job.id)
    if agent_type:
        query = query.filter(JobStage.agent_type == agent_type)
    return query.order_by(JobStage.sequence.desc()).first()


def stage_task(db, stage: JobStage) -> AgentTask:
    return db.query(AgentTask).filter(AgentTask.id == stage.task_id).first()


ROUTER_OUTPUT = {
    "intent": "brand_evaluation",
    "brand": "mastershield",
    "content_type": "comparison",
    "applicable_docs": ["100", "130", "316"],
    "next_agent": "writer",
    "confidence": 0.9,
}

WRITER_OUTPUT = {
    "agent": "writer",
    "provenance": [],
    "output": {"title": "T", "meta_title": "MT", "meta_description": "MD",
               "content_markdown": "# T\n\nDraft."},
}

AUDIT_FINDINGS = [{"check": "FAQ count", "severity": "major",
                   "status": "fail", "notes": "Only 2 questions above fold."}]


def test_create_job_dispatches_router_stage(db_session, test_user, no_celery):
    job = create_job(db_session, created_by=test_user.id, request="Write a comparison page about gutter guards")
    assert job.status == "running"
    assert job.revision_count == 0

    stage = latest_stage(db_session, job)
    assert stage.agent_type == "router"
    assert stage.sequence == 1
    assert stage.task_id is not None
    assert no_celery  # dispatch was recorded, not executed


def test_router_completion_dispatches_writer_with_routing_context(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a comparison page")
    router_task = stage_task(db_session, latest_stage(db_session, job))

    job = complete_stage(db_session, router_task, ROUTER_OUTPUT)

    writer_stage = latest_stage(db_session, job, "writer")
    assert writer_stage is not None
    assert writer_stage.sequence == 2
    writer_input = stage_task(db_session, writer_stage).input_data
    assert writer_input["brand"] == "mastershield"
    assert writer_input["content_type"] == "comparison"
    assert writer_input["applicable_docs"] == ["100", "130", "316"]
    assert job.brand == "mastershield"


def test_writer_completion_dispatches_auditor_with_source_task(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a comparison page")
    complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job)), ROUTER_OUTPUT)
    writer_task = stage_task(db_session, latest_stage(db_session, job, "writer"))

    job = complete_stage(db_session, writer_task, WRITER_OUTPUT)

    audit_stage = latest_stage(db_session, job, "auditor")
    assert audit_stage is not None
    audit_input = stage_task(db_session, audit_stage).input_data
    assert audit_input["source_task_id"] == str(writer_task.id)


def test_audit_pass_goes_to_awaiting_approval(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a comparison page")
    complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job)), ROUTER_OUTPUT)
    complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job, "writer")), WRITER_OUTPUT)

    verdict_output = {"agent": "auditor", "output": {"verdict": "pass_with_notes",
                                                     "summary": "ok", "findings": []}}
    job = complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job, "auditor")), verdict_output)

    assert job.status == "awaiting_approval"


def test_audit_fail_routes_back_to_writer_with_feedback(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a comparison page")
    complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job)), ROUTER_OUTPUT)
    complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job, "writer")), WRITER_OUTPUT)
    fail_output = {"agent": "auditor", "output": {"verdict": "fail",
                                                  "summary": "issues", "findings": AUDIT_FINDINGS}}

    job = complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job, "auditor")), fail_output)

    assert job.status == "running"
    assert job.revision_count == 1
    revision_stage = latest_stage(db_session, job, "writer")
    assert revision_stage.sequence > 2  # a new writer stage was appended
    assert "Only 2 questions above fold" in revision_stage.feedback
    revision_input = stage_task(db_session, revision_stage).input_data
    assert revision_input["revision_feedback"] == revision_stage.feedback


def test_audit_fail_exhausts_revisions_then_fails(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a comparison page")
    fail_output = {"agent": "auditor", "output": {"verdict": "fail",
                                                  "summary": "still bad", "findings": AUDIT_FINDINGS}}

    complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job)), ROUTER_OUTPUT)
    for _ in range(job.max_revisions + 1):  # initial write + all revisions
        complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job, "writer")), WRITER_OUTPUT)
        job = complete_stage(db_session, stage_task(db_session, latest_stage(db_session, job, "auditor")), fail_output)
        if job.status != "running":
            break

    assert job.status == "failed"
    assert job.revision_count == job.max_revisions
    assert "Escalated" in job.notes


def test_stage_error_fails_job(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a page")
    router_task = stage_task(db_session, latest_stage(db_session, job))
    job = complete_stage(db_session, router_task, None, status="failed", error="LLM timeout")
    assert job.status == "failed"
    assert "LLM timeout" in job.notes


def test_approve_only_from_awaiting_approval(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a page")
    with pytest.raises(ValueError, match="awaiting approval"):
        approve_job(db_session, job)

    job.status = "awaiting_approval"
    db_session.commit()
    approved = approve_job(db_session, job)
    assert approved.status == "approved"


def test_cancel_stops_advancement(db_session, test_user):
    job = create_job(db_session, created_by=test_user.id, request="Write a page")
    cancel_job(db_session, job)

    router_task = stage_task(db_session, latest_stage(db_session, job))
    job = complete_stage(db_session, router_task, ROUTER_OUTPUT)

    assert job.status == "cancelled"
    assert latest_stage(db_session, job).status == "skipped"
    # No writer stage was dispatched after cancellation.
    assert latest_stage(db_session, job, "writer") is None


def test_advance_ignores_standalone_tasks(db_session, test_user):
    task = AgentTask(agent_type="router", status="completed",
                     input_data={}, output_data=ROUTER_OUTPUT, created_by=test_user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    assert advance_job(db_session, task) is None


def test_advance_job_redelivery_does_not_duplicate_next_stage(db_session, test_user):
    """Fix 5B: a redelivered stage task must not re-dispatch the next stage.

    With acks_late + reject_on_worker_lost, a worker that dies just after
    committing a stage completion gets its agent task redelivered and
    ``advance_job`` re-run in the SAME job. Guard 1 (stage already completed)
    turns that re-entry into a no-op so the next stage (writer) is dispatched
    exactly once — no duplicate writer stage, no duplicate AgentTask, and the
    unique (job_id, sequence) constraint stays satisfied.
    """
    job = create_job(db_session, created_by=test_user.id, request="Write a page")
    router_task = stage_task(db_session, latest_stage(db_session, job))
    writer_before = db_session.query(JobStage).filter(
        JobStage.job_id == job.id, JobStage.agent_type == "writer"
    ).count()

    job = complete_stage(db_session, router_task, ROUTER_OUTPUT)

    writer_mid = db_session.query(JobStage).filter(
        JobStage.job_id == job.id, JobStage.agent_type == "writer"
    ).count()
    assert writer_mid == writer_before + 1

    # Crash-window redelivery: the same (already advanced) router task comes
    # back. advance_job must short-circuit instead of dispatching writer again.
    job = advance_job(db_session, router_task)

    writer_after = db_session.query(JobStage).filter(
        JobStage.job_id == job.id, JobStage.agent_type == "writer"
    ).count()
    assert writer_after == writer_mid == writer_before + 1
    assert job.status in ("running", "awaiting_approval")
