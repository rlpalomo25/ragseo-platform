import threading
import time
from collections import deque
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session as DBSession

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user, get_token_from_request
from app.models.user import User
from app.schemas.auth import LoginRequest, MeResponse, TokenResponse
from app.services.audit import log_audit
from app.services.auth_service import create_session, delete_session, verify_password

router = APIRouter()

# Login throttle policy. The account lock is per-username and escalating; the
# IP throttle is independent, so one IP cannot spray many accounts for free.
THROTTLE_MAX_ATTEMPTS = 5
THROTTLE_BACKOFFS = {
    5: timedelta(minutes=15),
    10: timedelta(hours=1),
    15: timedelta(hours=4),
    20: timedelta(days=1),
}

#: Failed logins allowed from one IP inside the window before 429s start. Kept
#: above the per-account lock threshold so a single user's typos cannot trip it,
#: but low enough that spraying many accounts costs the attacker real time.
IP_THROTTLE_MAX_FAILURES = 10
IP_THROTTLE_WINDOW_SECONDS = 300

#: A valid bcrypt hash of an unguessable value. Comparing against this when the
#: username does not exist keeps the response time in the same ballpark as a
#: real failed password check, so login does not become a username oracle.
DUMMY_PASSWORD_HASH = "$2b$12$W3aCT.hZeejnMUlSeCYNuOZ9tIFOkSB6fcPCdLzGhDTMW6./YLWUS"

_ip_failures: dict[str, deque[float]] = {}
_ip_failures_lock = threading.Lock()


def _client_ip(request: Request) -> str:
    """Best-effort client IP.

    Behind Caddy the original address is appended to X-Forwarded-For, so the
    *last* entry is the hop physically closest to us and cannot be spoofed by a
    request-supplied header the way the first entry can. With no header (dev,
    direct curl) fall back to the socket peer.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        candidate = forwarded.split(",")[-1].strip()
        if candidate:
            return candidate
    return request.client.host if request.client else "<unknown>"


def _prune_ip_failures(ip: str, now: float) -> deque[float]:
    failures = _ip_failures.setdefault(ip, deque())
    cutoff = now - IP_THROTTLE_WINDOW_SECONDS
    while failures and failures[0] < cutoff:
        failures.popleft()
    return failures


def _throttle_retry_after(ip: str) -> int | None:
    with _ip_failures_lock:
        failures = _prune_ip_failures(ip, time.monotonic())
        if len(failures) < IP_THROTTLE_MAX_FAILURES:
            return None
        return max(1, int(failures[0] + IP_THROTTLE_WINDOW_SECONDS - time.monotonic()) + 1)


def _record_ip_failure(ip: str) -> None:
    with _ip_failures_lock:
        now = time.monotonic()
        _prune_ip_failures(ip, now).append(now)


def _clear_ip_failures(ip: str) -> None:
    with _ip_failures_lock:
        _ip_failures.pop(ip, None)


def _reset_ip_throttle() -> None:
    """Test seam: the limiter is process-global, tests must not leak into each other."""
    with _ip_failures_lock:
        _ip_failures.clear()


def _as_utc(value: datetime) -> datetime:
    """SQLite drops the offset even for DateTime(timezone=True); assume UTC rather
    than comparing naive against aware and raising TypeError (the lock check used
    to 500 the moment any account had a lock set)."""
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _compute_lock_duration(attempts: int) -> timedelta:
    """Lock duration for an attempt count, capped at the highest tier.

    The old implementation indexed THROTTLE_BACKOFFS (keyed 5/10/15/20) with
    ``attempts // 5`` (1..4) — disjoint key sets, so the first failure at the
    threshold raised KeyError and, because that happened before the commit, the
    counter rolled back and the account was never locked at all.
    """
    for threshold in sorted(THROTTLE_BACKOFFS, reverse=True):
        if attempts >= threshold:
            return THROTTLE_BACKOFFS[threshold]
    return THROTTLE_BACKOFFS[min(THROTTLE_BACKOFFS)]


def _audit_failed_login(
    db: DBSession, request: Request, user: User | None, attempted: str, action: str
) -> None:
    """Record the failure and commit it. The caller raises immediately after, so
    a flush-only row would be rolled back with the request."""
    log_audit(
        db,
        user=user,
        action=action,
        route=request.url.path,
        detail=f"username='{attempted}'" + ("" if user else " (unknown user)"),
        status_code=401,
        commit=True,
    )


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, response: Response, db: DBSession = Depends(get_db)):
    ip = _client_ip(request)
    retry_after = _throttle_retry_after(ip)
    if retry_after is not None:
        raise HTTPException(
            status_code=429,
            detail="Too many failed login attempts. Try again later.",
            headers={"Retry-After": str(retry_after)},
        )

    user = db.query(User).filter(User.username == body.username, User.is_active).first()
    if not user:
        # Do the bcrypt work anyway: skipping it made an unknown username answer
        # an order of magnitude faster and turned login into an enumeration oracle.
        verify_password(body.password, DUMMY_PASSWORD_HASH)
        _record_ip_failure(ip)
        _audit_failed_login(db, request, None, body.username, "login.failed")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Check if account is locked. Deliberately the same 401 body as a bad
    # password: "Account locked" is a response only an existing account can
    # produce, which is exactly the existence disclosure the line above avoids.
    if user.locked_until and _as_utc(user.locked_until) > datetime.now(UTC):
        _record_ip_failure(ip)
        _audit_failed_login(db, request, user, body.username, "login.locked")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if verify_password(body.password, user.password_hash):
        _clear_ip_failures(ip)
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

        _record_ip_failure(ip)
        # commit=True persists the counter/lock too: the raise below would
        # otherwise roll back the increment along with the audit row.
        _audit_failed_login(db, request, user, body.username, "login.failed")

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
