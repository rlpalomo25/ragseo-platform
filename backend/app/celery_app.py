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
        "doctrine-reconcile-hourly": {
            "task": "app.tasks.reconcile_doctrine",
            "schedule": crontab(minute=0),  # hourly at :00
        },
    },
)
