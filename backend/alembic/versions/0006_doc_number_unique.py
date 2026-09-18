"""Doc-number uniqueness (Fix 7): unique constraint on documents.doc_number.

Revision ID: 0006_doc_number_unique
Revises: 0005_job_stage_idempotency
Create Date: 2026-09-15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

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

    # Add unique constraint on doc_number
    op.create_unique_constraint(
        "uq_documents_doc_number",
        "documents",
        ["doc_number"],
    )

    # Index for reconciliation lookups (active docs by doc_number)
    op.create_index("ix_documents_doc_number_status", "documents", ["doc_number", "status"])


def downgrade() -> None:
    op.drop_index("ix_documents_doc_number_status", table_name="documents")
    op.drop_constraint("uq_documents_doc_number", "documents", type_="unique")