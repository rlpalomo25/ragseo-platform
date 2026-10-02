"""Audit-log durability semantics.

The contract under test: an audit row must be durable exactly when the work it
describes is durable, and a denial must be durable even though the request that
produced it fails.

Durability cannot be observed by querying the shared test session and looking for
the row — a merely-flushed row is visible there, so such a test passes even when
the commit is missing. That is a real false pass, confirmed by removing the
commit from ``_deny`` and watching the existing test_rbac assertions still go
green. Worse, a ``rollback()`` probe cannot distinguish the two cases either,
because the test fixture wraps everything in an outer transaction.

So these tests count the commits each path actually issues. That is the property
that matters, and it cannot be faked by a flush.
"""

import pytest
from app.config import get_settings
from app.models.audit import AuditLog
from app.services.audit import log_audit

from tests.conftest import login


@pytest.fixture()
def doctrine_dirs(tmp_path, monkeypatch):
    """Local copy: the one in test_doctrine_upload.py is file-scoped."""
    settings = get_settings()
    baked = tmp_path / "baked_audit"
    uploads = tmp_path / "uploads_doctrine_audit"
    baked.mkdir()
    monkeypatch.setattr(settings, "doctrine_path", str(baked))
    monkeypatch.setattr(settings, "doctrine_upload_path", str(uploads))
    return baked, uploads


def count_commits(session):
    """Wrap session.commit so calls can be counted. Returns the list."""
    calls: list[int] = []
    original = session.commit

    def counting_commit():
        calls.append(1)
        return original()

    session.commit = counting_commit
    return calls


# ------------------------------------------------------------ log_audit itself


def test_log_audit_does_not_commit_by_default(db_session, test_user):
    """The default is flush-only, so the row follows the caller's transaction."""
    calls = count_commits(db_session)
    log_audit(db_session, user=test_user, action="test.no_commit", status_code=200)
    assert calls == [], "log_audit committed when it was not asked to"


def test_log_audit_commits_when_explicitly_asked(db_session, test_user):
    calls = count_commits(db_session)
    log_audit(db_session, user=test_user, action="test.commit", status_code=403, commit=True)
    assert calls == [1], "commit=True must issue exactly one commit"


def test_the_row_is_still_in_the_session_when_only_flushed(db_session, test_user):
    """Flush makes the row visible in-session without making it durable."""
    log_audit(db_session, user=test_user, action="test.flushed")
    assert db_session.query(AuditLog).filter(AuditLog.action == "test.flushed").count() == 1


# --------------------------------------------- denied access must be durable


def test_a_denied_request_commits_its_audit_row(client, db_session, test_user):
    """_deny raises, so without an explicit commit the 403 leaves no trace.

    Denied access that leaves no audit row is the worst outcome this system can
    have, which is why _deny opts in to commit=True.

    Counting starts *after* login on purpose: login writes a session row and
    commits, and counting that would make this test pass no matter what the 403
    path did. An earlier version of this test had exactly that bug and stayed
    green with the commit removed.
    """
    login(client, "testwriter", "secret123")
    calls = count_commits(db_session)
    assert client.get("/api/users").status_code == 403
    assert calls == [1], "the 403 audit row must be committed exactly once"


def test_a_denied_request_does_not_audit_a_successful_one(client, db_session, test_user):
    """Sanity: the row recorded is the denial, not something else."""
    login(client, "testwriter", "secret123")
    client.get("/api/users")
    db_session.expire_all()
    rows = db_session.query(AuditLog).filter(AuditLog.action == "access_denied").all()
    assert len(rows) == 1
    assert rows[0].status_code == 403
    assert rows[0].route == "/api/users"


# ------------------------------------------ read-only routes commit explicitly


def test_job_export_commits_its_audit_row(client, db_session, admin_user):
    """job.export mutates nothing else, so it has no transaction to join.

    A flush-only audit row in a read-only route would be discarded when the
    session closed, and job exports would leave no trail at all.
    """
    from tests.test_jobs_export import _export, _make_job

    job = _make_job(db_session, admin_user)
    login(client, "testadmin", "adminpass")

    calls = count_commits(db_session)
    assert _export(client, job).status_code == 200
    assert calls, "the export audit row was never committed"


# ------------------------------------------------- doctrine upload audit row


def test_doctrine_upload_commits_its_audit_row(client, db_session, admin_user, doctrine_dirs, monkeypatch):
    """The upload route logs after ingest_files has already committed.

    ingest_files commits internally, so simply counting commits across the
    request proves nothing — a commit certainly happened, just not for the audit
    row. The test therefore marks the commit count at the moment log_audit is
    called and requires a commit *after* that point.
    """
    from app.routers import ingest as ingest_module

    login(client, "testadmin", "adminpass")
    calls = count_commits(db_session)

    mark: dict[str, int] = {}
    real_log_audit = ingest_module.log_audit

    def spy(*args, **kwargs):
        mark["at_audit"] = len(calls)
        return real_log_audit(*args, **kwargs)

    monkeypatch.setattr(ingest_module, "log_audit", spy)

    files = [("files", ("Doc 940_Audited.md", b"body", "text/markdown"))]
    resp = client.post("/api/ingest/doctrine/upload", files=files)
    assert resp.status_code == 200, resp.text
    assert "at_audit" in mark, "log_audit was never reached"
    assert len(calls) > mark["at_audit"], "no commit was issued after the audit row was written"
