from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, MeResponse
from app.models.user import User
from app.services.auth_service import verify_password, create_session, delete_session
from app.dependencies import get_current_user, get_token_from_request
from app.config import get_settings

router = APIRouter()

# Login throttle policy
THROTTLE_MAX_ATTEMPTS = 5
THROTTLE_BACKOFFS = {
    5: timedelta(minutes=15),
    10: timedelta(hours=1),
    15: timedelta(hours=4),
    20: timedelta(days=1),
}


def _compute_lock_duration(attempts: int) -> timedelta:
    """Exponential backoff: each THROTTLE_MAX_ATTEMPTS tier extends the lock."""
    tier = min(attempts // THROTTLE_MAX_ATTEMPTS, len(THROTTLE_BACKOFFS) - 1)
    return THROTTLE_BACKOFFS[tier] if tier >= 0 else timedelta(seconds=30)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, response: Response, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username, User.is_active == True).first()
    if not user:
        # Never reveal whether username exists — same error as bad password
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        remaining = int((user.locked_until - datetime.now(timezone.utc)).total_seconds())
        raise HTTPException(
            status_code=401,
            detail=f"Account locked. Try again in {remaining // 60} minutes.",
        )

    if verify_password(body.password, user.password_hash):
        # Successful login: reset all throttle state
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_failed_login = None
        user.last_login = datetime.now(timezone.utc)
        db.commit()

        session, signed_token = create_session(db, user.id)

        settings = get_settings()
        proto = request.headers.get("x-forwarded-proto", "").split(",")[0].strip().lower()
        response.set_cookie(
            key="session_token",
            value=signed_token,
            httponly=True,
            samesite="lax",
            max_age=86400,
            secure=(settings.environment == "production" and proto == "https"),
        )
        return TokenResponse(
            token=signed_token,
            user=MeResponse(id=str(user.id), username=user.username, role=user.role),
        )
    else:
        # Failed login: increment attempts and apply lock if threshold reached
        user.failed_login_attempts += 1
        user.last_failed_login = datetime.now(timezone.utc)

        if user.failed_login_attempts >= THROTTLE_MAX_ATTEMPTS:
            user.locked_until = datetime.now(timezone.utc) + _compute_lock_duration(user.failed_login_attempts)

        db.commit()

        raise HTTPException(status_code=401, detail="Invalid username or password")


@router.post("/logout")
def logout(request: Request, response: Response, user: User = Depends(get_current_user), db: DBSession = Depends(get_db)):
    token = get_token_from_request(request)
    if token:
        delete_session(db, token)
    response.delete_cookie("session_token")
    return {"message": "Logged out"}


@router.get("/me", response_model=MeResponse)
def me(user: User = Depends(get_current_user)):
    return MeResponse(id=str(user.id), username=user.username, role=user.role)
