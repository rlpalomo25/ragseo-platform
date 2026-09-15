from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, MeResponse
from app.models.user import User
from app.services.auth_service import verify_password, create_session, delete_session
from app.dependencies import get_current_user, get_token_from_request
from app.config import get_settings

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, response: Response, db: DBSession = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username, User.is_active == True).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    session, signed_token = create_session(db, user.id)
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    settings = get_settings()
    # Secure only over an actually-secure channel: production behind the Caddy
    # TLS terminator sends X-Forwarded-Proto: https, so the flag travels with
    # the scheme instead of with a static environment value. Over plain-HTTP
    # interim (no domain yet) the cookie must be sendable, or browsers drop it.
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
