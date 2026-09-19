"""Baseline schema: users, sessions, documents, doc_references, agent_tasks, doc_chunks.

Revision ID: 0001_baseline
Revises:
Create Date: 2026-08-20
"""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy import Uuid

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None

EMBEDDING_DIMENSIONS = 1024


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "users",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="writer"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
    )

    op.create_table(
        "sessions",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id", Uuid(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("token", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "documents",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column("doc_number", sa.String(100), nullable=False, index=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("version", sa.String(50), nullable=True),
        sa.Column("series", sa.String(50), index=True),
        sa.Column("doc_type", sa.String(50), nullable=True),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("word_count", sa.Integer(), nullable=True),
        sa.Column("file_hash", sa.String(64), nullable=True),
        sa.Column("last_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "doc_references",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "source_doc_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("target_doc_number", sa.String(20), nullable=False, index=True),
        sa.Column("reference_type", sa.String(20), nullable=False),
    )

    op.create_table(
        "agent_tasks",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column("agent_type", sa.String(50), nullable=False, index=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending", index=True),
        sa.Column("input_data", sa.JSON(), nullable=False),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_by", Uuid(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "doc_chunks",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "document_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("heading_path", sa.String(500), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=True),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("embedding", Vector(EMBEDDING_DIMENSIONS), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_doc_chunks_document_chunk", "doc_chunks", ["document_id", "chunk_index"], unique=True)
    op.create_index(
        "ix_doc_chunks_embedding_hnsw",
        "doc_chunks",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )


def downgrade() -> None:
    op.drop_index("ix_doc_chunks_embedding_hnsw", table_name="doc_chunks")
    op.drop_table("doc_chunks")
    op.drop_table("agent_tasks")
    op.drop_table("doc_references")
    op.drop_table("documents")
    op.drop_table("sessions")
    op.drop_table("users")
