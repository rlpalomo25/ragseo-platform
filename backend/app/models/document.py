import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text, Uuid, text

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_number = Column(String(100), nullable=False, index=True)
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
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    __table_args__ = (
        # doc_number is unique among ACTIVE docs only: superseding a doc frees
        # its number for a newer take, but the superseded row (same number)
        # must still be kept for history. A full-table unique constraint (as in
        # the original 0006 draft) makes "supersede" impossible at runtime.
        Index(
            "uq_documents_doc_number_active",
            "doc_number",
            unique=True,
            sqlite_where=text("status = 'active'"),
            postgresql_where=text("status = 'active'"),
        ),
    )


class DocReference(Base):
    __tablename__ = "doc_references"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_doc_id = Column(Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    target_doc_number = Column(String(20), nullable=False, index=True)
    reference_type = Column(String(20), nullable=False)
