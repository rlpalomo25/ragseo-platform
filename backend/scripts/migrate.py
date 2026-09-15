"""Idempotent, serialized Alembic migration runner.

Holds a PostgreSQL session-level advisory lock while running ``alembic upgrade
head`` so concurrent boots (backend + celery-worker both start with migration
steps) cannot race each other's DDL on a fresh database. The lock is released
in ``finally``, and the session scoping means it is also released automatically
if this process is killed mid-migration.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from alembic.config import Config
from alembic import command

from app.database import engine

# Arbitrary, stable advisory-lock key for this application's migrations.
LOCK_KEY = 90081


def main() -> None:
    alembic_ini = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "alembic.ini"
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT pg_advisory_lock(:key)"), {"key": LOCK_KEY})
        try:
            command.upgrade(Config(alembic_ini), "head")
        finally:
            conn.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": LOCK_KEY})


if __name__ == "__main__":
    main()