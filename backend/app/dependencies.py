from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.models.user import User
from app.services.audit import log_audit
from app.services.auth_service import get_user_by_token


def get_token_from_request(request: Request) -> str | None:
    token = request.cookies.get("session_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    return token


def get_current_user(request: Request, db: DBSession = Depends(get_db)) -> User:
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return user


def _deny(request: Request, db: DBSession, user: User, detail: str, action: str) -> None:
    # commit=True is required here and nowhere else. The raise below discards
    # the session's transaction, so an audit row that only joined the caller's
    # transaction would be rolled back with it and the denied request would
    # leave no trace at all. Persisting the 403 is the entire point of logging
    # it, so this write must survive the exception that is about to be raised.
    log_audit(
        db,
        user=user,
        action=action,
        route=request.url.path,
        detail=f"{detail} (role={user.role})",
        status_code=403,
        commit=True,
    )
    raise HTTPException(status_code=403, detail=detail)


def require_admin(
    request: Request,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
) -> User:
    if user.role != "admin":
        _deny(request, db, user, "Admin access required", "access_denied")
    return user


def require_writer(
    request: Request,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
) -> User:
    if user.role not in ("admin", "writer"):
        _deny(request, db, user, "Writer access required", "access_denied")
    return user
