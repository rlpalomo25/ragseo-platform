from uuid import UUID
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app.models.user import User
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


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def require_writer(user: User = Depends(get_current_user)) -> User:
    if user.role not in ("admin", "writer"):
        raise HTTPException(status_code=403, detail="Writer access required")
    return user
