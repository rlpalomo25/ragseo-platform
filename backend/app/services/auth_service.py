import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

import bcrypt
from sqlalchemy.orm import Session as DBSession

from app.config import DEFAULT_ADMIN_PASSWORD_PLACEHOLDER, get_settings
from app.models.user import Session, User

settings = get_settings()


def _sign(raw_token: str) -> str:
    mac = hmac.new(settings.secret_key.encode(), raw_token.encode(), hashlib.sha256).hexdigest()
    return f"{raw_token}.{mac}"


def _unsign(signed_token: str) -> str | None:
    if "." not in signed_token:
        return None
    raw_token, mac = signed_token.rsplit(".", 1)
    expected = hmac.new(settings.secret_key.encode(), raw_token.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected):
        return None
    return raw_token


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ValueError:
        return False


SESSION_MAX_PER_USER = 5


def create_session(db: DBSession, user_id: UUID) -> tuple[Session, str]:
    """Create a session row (raw token stored) and return it with the signed
    client-facing token. The ORM object keeps the raw token so later commits
    never persist the signed form.

    Enforces a max concurrent sessions limit per user (SESSION_MAX_PER_USER).
    If the user already has the max number of active sessions, the oldest one
    is revoked before creating the new one."""
    # Revoke oldest existing session if at max capacity
    existing = (
        db.query(Session)
        .filter(
            Session.user_id == user_id,
            Session.expires_at > datetime.now(UTC),
        )
        .order_by(Session.created_at.asc())
        .all()
    )

    if len(existing) >= SESSION_MAX_PER_USER:
        for old in existing[: len(existing) - SESSION_MAX_PER_USER + 1]:
            db.query(Session).filter(Session.id == old.id).delete()
        db.commit()

    token = secrets.token_hex(32)
    expires_at = datetime.now(UTC) + timedelta(hours=settings.session_expiry_hours)
    session = Session(user_id=user_id, token=token, expires_at=expires_at)
    db.add(session)
    db.commit()
    db.refresh(session)
    db.expunge(session)
    return session, _sign(token)


def get_user_by_token(db: DBSession, signed_token: str) -> User | None:
    raw_token = _unsign(signed_token)
    if not raw_token:
        return None
    session = (
        db.query(Session)
        .filter(
            Session.token == raw_token,
            Session.expires_at > datetime.now(UTC),
        )
        .first()
    )
    if not session:
        return None
    user = db.query(User).filter(User.id == session.user_id, User.is_active).first()
    return user


def delete_session(db: DBSession, signed_token: str) -> bool:
    raw_token = _unsign(signed_token)
    if not raw_token:
        return False
    deleted = db.query(Session).filter(Session.token == raw_token).delete()
    db.commit()
    return deleted > 0


def prune_expired_sessions(db: DBSession) -> int:
    """Delete all expired sessions and return the count of deleted rows."""
    result = db.query(Session).filter(Session.expires_at < datetime.now(UTC)).delete()
    db.commit()
    return result


def create_default_admin(db: DBSession) -> User | None:
    existing = db.query(User).filter(User.username == settings.default_admin_username).first()
    if existing:
        return None
    if (
        settings.environment == "production"
        and settings.default_admin_password == DEFAULT_ADMIN_PASSWORD_PLACEHOLDER
    ):
        raise RuntimeError(
            "Refusing to seed default admin with default password in production. "
            "Set DEFAULT_ADMIN_PASSWORD to a strong value first."
        )
    user = User(
        username=settings.default_admin_username,
        password_hash=hash_password(settings.default_admin_password),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
