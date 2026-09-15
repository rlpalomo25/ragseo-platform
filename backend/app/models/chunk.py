import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Uuid, Index
from pgvector.sqlalchemy import Vector
from app.config import get_settings
from app.database import Base

settings = get_settings()


class DocChunk(Base):
    __tablename__ = "doc_chunks"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    heading_path = Column(String(500))
    content = Column(Text, nullable=False)
    token_count = Column(Integer)
    content_hash = Column(String(64), nullable=False)
    embedding = Column(Vector(settings.embedding_dimensions))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_doc_chunks_document_chunk", "document_id", "chunk_index", unique=True),
    )
