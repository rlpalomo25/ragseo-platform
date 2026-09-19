import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)

from app.database import Base


class AgentJob(Base):
    """A content-production job chained through pipeline stages (Doc 230).

    Status flow: running -> awaiting_approval -> approved
                 running -> failed (audit revisions exhausted / stage error)
                 any active status -> cancelled
    """

    __tablename__ = "agent_jobs"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    request = Column(Text, nullable=False)
    brand = Column(String(50))
    content_type = Column(String(100))
    status = Column(String(30), nullable=False, default="running", index=True)
    revision_count = Column(Integer, nullable=False, default=0)
    max_revisions = Column(Integer, nullable=False, default=2)
    notes = Column(Text)
    created_by = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )


class JobStage(Base):
    """One pipeline stage of a job, linked to the agent task executing it."""

    __tablename__ = "job_stages"

    __table_args__ = (
        # Idempotency backstop (Fix 5B): one sequence per job. A crashed /
        # redelivered worker task that re-runs _dispatch_stage for the same
        # (job, sequence) cannot silently create a duplicate stage row — the
        # INSERT fails instead, so the pipeline stays on the original chain.
        UniqueConstraint("job_id", "sequence", name="uq_job_stages_job_sequence"),
    )

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(
        Uuid(as_uuid=True), ForeignKey("agent_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sequence = Column(Integer, nullable=False)
    agent_type = Column(String(50), nullable=False)
    task_id = Column(Uuid(as_uuid=True), ForeignKey("agent_tasks.id"), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
