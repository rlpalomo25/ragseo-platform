"""Celery task glue: scheduled tasks call the real services (not themselves),
and every beat-schedule entry resolves to a registered task name.

Regression (Fix 7): tasks.reconcile_doctrine used to SHADOW the
doc_ingestion import, so the task body self-called the bound celery task
with the session as a positional arg -> TypeError on every hourly run.
"""

from contextlib import contextmanager

import app.tasks as tasks
import pytest
from app.celery_app import celery_app


class _FakeSession:
    def close(self):
        passes = getattr(self, "_closed", False)
        self._closed = True
        return passes


@pytest.fixture(autouse=True)
def fake_task_session(monkeypatch):
    """Eagerly run scheduled-task bodies without a real DB / Redis."""

    @contextmanager
    def _fake_scope():
        yield _FakeSession()

    monkeypatch.setattr(tasks, "session_scope", _fake_scope)


def test_reconcile_doctrine_task_calls_service_not_self(monkeypatch):
    seen = []
    monkeypatch.setattr(
        tasks,
        "reconcile_doctrine_service",
        lambda db: (seen.append(db), {"created": 2, "missing": 0, "superseded": 0, "errors": []})[1],
    )
    result = tasks.reconcile_doctrine.apply()
    assert result.get()["created"] == 2
    assert len(seen) == 1 and isinstance(seen[0], _FakeSession)


def test_prune_sessions_task_calls_service(monkeypatch):
    seen = []
    monkeypatch.setattr(
        tasks,
        "prune_expired_sessions",
        lambda db: (seen.append(db), 5)[1],
    )
    result = tasks.prune_sessions_task.apply()
    assert result.get() == {"deleted": 5}
    assert len(seen) == 1 and isinstance(seen[0], _FakeSession)


def test_sweep_stale_task_calls_service(monkeypatch):
    seen = []
    monkeypatch.setattr(
        tasks,
        "sweep_stale_tasks",
        lambda db: (seen.append(db), {"stale_tasks": 2, "stale_after_seconds": 1800})[1],
    )
    result = tasks.sweep_stale_tasks_task.apply()
    assert result.get()["stale_tasks"] == 2
    assert len(seen) == 1 and isinstance(seen[0], _FakeSession)


def test_beat_schedule_entries_all_registered():
    celery_app.loader.import_default_modules()
    registered = set(celery_app.tasks.keys())
    schedule = celery_app.conf.beat_schedule

    assert "doctrine-reconcile-hourly" in schedule
    assert schedule["doctrine-reconcile-hourly"]["task"] == "doctrine.reconcile"
    assert "session-prune" in schedule
    assert schedule["session-prune"]["task"] == "auth.prune_sessions"
    assert "task-sweeper" in schedule
    assert schedule["task-sweeper"]["task"] == "pipeline.sweep_stale"

    for entry in schedule.values():
        assert entry["task"] in registered
