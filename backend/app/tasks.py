import logging
from uuid import UUID

from app.celery_app import celery_app
from app.database import session_scope
from app.services.agent_runner import run_agent
from app.services.agents.auditor import run_auditor
from app.services.agents.router import run_router
from app.services.agents.writer import run_writer
from app.services.auth_service import prune_expired_sessions
from app.services.doc_ingestion import reconcile_doctrine as reconcile_doctrine_service
from app.services.orchestrator import advance_job, sweep_stale_tasks

logger = logging.getLogger(__name__)

AGENT_FUNCTIONS = {
    "router": run_router,
    "writer": run_writer,
    "auditor": run_auditor,
}


@celery_app.task(name="agents.run_agent_task", bind=True)
def run_agent_task(self, task_id: str, agent_type: str, input_data: dict):
    with session_scope() as db:
        agent_fn = AGENT_FUNCTIONS.get(agent_type)
        if not agent_fn:
            raise ValueError(f"Unknown agent type: {agent_type}")

        task = run_agent(
            db=db,
            task_id=UUID(task_id),
            agent_fn=agent_fn,
            input_data=input_data,
        )

        # Advance the pipeline if this task belongs to a job. Orchestration
        # errors must not lose the already-persisted task result.
        try:
            advance_job(db, task)
        except Exception:
            logger.exception("Orchestration failed after task %s (%s)", task_id, agent_type)

        return {"task_id": str(task.id), "status": task.status}


@celery_app.task(name="doctrine.reconcile", bind=True)
def reconcile_doctrine(self):
    """Scheduled task to reconcile doctrine DB with filesystem."""
    with session_scope() as db:
        try:
            stats = reconcile_doctrine_service(db)
        except Exception:
            logger.exception("Doctrine reconciliation failed")
            raise
        logger.info("Doctrine reconciliation completed: %s", stats)
        return stats


@celery_app.task(name="auth.prune_sessions", bind=True)
def prune_sessions_task(self):
    """Scheduled task to clean up expired sessions."""
    with session_scope() as db:
        try:
            count = prune_expired_sessions(db)
        except Exception:
            logger.exception("Session pruning failed")
            raise
        logger.info("Session pruning completed: %d expired sessions deleted", count)
        return {"deleted": count}


@celery_app.task(name="pipeline.sweep_stale", bind=True)
def sweep_stale_tasks_task(self):
    """Scheduled task to reclaim AgentTasks stuck in ``running`` (Fix 5)."""
    with session_scope() as db:
        try:
            stats = sweep_stale_tasks(db)
        except Exception:
            logger.exception("Sweep of stale running tasks failed")
            raise
        if stats["stale_tasks"]:
            logger.info("Sweep reclaimed %d stale running tasks", stats["stale_tasks"])
        return stats
