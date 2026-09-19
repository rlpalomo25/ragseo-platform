from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session as DBSession

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user, get_token_from_request
from app.models.user import User
from app.schemas.auth import LoginRequest, MeResponse, TokenResponse
from app.services.auth_service import create_session, delete_session, verify_password

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
    """Lock duration, escalating per THROTTLE_MAX_ATTEMPTS tier (e.g. every 5 failures)."""
    tier = min(attempts // THROTTLE_MAX_ATTEMPTS, len(THROTTLE_BACKOFFS) - 1)
    return THROTTLE_BACKOFFS[tier]


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, response: Response, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username, User.is_active).first()
    if not user:
        # Never reveal whether username exists — same error as bad password
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.now(UTC):
        remaining = int((user.locked_until - datetime.now(UTC)).total_seconds())
        raise HTTPException(
            status_code=401,
            detail=f"Account locked. Try again in {remaining // 60} minutes.",
        )

    if verify_password(body.password, user.password_hash):
        # Successful login: reset all throttle state
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_failed_login = None
        user.last_login = datetime.now(UTC)
        db.commit()

        _, signed_token = create_session(db, user.id)

        settings = get_settings()
        proto = request.headers.get("x-forwarded-proto", "").split(",")[0].strip().lower()
        response.set_cookie(
            key="session_token",
            value=signed_token,
            httponly=True,
            samesite="lax",
            max_age=settings.session_expiry_hours * 3600,
            secure=(settings.environment == "production" and proto == "https"),
        )
        return TokenResponse(
            token=signed_token,
            user=MeResponse(id=str(user.id), username=user.username, role=user.role),
        )
    else:
        # Failed login: increment attempts and apply lock if threshold reached
        user.failed_login_attempts += 1
        user.last_failed_login = datetime.now(UTC)

        if user.failed_login_attempts >= THROTTLE_MAX_ATTEMPTS:
            user.locked_until = datetime.now(UTC) + _compute_lock_duration(user.failed_login_attempts)

        db.commit()

        raise HTTPException(status_code=401, detail="Invalid username or password")


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    token = get_token_from_request(request)
    if token:
        delete_session(db, token)
    response.delete_cookie("session_token")
    return {"message": "Logged out"}


@router.get("/me", response_model=MeResponse)
def me(user: User = Depends(get_current_user)):
    return MeResponse(id=str(user.id), username=user.username, role=user.role)
