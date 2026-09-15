from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app.schemas.user import CreateUser, UpdateUser, UserResponse, UserList
from app.models.user import User
from app.services.auth_service import hash_password
from app.dependencies import require_admin

router = APIRouter()


@router.get("", response_model=UserList)
def list_users(admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return UserList(
        users=[UserResponse(
            id=str(u.id),
            username=u.username,
            role=u.role,
            is_active=u.is_active,
            created_at=u.created_at.isoformat() if u.created_at else "",
            last_login=u.last_login.isoformat() if u.last_login else None,
        ) for u in users],
        total=len(users),
    )


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
    return UserResponse(
        id=str(user.id),
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else "",
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UpdateUser, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
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
    return UserResponse(
        id=str(user.id),
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else "",
    )


@router.delete("/{user_id}")
def delete_user(user_id: str, admin: User = Depends(require_admin), db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"message": f"User {user.username} deactivated"}
