from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "ragseo",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    # A hung LLM call must not permanently occupy one of the two worker slots.
    # Hard-limit worker loss is deliberate: with acks_late + reject_on_worker_lost
    # the task is redelivered and run_agent re-runs, resetting a stale running row.
    task_soft_time_limit=600,
    task_time_limit=900,
    task_reject_on_worker_lost=True,
    worker_cancel_long_running_tasks_on_connection_loss=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
    result_expires=60 * 60,
    beat_schedule={
        # Registered task name is "doctrine.reconcile" (explicit name= in
        # app/tasks.py); beat must reference that, not the module path — the
        # old "app.tasks.reconcile_doctrine" never matched a registered task
        # so the hourly reconcile silently never ran.
        "doctrine-reconcile-hourly": {
            "task": "doctrine.reconcile",
            "schedule": crontab(minute=0),  # hourly at :00
        },
        # Fix 8: prune_expired_sessions was implemented but never scheduled.
        # Sessions expire after session_expiry_hours (24h), so every 6h is
        # far more frequent than needed; picks up stragglers promptly anyway.
        "session-prune": {
            "task": "auth.prune_sessions",
            "schedule": crontab(minute=30, hour="*/6"),
        },
        # Fix 5: reclaim AgentTasks stuck in `running` (worker lost / revoked
        # on connection loss). Runs every 5 min; cheap scan on an indexed
        # status column, only acting on tasks idle past the 30-min threshold.
        "task-sweeper": {
            "task": "pipeline.sweep_stale",
            "schedule": crontab(minute="*/5"),
        },
    },
)
