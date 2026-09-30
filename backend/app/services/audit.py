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
) -> AuditLog:
    """Persist an audit-log entry immediately (commits the surrounding tx)."""
    entry = AuditLog(
        user_id=getattr(user, "id", None),
        username=getattr(user, "username", "<anonymous>"),
        action=action,
        route=route,
        detail=detail,
        status_code=status_code,
    )
    db.add(entry)
    db.commit()
    return entry
