"""Security regressions for the 2026-10 audit wave.

Each test encodes the *secure* behaviour. The original exploratory probes
(tests/test_security_probe*.py) asserted that a weakness existed; they were
inverted here as each weakness was fixed, so a regression now fails a test
instead of passing a probe.

Deliberate, documented decisions (not bugs) are collected at the bottom of the
file so the rationale is not lost when the code changes.
"""

import hashlib
from datetime import UTC, datetime, timedelta

import pytest
from app.models.audit import AuditLog
from app.models.job import AgentJob
from app.models.user import Session as UserSession
from app.models.user import User

from tests.conftest import login, seed_doc

# --------------------------------------------------------------- login (SEC-01)


def test_unknown_username_still_pays_the_bcrypt_cost(client, test_user, monkeypatch):
    """A missing user must not answer measurably faster than a wrong password."""
    import app.routers.auth as auth

    calls: list[str] = []
    real_verify = auth.verify_password

    def spy(password, password_hash):
        calls.append(password_hash)
        return real_verify(password, password_hash)

    monkeypatch.setattr(auth, "verify_password", spy)
    assert login(client, "nosuchuser", "wrong").status_code == 401
    assert calls == [auth.DUMMY_PASSWORD_HASH], "unknown user skipped bcrypt"


# ------------------------------------------------------- lockout (SEC-02/18/19)


def test_fifth_failure_locks_the_account_without_a_500(client, db_session, test_user):
    for _ in range(5):
        assert login(client, "testwriter", "wrong").status_code == 401

    db_session.expire_all()
    user = db_session.query(User).filter(User.username == "testwriter").first()
    assert user.failed_login_attempts == 5
    assert user.locked_until is not None

    # The naive SQLite datetime must not raise TypeError in the lock check, and
    # the correct password is refused while locked (that is the point of a lock).
    locked = login(client, "testwriter", "secret123")
    assert locked.status_code == 401


def test_locked_account_uses_the_same_error_as_a_bad_password(client, test_user):
    """The lock branch must not be an account-existence oracle."""
    for _ in range(5):
        login(client, "testwriter", "wrong")
    wrong = login(client, "testwriter", "still-wrong")
    locked = login(client, "testwriter", "secret123")
    assert wrong.status_code == locked.status_code == 401
    assert wrong.json()["detail"] == locked.json()["detail"] == "Invalid username or password"


def test_lock_is_temporary_and_expires(client, db_session, test_user):
    for _ in range(5):
        login(client, "testwriter", "wrong")
    db_session.expire_all()
    user = db_session.query(User).filter(User.username == "testwriter").first()
    user.locked_until = datetime.now(UTC) - timedelta(seconds=1)
    db_session.commit()

    assert login(client, "testwriter", "secret123").status_code == 200


@pytest.mark.parametrize(
    ("attempts", "expected_minutes"),
    [(0, 15), (5, 15), (6, 15), (10, 60), (14, 60), (15, 240), (20, 1440), (100, 1440)],
)
def test_lock_duration_tiers_are_reachable(attempts, expected_minutes):
    from app.routers.auth import _compute_lock_duration

    assert _compute_lock_duration(attempts) == timedelta(minutes=expected_minutes)


# --------------------------------------------------------- IP throttle (SEC-03)


def test_repeated_failures_from_one_ip_are_throttled(client):
    for _ in range(10):
        assert login(client, "ghost", "wrong").status_code == 401

    throttled = login(client, "ghost", "wrong")
    assert throttled.status_code == 429
    assert throttled.headers["Retry-After"]


def test_successful_login_clears_the_ip_failure_window(client, test_user):
    # Four failures: below the per-account lock, so the success can happen.
    for _ in range(4):
        login(client, "testwriter", "wrong")
    assert login(client, "testwriter", "secret123").status_code == 200
    # A fresh account from the same IP is not punished for the earlier failures.
    for _ in range(10):
        assert login(client, "other-ghost", "wrong").status_code == 401


# ------------------------------------------------------- failed-login audit (SEC-21)


def test_failed_logins_are_audited(client, db_session, test_user):
    login(client, "testwriter", "wrong")
    login(client, "ghost", "wrong")
    db_session.expire_all()

    rows = db_session.query(AuditLog).filter(AuditLog.action == "login.failed").all()
    assert len(rows) == 2
    assert {row.username for row in rows} == {"testwriter", "<anonymous>"}
    assert any("ghost" in row.detail for row in rows)


# ------------------------------------------------------------- input caps (SEC-06)


def test_login_rejects_oversized_credentials(client):
    big = "A" * 200_000
    assert client.post("/api/auth/login", json={"username": big, "password": big}).status_code == 422
    assert client.post("/api/auth/login", json={"username": "a" * 51, "password": "x"}).status_code == 422
    assert client.post("/api/auth/login", json={"username": "a", "password": "x" * 73}).status_code == 422


# -------------------------------------------------------- session tokens (SEC-07)


def test_session_tokens_are_stored_hashed(client, db_session, test_user):
    login(client, "testwriter", "secret123")
    signed = client.cookies["session_token"]
    raw = signed.rsplit(".", 1)[0]

    row = db_session.query(UserSession).first()
    assert row.token == hashlib.sha256(raw.encode()).hexdigest()
    assert raw not in row.token
    assert signed != row.token


# ----------------------------------------------------- user creation rules (SEC-16/22)


def test_create_user_rejects_weak_password_and_oversized_username(client, admin_user):
    login(client, "testadmin", "adminpass")
    assert client.post("/api/users", json={"username": "weakling", "password": "a"}).status_code == 422
    assert (
        client.post("/api/users", json={"username": "x" * 5000, "password": "secret123"}).status_code == 422
    )
    assert client.post("/api/users", json={"username": "longpw", "password": "a" * 100}).status_code == 422


