"""Audit log table (RBAC/compliance trail).

Revision ID: 0010_audit_logs
Revises: 0009_user_soft_delete
Create Date: 2026-09-23
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Uuid

revision = "0010_audit_logs"
down_revision = "0009_user_soft_delete"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("route", sa.String(255), nullable=True),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
