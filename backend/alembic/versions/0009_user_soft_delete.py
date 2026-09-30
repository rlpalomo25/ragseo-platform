"""User soft-delete: deleted_at column + partial unique username index.

Revision ID: 0009_user_soft_delete
Revises: 0008_learning_loop
Create Date: 2026-09-23
"""

import sqlalchemy as sa
from alembic import op

revision = "0009_user_soft_delete"
down_revision = "0008_learning_loop"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))

    # Whole-table unique index on username -> partial unique (only active rows).
    # Soft-deleted users keep their username in history but must not block a
    # new registration.
    op.drop_index("ix_users_username", table_name="users")
    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        op.create_index(
            "uq_users_username_active",
            "users",
            ["username"],
            unique=True,
            sqlite_where=sa.text("deleted_at IS NULL"),
        )
    else:
        op.create_index(
            "uq_users_username_active",
            "users",
            ["username"],
            unique=True,
            postgresql_where=sa.text("deleted_at IS NULL"),
        )

    op.create_index("ix_users_deleted_at", "users", ["deleted_at"])


def downgrade() -> None:
    op.drop_index("ix_users_deleted_at", table_name="users")
    op.drop_index("uq_users_username_active", table_name="users")
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.drop_column("users", "deleted_at")
