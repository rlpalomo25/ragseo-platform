"""Doc-number uniqueness among ACTIVE docs (Fix 7).

Revision ID: 0006_doc_number_unique
Revises: 0005_job_stage_idempotency
Create Date: 2026-09-15
"""

import sqlalchemy as sa
from alembic import op

revision = "0006_doc_number_unique"
down_revision = "0005_job_stage_idempotency"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First, handle any existing duplicates by marking older ones as superseded
    # (keeping the most recently updated one as active)
    op.execute("""
        WITH ranked AS (
            SELECT id,
                   doc_number,
                   ROW_NUMBER() OVER (PARTITION BY doc_number ORDER BY last_updated DESC NULLS LAST, created_at DESC) as rn
            FROM documents
            WHERE status = 'active'
        )
        UPDATE documents
        SET status = 'superseded',
            last_updated = NOW()
        WHERE id IN (SELECT id FROM ranked WHERE rn > 1)
    """)

    # Partial unique index on ACTIVE docs. A whole-table constraint would make
    # the runtime supersede flow impossible: a newer take of doc 503 can only
    # be inserted after the old (superseded) row relinquishes the number, and
    # that old row STILL holds doc_number=503 — history must keep it.
    if op.get_bind().dialect.name == "sqlite":
        op.create_index(
            "uq_documents_doc_number_active",
            "documents",
            ["doc_number"],
            unique=True,
            sqlite_where=sa.text("status = 'active'"),
        )
    else:
        op.create_index(
            "uq_documents_doc_number_active",
            "documents",
            ["doc_number"],
            unique=True,
            postgresql_where=sa.text("status = 'active'"),
        )

    # Index for reconciliation lookups (active docs by doc_number)
    op.create_index("ix_documents_doc_number_status", "documents", ["doc_number", "status"])


def downgrade() -> None:
    op.drop_index("ix_documents_doc_number_status", table_name="documents")
    op.drop_index("uq_documents_doc_number_active", table_name="documents")
