"""Retarget embeddings to a local provider: Vector 1024 -> 768, HNSW rebuild.

Backstory: the corpus was chunked under Voyage AI (voyage-3-lite, 1024 dims).
Switching to a local Ollama-embedded model (nomic-embed-text, 768 dims) changes
the vector dimension, so the column type and the HNSW index must be rebuilt and
all existing vectors dropped (they are incompatible with the new space and
would be re-embedded on the next re-ingest anyway).

Revision ID: 0003_local_embeddings
Revises: 0002_jobs
Create Date: 2026-09-10
"""

from alembic import op
from pgvector.sqlalchemy import Vector

revision = "0003_local_embeddings"
down_revision = "0002_jobs"
branch_labels = None
depends_on = None

HNSW_INDEX = "ix_doc_chunks_embedding_hnsw"
PREV_DIM = 1024
NEW_DIM = 768


def upgrade() -> None:
    op.drop_index(HNSW_INDEX, table_name="doc_chunks")
    # Existing vectors are 1024-dim and incompatible with the new column type;
    # null them out so the ALTER succeeds. Next re-ingest re-embeds from scratch.
    op.execute("UPDATE doc_chunks SET embedding = NULL")
    op.alter_column("doc_chunks", "embedding", existing_type=Vector(PREV_DIM), type_=Vector(NEW_DIM))
    op.create_index(
        HNSW_INDEX,
        "doc_chunks",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )


def downgrade() -> None:
    op.drop_index(HNSW_INDEX, table_name="doc_chunks")
    op.execute("UPDATE doc_chunks SET embedding = NULL")
    op.alter_column("doc_chunks", "embedding", existing_type=Vector(NEW_DIM), type_=Vector(PREV_DIM))
    op.create_index(
        HNSW_INDEX,
        "doc_chunks",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )
