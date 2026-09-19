"""Learning loop: content_publications, content_performance_snapshots, learning_signals.

Doc 203/205 Simple Performance Record. New tables:

- ``content_publications``: human-registered published URL for a job (the link
  between a generated draft and its live page).
- ``content_performance_snapshots``: per-publication weekly measurement, keyed
  to the source ``external_exports`` row for provenance; unique per
  (publication, export) so re-imports never double-count.
- ``learning_signals``: Doc 205 flags surfaced for human review.

Revision ID: 0008_learning_loop
Revises: 0007_login_throttle
Create Date: 2026-09-18
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Uuid

revision = "0008_learning_loop"
down_revision = "0007_login_throttle"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "content_publications",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "job_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("agent_jobs.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("publish_url", sa.Text(), nullable=False),
        sa.Column("publish_date", sa.Date(), nullable=True),
        sa.Column("target_keyword", sa.String(500), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "content_performance_snapshots",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "publication_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("content_publications.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "source_export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("period_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("period_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("position", sa.Float(), nullable=True),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ctr", sa.Float(), nullable=True),
        sa.Column("ai_overview_impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("calls", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("est_visits", sa.Integer(), nullable=True),
        sa.Column("revenue", sa.Float(), nullable=True),
        sa.Column("movement", sa.Float(), nullable=True),
        sa.Column("movement_ctr", sa.Float(), nullable=True),
        sa.Column("movement_impressions", sa.Integer(), nullable=True),
        sa.Column("flags", sa.JSON(), nullable=False),
    )
    op.create_index(
        "uq_content_perf_pub_export",
        "content_performance_snapshots",
        ["publication_id", "source_export_id"],
        unique=True,
    )

    op.create_table(
        "learning_signals",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "publication_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("content_publications.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("observation", sa.Text(), nullable=False),
        sa.Column("action_taken", sa.Text(), nullable=True),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("learning_signals")
    op.drop_index("uq_content_perf_pub_export", table_name="content_performance_snapshots")
    op.drop_table("content_performance_snapshots")
    op.drop_table("content_publications")
