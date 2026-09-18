"""Login throttle fields (Fix 8): failed_login_attempts, locked_until, last_failed_login.

Revision ID: 0007_login_throttle
Revises: 0006_doc_number_unique
Create Date: 2026-09-15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "0007_login_throttle"
down_revision = "0006_doc_number_unique"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "users",
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("last_failed_login", sa.DateTime(timezone=True), nullable=True),
    )

    # Index for finding locked accounts
    op.create_index("ix_users_locked_until", "users", ["locked_until"])


def downgrade() -> None:
    op.drop_index("ix_users_locked_until", table_name="users")
    op.drop_column("users", "last_failed_login")
    op.drop_column("users", "locked_until")
    op.drop_column("users", "failed_login_attempts")