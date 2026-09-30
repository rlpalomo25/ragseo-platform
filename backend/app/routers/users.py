from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.database import disable_soft_delete_filter, get_db
from app.dependencies import require_admin
from app.models.user import Session as UserSession
from app.models.user import User
from app.schemas.user import CreateUser, UpdateUser, UserList, UserResponse
from app.services.audit import log_audit
from app.services.auth_service import hash_password

router = APIRouter()


def _response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else "",
        last_login=user.last_login.isoformat() if user.last_login else None,
        deleted_at=user.deleted_at.isoformat() if user.deleted_at else None,
    )


@router.get("", response_model=UserList)
def list_users(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return UserList(users=[_response(u) for u in users], total=len(users))


@router.post("", response_model=UserResponse, status_code=201)
def create_user(body: CreateUser, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    existing = db.query(User).filter(User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    if body.role not in ("admin", "writer"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'writer'")
    user = User(
        username=body.username,
        password_hash=hash_password(body.password),
        role=body.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _response(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID, body: UpdateUser, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if body.role is not None:
        if body.role not in ("admin", "writer"):
            raise HTTPException(status_code=400, detail="Role must be 'admin' or 'writer'")
        user.role = body.role
    if body.is_active is not None:
        user.is_active = body.is_active
    db.commit()
    db.refresh(user)
    return _response(user)


@router.delete("/{user_id}")
def delete_user(user_id: UUID, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    user.deleted_at = datetime.now(UTC)
    # Revoke every active session/token for this user immediately.
    db.query(UserSession).filter(UserSession.user_id == user.id).delete(synchronize_session="fetch")
    log_audit(
        db,
        user=admin,
        action="user.delete",
        route=f"/api/users/{user_id}",
        detail=f"Soft-deleted user '{user.username}'",
        status_code=200,
    )
    db.commit()
    return {"message": f"User {user.username} deactivated"}


@router.post("/{user_id}/restore", response_model=UserResponse)
def restore_user(user_id: UUID, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    with disable_soft_delete_filter():
        user = db.query(User).filter(User.id == user_id).first()
    if not user or user.deleted_at is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.deleted_at = None
    user.is_active = True
    log_audit(
        db,
        user=admin,
        action="user.restore",
        route=f"/api/users/{user_id}/restore",
        detail=f"Restored user '{user.username}'",
        status_code=200,
    )
    db.commit()
    db.refresh(user)
    return _response(user)
