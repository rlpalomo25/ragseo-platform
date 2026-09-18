import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Uuid, UniqueConstraint
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_number = Column(String(100), nullable=False, index=True, unique=True)
    title = Column(String(500), nullable=False)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(String(50))
    series = Column(String(50), index=True)
    doc_type = Column(String(50))
    status = Column(String(20), default="active")
    word_count = Column(Integer)
    file_hash = Column(String(64))
    last_updated = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("doc_number", name="uq_documents_doc_number"),
    )


class DocReference(Base):
    __tablename__ = "doc_references"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_doc_id = Column(Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    target_doc_number = Column(String(20), nullable=False, index=True)
    reference_type = Column(String(20), nullable=False)
