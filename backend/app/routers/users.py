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
from app.services.auth_service import BCRYPT_MAX_PASSWORD_BYTES, hash_password

router = APIRouter()


def _other_active_admins(db: DBSession, user: User) -> int:
    return (
        db.query(User)
        .filter(
            User.role == "admin",
            User.is_active.is_(True),
            User.id != user.id,
        )
        .count()
    )


def _guard_last_admin(db: DBSession, user: User, action: str) -> None:
    """Refuse a change that would leave the platform with no active admin.

    There is no password-reset or recovery path, so deleting/demoting the last
    admin is unrecoverable by design — including an admin doing it to themself.
    """
    if user.role == "admin" and user.is_active and _other_active_admins(db, user) == 0:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot {action} the last active admin; promote another admin first",
        )


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
    if len(body.password.encode()) > BCRYPT_MAX_PASSWORD_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"Password exceeds bcrypt's {BCRYPT_MAX_PASSWORD_BYTES}-byte limit",
        )
    user = User(
        username=body.username,
        password_hash=hash_password(body.password),
        role=body.role,
    )
    db.add(user)
    db.flush()
    log_audit(
        db,
        user=admin,
        action="user.create",
        route="/api/users",
        detail=f"Created user '{user.username}' with role {user.role}",
        status_code=201,
    )
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

    if body.role is not None and body.role not in ("admin", "writer"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'writer'")

    final_role = body.role if body.role is not None else user.role
    final_active = body.is_active if body.is_active is not None else user.is_active
    if user.role == "admin" and user.is_active and (final_role != "admin" or not final_active):
        _guard_last_admin(db, user, "demote or deactivate")

    # Captured before the writes: an audit row saying "role admin -> writer" is
    # only useful if it records what the value actually was.
    changes: list[str] = []
    if body.role is not None:
        if body.role not in ("admin", "writer"):
            raise HTTPException(status_code=400, detail="Role must be 'admin' or 'writer'")
        if body.role != user.role:
            changes.append(f"role {user.role} -> {body.role}")
        user.role = body.role
    if body.is_active is not None:
        if body.is_active != user.is_active:
            changes.append(f"is_active {user.is_active} -> {body.is_active}")
        user.is_active = body.is_active
    db.flush()
    # Audited even when nothing actually changed, so "an admin PUT and the row
    # says no change" is a record rather than a gap. The detail says which.
    log_audit(
        db,
        user=admin,
        action="user.update",
        route=f"/api/users/{user_id}",
        detail=(
            f"Updated user '{user.username}': {'; '.join(changes)}"
            if changes
            else f"Updated user '{user.username}': no change"
        ),
        status_code=200,
    )
    db.commit()
    db.refresh(user)
    return _response(user)


@router.delete("/{user_id}")
def delete_user(user_id: UUID, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    _guard_last_admin(db, user, "delete")
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
