"""Audit-log writes.

Audit logging is a side effect of something else, so it must never be the thing
that decides whether that something else is durable. That distinction is the
whole reason this module does not commit by default.
"""

from sqlalchemy.orm import Session as DBSession

from app.models.audit import AuditLog


def log_audit(
    db: DBSession,
    *,
    user,
    action: str,
    route: str | None = None,
    detail: str | None = None,
    status_code: int | None = None,
    commit: bool = False,
) -> AuditLog:
    """Add an audit-log entry to the caller's session.

    By default the entry is only ``flush``ed, so it joins the caller's
    transaction and becomes durable exactly when the work it describes does.
    Two reasons this is the correct default:

    * **An audit row for work that rolled back is a lie.** With an implicit
      commit, a route that failed after logging would leave behind a record of a
      change that never happened, and the real change would be missing its
      record. The log and the data drift apart in both directions.
    * **Committing inside a helper is a hidden transaction boundary.** Callers
      cannot see it, cannot roll it back, and lose the ability to make their own
      changes and their audit entry atomic.

    ``commit=True`` exists for the one case where there is no surrounding
    transaction to join: :func:`app.dependencies._deny` records a 403 and then
    *raises*, and that raise would otherwise roll the audit row back with the
    request. Denied access that leaves no trace is the worst possible outcome
    for an audit log, so that caller opts in explicitly.

    Prefer letting the caller's ``db.commit()`` persist the row. Reach for
    ``commit=True`` only when the code is about to raise, or when there is no
    transaction at all.
    """
    entry = AuditLog(
        user_id=getattr(user, "id", None),
        username=getattr(user, "username", "<anonymous>"),
        action=action,
        route=route,
        detail=detail,
        status_code=status_code,
    )
    db.add(entry)
    if commit:
        db.commit()
    else:
        db.flush()
    return entry
