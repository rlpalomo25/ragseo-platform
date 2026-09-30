"""RBAC: 403s are enforced and each denial is persisted to the audit log."""

from app.models.audit import AuditLog

from tests.conftest import login


def test_writer_gets_403_with_audit_row(client, db_session, test_user):
    login(client, "testwriter", "secret123")
    resp = client.get("/api/users")
    assert resp.status_code == 403

    db_session.expire_all()
    rows = db_session.query(AuditLog).filter(AuditLog.action == "access_denied").all()
    assert len(rows) == 1
    assert rows[0].username == "testwriter"
    assert rows[0].status_code == 403
    assert rows[0].route == "/api/users"


def test_writer_gets_403_on_admin_ingest(client, db_session, test_user):
    login(client, "testwriter", "secret123")
    resp = client.get("/api/ingest/status")
    assert resp.status_code == 403

    db_session.expire_all()
    rows = db_session.query(AuditLog).filter(AuditLog.action == "access_denied").all()
    assert rows
    assert rows[0].route == "/api/ingest/status"


def test_anonymous_401_is_not_audited(client, db_session):
    client.cookies.clear()
    resp = client.get("/api/users")
    assert resp.status_code == 401
    assert db_session.query(AuditLog).count() == 0


def test_writer_cannot_read_audit(client, test_user):
    login(client, "testwriter", "secret123")
    resp = client.get("/api/audit")
    assert resp.status_code == 403


def test_admin_can_read_audit(client, admin_user):
    login(client, "testadmin", "adminpass")
    resp = client.get("/api/audit")
    assert resp.status_code == 200
    assert "entries" in resp.json()
