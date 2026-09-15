"""External market data: GSC, AI-Overview, Ubersuggest, GA4, calls, leads.

All rows hang off an ``external_exports`` row that records which weekly export
file they came from (unique by file hash) so re-imports are idempotent and
every number keeps provenance (Doc 329/C17-style) for agent decisions.
"""
import uuid
from datetime import datetime, date, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Date, ForeignKey, Uuid, Index
from app.database import Base


def _now():
    return datetime.now(timezone.utc)


class ExternalExport(Base):
    __tablename__ = "external_exports"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(String(50), nullable=False, index=True)
    domain = Column(String(255), nullable=False, index=True)
    brand = Column(String(50), index=True)
    file_name = Column(String(500), nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True)
    period_from = Column(DateTime(timezone=True))
    period_to = Column(DateTime(timezone=True))
    exported_at = Column(DateTime(timezone=True))
    row_count = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="imported")
    error = Column(Text)
    imported_at = Column(DateTime(timezone=True), default=_now)


class SearchConsoleDim(Base):
    """GSC top queries / pages / countries / devices / search appearance."""
    __tablename__ = "search_console_dims"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    dim_type = Column(String(20), nullable=False)
    key = Column(String(500), nullable=False)
    clicks = Column(Integer, nullable=False, default=0)
    impressions = Column(Integer, nullable=False, default=0)
    ctr = Column(Float)
    position = Column(Float)

    __table_args__ = (Index("ix_sc_dim_domain_type", "domain", "dim_type"),)


class SearchConsoleDaily(Base):
    __tablename__ = "search_console_daily"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    day = Column(Date, nullable=False)
    clicks = Column(Integer, nullable=False, default=0)
    impressions = Column(Integer, nullable=False, default=0)
    ctr = Column(Float)
    position = Column(Float)


class AIOverviewImpressions(Base):
    __tablename__ = "ai_overview_impressions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    dim_type = Column(String(20), nullable=False)
    key = Column(String(255))
    day = Column(Date)
    impressions = Column(Integer, nullable=False, default=0)


class KeywordEstimate(Base):
    """Ubersuggest KBT keyword tables."""
    __tablename__ = "keyword_estimates"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    keyword = Column(String(500), nullable=False)
    volume = Column(Integer)
    position = Column(Float)
    est_visits = Column(Integer)
    difficulty = Column(Float)
    cpc = Column(Float)
    ranking_url = Column(Text)

    __table_args__ = (Index("ix_kw_est_domain_kw", "domain", "keyword"),)


class Backlink(Base):
    __tablename__ = "backlinks"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    source_title = Column(Text)
    source_url = Column(Text)
    target_url = Column(Text)
    domain_authority = Column(Integer)
    page_authority = Column(Integer)
    spam_score = Column(Float)
    anchor_text = Column(Text)
    first_seen = Column(Date)
    last_seen = Column(Date)


class TopPage(Base):
    __tablename__ = "top_pages"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    url = Column(Text)
    title = Column(Text)
    est_visits = Column(Integer)
    backlinks = Column(Integer)


class CallTracking(Base):
    __tablename__ = "call_tracking"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    name = Column(String(255))
    customer_number = Column(String(50))
    source = Column(String(100))
    status = Column(String(50))
    search_query = Column(Text)
    referral = Column(Text)
    page = Column(Text)
    last_url = Column(Text)
    likelihood = Column(Float)
    message_body = Column(Text)
    duration_seconds = Column(Integer)
    ring_time_seconds = Column(Integer)
    call_date = Column(Date)


class LeadSummary(Base):
    __tablename__ = "lead_summaries"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    week_start = Column(Date)
    week_end = Column(Date)
    form_fills = Column(Integer, nullable=False, default=0)
    vapi_calls = Column(Integer, nullable=False, default=0)


class GA4Event(Base):
    __tablename__ = "ga4_events"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    event_name = Column(String(100), nullable=False)
    event_count = Column(Integer, nullable=False, default=0)
    total_users = Column(Integer, nullable=False, default=0)
    events_per_user = Column(Float)
    total_revenue = Column(Float, nullable=False, default=0.0)
    start_date = Column(Date)
    end_date = Column(Date)


class DomainReport(Base):
    """Ubersuggest PDF reports exported as markdown (traffic / backlink overviews)."""
    __tablename__ = "domain_reports"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    report_type = Column(String(20), nullable=False)
    source_file = Column(String(500))
    raw_text = Column(Text, nullable=False)


class DomainMetric(Base):
    """Key-value metrics mined from report markdown (DA, backlinks, ref domains, visits)."""
    __tablename__ = "domain_metrics"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    export_id = Column(Uuid(as_uuid=True), ForeignKey("external_exports.id", ondelete="CASCADE"),
                       nullable=False, index=True)
    domain = Column(String(255), nullable=False, index=True)
    metric = Column(String(50), nullable=False)
    value = Column(Float)