import pytest
from tests.conftest import login


def test_login_success_sets_cookie_and_returns_user(client, test_user):
    response = login(client, "testwriter", "secret123")
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["username"] == "testwriter"
    assert body["user"]["role"] == "writer"
    assert "session_token" in response.cookies


def test_login_wrong_password_rejected(client, test_user):
    assert login(client, "testwriter", "wrong").status_code == 401


def test_login_unknown_user_rejected(client, test_user):
    assert login(client, "ghost", "secret123").status_code == 401


def test_me_requires_auth(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_with_valid_session(client, test_user):
    login(client, "testwriter", "secret123")
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["username"] == "testwriter"


def test_tampered_token_rejected(client, test_user):
    login(client, "testwriter", "secret123")
    valid = client.cookies["session_token"]
    tampered = valid[:-4] + "0000"
    client.cookies.set("session_token", tampered)
    assert client.get("/api/auth/me").status_code == 401


def test_raw_unsigned_token_rejected(client, test_user, db_session):
    """A token stolen from the DB (raw form) must not authenticate."""
    from app.models.user import Session as UserSession

    login(client, "testwriter", "secret123")
    raw = db_session.query(UserSession).first().token
    client.cookies.set("session_token", raw)
    assert client.get("/api/auth/me").status_code == 401


def test_expired_session_rejected(client, test_user, db_session):
    from datetime import datetime, timedelta, timezone
    from app.models.user import Session as UserSession

    login(client, "testwriter", "secret123")
    session_row = db_session.query(UserSession).first()
    session_row.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
    db_session.commit()
    assert client.get("/api/auth/me").status_code == 401


def test_logout_deletes_current_session_only(client, test_user, db_session):
    from app.models.user import Session as UserSession

    # Two sessions for the same user.
    r1 = login(client, "testwriter", "secret123")
    first_cookie = r1.cookies["session_token"]
    r2 = login(client, "testwriter", "secret123")
    second_cookie = r2.cookies["session_token"]

    client.cookies.set("session_token", second_cookie)
    assert client.post("/api/auth/logout").status_code == 200

    remaining = db_session.query(UserSession).all()
    assert len(remaining) == 1

    # The logged-out token no longer works; the other one still does.
    client.cookies.set("session_token", second_cookie)
    assert client.get("/api/auth/me").status_code == 401
    client.cookies.set("session_token", first_cookie)
    assert client.get("/api/auth/me").status_code == 200


def test_admin_role_required_for_users_endpoint(client, test_user, admin_user):
    login(client, "testwriter", "secret123")
    assert client.get("/api/users").status_code == 403

    client.cookies.clear()
    login(client, "testadmin", "adminpass")
    assert client.get("/api/users").status_code == 200


def test_default_admin_blocked_in_production(db_session, monkeypatch):
    from app.config import get_settings
    from app.services.auth_service import create_default_admin

    settings = get_settings()
    monkeypatch.setattr(settings, "environment", "production")
    with pytest.raises(RuntimeError, match="production"):
        create_default_admin(db_session)
