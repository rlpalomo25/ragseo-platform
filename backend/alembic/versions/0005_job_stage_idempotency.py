"""Job-stage idempotency backstop (Fix 5B): unique (job_id, sequence).

Revision ID: 0005_job_stage_idempotency
Revises: 0004_external_data
Create Date: 2026-09-15
"""

from alembic import op

revision = "0005_job_stage_idempotency"
down_revision = "0004_external_data"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # One stage per (job, sequence). With Celery `acks_late` +
    # `reject_on_worker_lost`, a lost worker redelivers the agent task and
    # `advance_job` re-runs; the DB constraint turns what would be a silent
    # duplicate stage row (double LLM spend, double revision_count bump) into
    # a caught IntegrityError that the sweeper/guard handles instead.
    op.create_unique_constraint(
        "uq_job_stages_job_sequence",
        "job_stages",
        ["job_id", "sequence"],
    )

    # Index the sweeper's lookups: a stage whose task has been running longer
    # than the sweeper threshold. Speeds "find oldest active stage per job".
    op.create_index("ix_job_stages_job_status", "job_stages", ["job_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_job_stages_job_status", table_name="job_stages")
    op.drop_constraint("uq_job_stages_job_sequence", "job_stages", type_="unique")
