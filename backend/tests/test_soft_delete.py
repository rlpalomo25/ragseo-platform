"""Soft-delete: global filter, revoke-on-delete, restore, and username re-use."""

from datetime import UTC, datetime

from app.database import disable_soft_delete_filter
from app.models.audit import AuditLog
from app.models.user import Session as UserSession
from app.models.user import User
from app.services.auth_service import hash_password

from tests.conftest import login


def _login_as_admin(client, admin_user) -> None:
    client.cookies.clear()
    resp = login(client, admin_user.username, "adminpass")
    assert resp.status_code == 200


# -- mechanism: global filter propagation -------------------------------------


def test_global_filter_hides_deleted_from_orm(db_session):
    ghost = User(
        username="soft_ghost",
        password_hash=hash_password("secret123"),
        role="writer",
        deleted_at=datetime.now(UTC),
    )
    alive = User(username="soft_alive", password_hash=hash_password("secret123"), role="writer")
    db_session.add_all([ghost, alive])
    db_session.commit()

    usernames = {u.username for u in db_session.query(User).all()}
    assert "soft_alive" in usernames
    assert "soft_ghost" not in usernames


def test_bypass_utility_exposes_deleted(db_session):
    ghost = User(
        username="soft_ghost2",
        password_hash=hash_password("secret123"),
        role="writer",
        deleted_at=datetime.now(UTC),
    )
    db_session.add(ghost)
    db_session.commit()

    with disable_soft_delete_filter():
        rows = db_session.query(User).all()
        assert any(u.username == "soft_ghost2" for u in rows)


# -- API behavior --------------------------------------------------------------


def test_delete_sets_deleted_at_and_revokes_sessions(client, db_session, admin_user, test_user):
    login(client, "testwriter", "secret123")
    _login_as_admin(client, admin_user)
    resp = client.delete(f"/api/users/{test_user.id}")
    assert resp.status_code == 200

    db_session.expire_all()
    assert db_session.query(User).filter(User.id == test_user.id).first() is None
    with disable_soft_delete_filter():
        deleted = db_session.query(User).filter(User.id == test_user.id).first()
    assert deleted is not None
    assert deleted.deleted_at is not None
    assert deleted.is_active is False
    assert db_session.query(UserSession).filter(UserSession.user_id == test_user.id).count() == 0


def test_deleted_user_token_rejected(client, admin_user, test_user):
    login(client, "testwriter", "secret123")
    _login_as_admin(client, admin_user)
    client.delete(f"/api/users/{test_user.id}")

    assert login(client, "testwriter", "secret123").status_code == 401


def test_deleted_user_hidden_from_admin_listing(client, db_session, admin_user, test_user):
    _login_as_admin(client, admin_user)
    client.delete(f"/api/users/{test_user.id}")
    resp = client.get("/api/users")
    assert resp.status_code == 200
    usernames = [u["username"] for u in resp.json()["users"]]
    assert test_user.username not in usernames


def test_restore_reactivates_user(client, admin_user, test_user):
    _login_as_admin(client, admin_user)
    client.delete(f"/api/users/{test_user.id}")

    resp = client.post(f"/api/users/{test_user.id}/restore")
    assert resp.status_code == 200
    assert resp.json()["is_active"] is True
    assert resp.json()["deleted_at"] is None

    assert login(client, "testwriter", "secret123").status_code == 200


def test_restore_unknown_or_active_user_404(client, admin_user, test_user):
    _login_as_admin(client, admin_user)
    # Active user is not soft-deleted -> 404 (restore only targets soft-deleted).
    resp = client.post(f"/api/users/{test_user.id}/restore")
    assert resp.status_code == 404
    resp = client.post("/api/users/00000000-0000-0000-0000-000000000000/restore")
    assert resp.status_code == 404


def test_recreate_soft_deleted_username_succeeds(client, admin_user, test_user):
    _login_as_admin(client, admin_user)
    client.delete(f"/api/users/{test_user.id}")
    resp = client.post(
        "/api/users", json={"username": "testwriter", "password": "newpass123", "role": "writer"}
    )
    assert resp.status_code == 201


def test_delete_and_restore_write_audit_rows(client, db_session, admin_user, test_user):
    _login_as_admin(client, admin_user)
    client.delete(f"/api/users/{test_user.id}")
    client.post(f"/api/users/{test_user.id}/restore")

    rows = db_session.query(AuditLog).all()
    assert {a.action for a in rows} >= {"user.delete", "user.restore"}
    assert all(a.username == "testadmin" for a in rows)
