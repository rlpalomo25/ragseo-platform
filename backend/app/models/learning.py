"""Learning-loop persistence: publications, weekly performance snapshots, signals.

Doc 203/205 "Simple Performance Record": link a generated job to its published
URL, snapshot its GSC/GA4/AI/call metrics each import cycle, and surface
Doc 205-style flags for human review. Doctrine updates stay human-driven
(Doc 203 sec. 4.0 approval requirement) — this layer records and exposes
signals only. Every snapshot carries its source export for provenance.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Uuid,
)

from app.database import Base


def _now():
    return datetime.now(UTC)


class ContentPublication(Base):
    __tablename__ = "content_publications"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(
        Uuid(as_uuid=True), ForeignKey("agent_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    publish_url = Column(Text, nullable=False)
    publish_date = Column(Date)
    target_keyword = Column(String(500))
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), default=_now)


class ContentPerformanceSnapshot(Base):
    __tablename__ = "content_performance_snapshots"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("content_publications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_export_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("external_exports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    period_from = Column(DateTime(timezone=True))
    period_to = Column(DateTime(timezone=True))
    position = Column(Float)
    clicks = Column(Integer, nullable=False, default=0)
    impressions = Column(Integer, nullable=False, default=0)
    ctr = Column(Float)
    ai_overview_impressions = Column(Integer, nullable=False, default=0)
    calls = Column(Integer, nullable=False, default=0)
    est_visits = Column(Integer)
    revenue = Column(Float)
    movement = Column(Float)
    movement_ctr = Column(Float)
    movement_impressions = Column(Integer)
    flags = Column(JSON, nullable=False, default=list)

    __table_args__ = (
        # One snapshot per (publication, export): re-snapshotting the same
        # weekly import must not duplicate a measurement. A plain unique
        # constraint is sufficient here (no supersede semantics like docs).
        Index(
            "uq_content_perf_pub_export",
            "publication_id",
            "source_export_id",
            unique=True,
        ),
    )


class LearningSignal(Base):
    __tablename__ = "learning_signals"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("content_publications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source = Column(String(50), nullable=False)
    observation = Column(Text, nullable=False)
    action_taken = Column(Text)
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), default=_now)
