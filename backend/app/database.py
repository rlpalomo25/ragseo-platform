import contextvars
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, with_loader_criteria

from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


_soft_delete_bypass = contextvars.ContextVar("ragseo_soft_delete_bypass", default=False)


@contextmanager
def disable_soft_delete_filter():
    """Admin bypass: let queries see soft-deleted users (audit/compliance)."""
    token = _soft_delete_bypass.set(True)
    try:
        yield
    finally:
        _soft_delete_bypass.reset(token)


def _apply_soft_delete_filter(execute_state) -> None:
    # Deferred import: database.py is imported by app.models.user (via Base),
    # so importing User at module scope would be a circular import.
    from app.models.user import User

    if _soft_delete_bypass.get():
        return
    if not execute_state.is_orm_statement or execute_state.is_column_load:
        return
    execute_state.statement = execute_state.statement.options(
        with_loader_criteria(User, lambda u: u.deleted_at.is_(None), include_aliases=True)
    )


event.listen(Session, "do_orm_execute", _apply_soft_delete_filter)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope():
    """Yield a Session, always closing it (works outside request/DI context)."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
