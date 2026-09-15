"""Pipeline orchestration tables: agent_jobs, job_stages.

Revision ID: 0002_jobs
Revises: 0001_baseline
Create Date: 2026-08-20
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Uuid

revision = "0002_jobs"
down_revision = "0001_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agent_jobs",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("request", sa.Text(), nullable=False),
        sa.Column("brand", sa.String(50), nullable=True),
        sa.Column("content_type", sa.String(100), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="running", index=True),
        sa.Column("revision_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_revisions", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", Uuid(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "job_stages",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column("job_id", Uuid(as_uuid=True), sa.ForeignKey("agent_jobs.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("agent_type", sa.String(50), nullable=False),
        sa.Column("task_id", Uuid(as_uuid=True), sa.ForeignKey("agent_tasks.id"), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("job_stages")
    op.drop_table("agent_jobs")
