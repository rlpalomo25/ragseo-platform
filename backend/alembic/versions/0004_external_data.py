"""External market-data tables (weekly GSC/GA4/Ubersuggest/calls/leads exports).

Revision ID: 0004_external_data
Revises: 0003_local_embeddings
Create Date: 2026-09-10
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Uuid

revision = "0004_external_data"
down_revision = "0003_local_embeddings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "external_exports",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("brand", sa.String(50), nullable=True),
        sa.Column("file_name", sa.String(500), nullable=False),
        sa.Column("file_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("period_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("period_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("exported_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="imported"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("imported_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_external_exports_source_type", "external_exports", ["source_type"])
    op.create_index("ix_external_exports_domain", "external_exports", ["domain"])

    op.create_table(
        "search_console_dims",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("dim_type", sa.String(20), nullable=False),
        sa.Column("key", sa.String(500), nullable=False),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ctr", sa.Float(), nullable=True),
        sa.Column("position", sa.Float(), nullable=True),
    )
    op.create_index("ix_sc_dim_export", "search_console_dims", ["export_id"])
    op.create_index("ix_sc_dim_domain_type", "search_console_dims", ["domain", "dim_type"])

    op.create_table(
        "search_console_daily",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ctr", sa.Float(), nullable=True),
        sa.Column("position", sa.Float(), nullable=True),
    )
    op.create_index("ix_sc_daily_export", "search_console_daily", ["export_id"])

    op.create_table(
        "ai_overview_impressions",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("dim_type", sa.String(20), nullable=False),
        sa.Column("key", sa.String(255), nullable=True),
        sa.Column("day", sa.Date(), nullable=True),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_ai_imp_export", "ai_overview_impressions", ["export_id"])

    op.create_table(
        "keyword_estimates",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("keyword", sa.String(500), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=True),
        sa.Column("position", sa.Float(), nullable=True),
        sa.Column("est_visits", sa.Integer(), nullable=True),
        sa.Column("difficulty", sa.Float(), nullable=True),
        sa.Column("cpc", sa.Float(), nullable=True),
        sa.Column("ranking_url", sa.Text(), nullable=True),
    )
    op.create_index("ix_kw_est_export", "keyword_estimates", ["export_id"])
    op.create_index("ix_kw_est_domain_kw", "keyword_estimates", ["domain", "keyword"])

    op.create_table(
        "backlinks",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("source_title", sa.Text(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("target_url", sa.Text(), nullable=True),
        sa.Column("domain_authority", sa.Integer(), nullable=True),
        sa.Column("page_authority", sa.Integer(), nullable=True),
        sa.Column("spam_score", sa.Float(), nullable=True),
        sa.Column("anchor_text", sa.Text(), nullable=True),
        sa.Column("first_seen", sa.Date(), nullable=True),
        sa.Column("last_seen", sa.Date(), nullable=True),
    )
    op.create_index("ix_backlinks_export", "backlinks", ["export_id"])

    op.create_table(
        "top_pages",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("est_visits", sa.Integer(), nullable=True),
        sa.Column("backlinks", sa.Integer(), nullable=True),
    )
    op.create_index("ix_top_pages_export", "top_pages", ["export_id"])

    op.create_table(
        "call_tracking",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("customer_number", sa.String(50), nullable=True),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("search_query", sa.Text(), nullable=True),
        sa.Column("referral", sa.Text(), nullable=True),
        sa.Column("page", sa.Text(), nullable=True),
        sa.Column("last_url", sa.Text(), nullable=True),
        sa.Column("likelihood", sa.Float(), nullable=True),
        sa.Column("message_body", sa.Text(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("ring_time_seconds", sa.Integer(), nullable=True),
        sa.Column("call_date", sa.Date(), nullable=True),
    )
    op.create_index("ix_call_tracking_export", "call_tracking", ["export_id"])

    op.create_table(
        "lead_summaries",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("week_start", sa.Date(), nullable=True),
        sa.Column("week_end", sa.Date(), nullable=True),
        sa.Column("form_fills", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("vapi_calls", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_lead_summaries_export", "lead_summaries", ["export_id"])

    op.create_table(
        "ga4_events",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("event_name", sa.String(100), nullable=False),
        sa.Column("event_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_users", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("events_per_user", sa.Float(), nullable=True),
        sa.Column("total_revenue", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
    )
    op.create_index("ix_ga4_events_export", "ga4_events", ["export_id"])

    op.create_table(
        "domain_reports",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("report_type", sa.String(20), nullable=False),
        sa.Column("source_file", sa.String(500), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=False),
    )
    op.create_index("ix_domain_reports_export", "domain_reports", ["export_id"])
    op.create_index("ix_domain_reports_domain", "domain_reports", ["domain"])

    op.create_table(
        "domain_metrics",
        sa.Column("id", Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "export_id",
            Uuid(as_uuid=True),
            sa.ForeignKey("external_exports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(255), nullable=False),
        sa.Column("metric", sa.String(50), nullable=False),
        sa.Column("value", sa.Float(), nullable=True),
    )
    op.create_index("ix_domain_metrics_export", "domain_metrics", ["export_id"])
    op.create_index("ix_domain_metrics_domain", "domain_metrics", ["domain"])


def downgrade() -> None:
    op.drop_table("domain_metrics")
    op.drop_table("domain_reports")
    op.drop_table("ga4_events")
    op.drop_table("lead_summaries")
    op.drop_table("call_tracking")
    op.drop_table("top_pages")
    op.drop_table("backlinks")
    op.drop_table("keyword_estimates")
    op.drop_table("ai_overview_impressions")
    op.drop_table("search_console_daily")
    op.drop_table("search_console_dims")
    op.drop_table("external_exports")