def test_create_user_rejects_password_over_the_bcrypt_byte_limit(client, admin_user):
    """72 accented characters pass the character cap but exceed 72 *bytes*."""
    login(client, "testadmin", "adminpass")
    response = client.post("/api/users", json={"username": "multibyte", "password": "é" * 72})
    assert response.status_code == 400


# --------------------------------------------------------- last admin (SEC-15)


def test_last_admin_cannot_delete_themself(client, db_session, admin_user):
    login(client, "testadmin", "adminpass")
    response = client.request("DELETE", f"/api/users/{admin_user.id}")
    assert response.status_code == 409

    db_session.expire_all()
    user = db_session.query(User).filter(User.id == admin_user.id).first()
    assert user.is_active is True and user.deleted_at is None


def test_last_admin_cannot_be_demoted_or_deactivated(client, db_session, admin_user):
    login(client, "testadmin", "adminpass")
    assert client.put(f"/api/users/{admin_user.id}", json={"role": "writer"}).status_code == 409
    assert client.put(f"/api/users/{admin_user.id}", json={"is_active": False}).status_code == 409


def test_an_admin_can_be_removed_once_another_admin_exists(client, db_session, admin_user):
    from app.services.auth_service import hash_password

    second = User(username="secondadmin", password_hash=hash_password("secret123"), role="admin")
    db_session.add(second)
    db_session.commit()

    login(client, "testadmin", "adminpass")
    assert client.request("DELETE", f"/api/users/{admin_user.id}").status_code == 200


# --------------------------------------------------------- query bounds (SEC-12/13)


def test_agent_task_listing_limit_is_bounded(client, test_user):
    login(client, "testwriter", "secret123")
    assert client.get("/api/agents/tasks", params={"limit": 1_000_000_000}).status_code == 422


def test_document_search_treats_like_wildcards_as_literal_text(client, db_session, test_user):
    seed_doc(db_session, "100", "Widget handbook", "alpha bravo charlie delta echo")
    login(client, "testwriter", "secret123")

    def total(query):
        return client.get("/api/docs/search", params={"q": query}).json()["total"]

    assert total("Widget") == 1
    assert total("%") == 0
    assert total("_idget") == 0


# --------------------------------------------------------- upload types (SEC-14)


def test_external_upload_rejects_unknown_file_types(client, test_user, tmp_path, monkeypatch):
    from app.config import get_settings

    uploads = tmp_path / "uploads"
    monkeypatch.setattr(get_settings(), "external_upload_path", str(uploads))
    monkeypatch.setattr(get_settings(), "external_data_path", str(tmp_path / "baked"))

    login(client, "testwriter", "secret123")
    response = client.post(
        "/api/ingest/external/upload",
        files=[("files", ("payload.sh", b"#!/bin/sh\nid\n", "application/x-sh"))],
    )
    assert response.status_code == 400
    assert not uploads.exists() or not list(uploads.iterdir())


# --------------------------------------------------------------- CSRF (SEC-24)


def test_foreign_origin_cookie_mutation_is_rejected(client, test_user):
    login(client, "testwriter", "secret123")
    payload = {"request": "A sufficiently long attacker-controlled brief"}

    foreign = client.post("/api/jobs", json=payload, headers={"Origin": "https://evil.example"})
    assert foreign.status_code == 403

    same_origin = client.post("/api/jobs", json=payload, headers={"Origin": "http://testserver"})
    assert same_origin.status_code == 201


def test_bearer_clients_are_not_subject_to_the_origin_guard(client, test_user):
    signed = login(client, "testwriter", "secret123").json()["token"]
    client.cookies.clear()
    response = client.post(
        "/api/jobs",
        json={"request": "A sufficiently long server-to-server brief"},
        headers={"Authorization": f"Bearer {signed}", "Origin": "https://partner.example"},
    )
    assert response.status_code == 201


# ---------------------------------------------------------------------------
# Documented decisions — these are *not* vulnerabilities by intent.
#
# * Jobs and agent tasks form a shared team queue: every writer can list, read,
#   approve, retry and cancel any job. There is no per-owner concept in the UI or
#   API, and the content team works the same queue. If private per-writer jobs
#   become a requirement this must be revisited (add an owner check in
#   routers/jobs.py and routers/agents.py).
# * Weekly-export uploads are a shared team folder: any writer may delete any
#   uploaded export (baked files remain immutable). Same revisit condition.
# * /openapi.json, /api/meta/docs and /api/meta/redoc are anonymous. The deploy
#   smoke check depends on /openapi.json, and the schema contains no secrets.
# * POST /api/agents/run lets an authenticated writer supply agent input. Prompt
#   injection is an agent-design concern, not an authorization boundary: the
#   caller is already allowed to create that content through a job.
# * A per-account lockout is inherently a denial-of-service lever for a known
#   username; the per-IP throttle bounds the cost and the lock is temporary.
# ---------------------------------------------------------------------------


def test_jobs_are_a_shared_team_queue(client, db_session, test_user):
    """Documents current intent: writer B may open writer A's job."""
    from app.services.auth_service import hash_password

    victim = User(username="queueowner", password_hash=hash_password("secret123"), role="writer")
    db_session.add(victim)
    db_session.commit()
    job = AgentJob(title="Shared brief", request="Confidential plan", created_by=victim.id, status="pending")
    db_session.add(job)
    db_session.commit()

    login(client, "testwriter", "secret123")
    assert client.get(f"/api/jobs/{job.id}").status_code == 200
