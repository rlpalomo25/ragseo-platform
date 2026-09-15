"use client";

import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { useStats } from "@/lib/hooks/useStats";
import type { StatsResponse } from "@/types/stats";

const STATUS_LABELS: Record<string, string> = {
  running: "Running",
  awaiting_approval: "Awaiting review",
  approved: "Approved",
  failed: "Failed",
  cancelled: "Cancelled",
  abandoned: "Abandoned",
};

const DOC_TYPE_LABELS: Record<string, string> = {
  doctrine: "Doctrine",
  agent: "Agents",
  playbook: "Playbooks",
  brand_module: "Brand",
  schema: "Schema",
  system: "System",
  sop: "SOP",
  misc: "Other",
};

function StatCard({
  label,
  value,
  hint,
  accent = "brand",
}: {
  label: string;
  value: string;
  hint?: string;
  accent?: "brand" | "success" | "warning" | "danger";
}) {
  const accents = {
    brand: "from-brand-600 to-brand-400",
    success: "from-green-600 to-green-400",
    warning: "from-amber-500 to-amber-400",
    danger: "from-red-600 to-red-400",
  };
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">{label}</p>
      <p
        className={`mt-2 bg-gradient-to-r bg-clip-text text-3xl font-bold text-transparent ${accents[accent]}`}
        style={{ fontVariantNumeric: "tabular-nums" }}
      >
        {value}
      </p>
      {hint && <p className="mt-1 text-sm text-gray-500">{hint}</p>}
    </div>
  );
}

function CoverageBar({ pct }: { pct: number }) {
  const p = Math.round(pct * 100);
  return (
    <div className="mt-3">
      <div className="h-2 overflow-hidden rounded-full bg-gray-100" aria-hidden="true">
        <div
          className={`h-full rounded-full ${p >= 100 ? "bg-green-500" : p >= 90 ? "bg-brand-500" : "bg-amber-500"}`}
          style={{ width: `${Math.min(100, p)}%` }}
        />
      </div>
      <div className="mt-1 flex justify-between text-xs text-gray-500">
        <span>{p}% vectorized</span>
      </div>
    </div>
  );
}

export function DashboardContent() {
  const { data, isLoading, error } = useStats();

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <p className="py-12 text-center text-sm text-red-600" role="alert">
        Failed to load dashboard statistics.
      </p>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Doctrine corpus, embedding health, and content pipeline at a glance.
        </p>
      </div>

      <DashboardTiles data={data} />

      <div className="grid gap-6 lg:grid-cols-2">
        <SeriesBreakdown data={data} />
        <JobBreakdown data={data} />
      </div>
    </div>
  );
}

function DashboardTiles({ data }: { data: StatsResponse }) {
  const c = data.chunks;
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <StatCard
        label="Documents"
        value={String(data.documents.active)}
        hint={`${data.documents.total} total, ${data.documents.by_status["active"] ?? 0} active status`}
      />
      <StatCard
        label="Chunks indexed"
        value={`${c.embedded.toLocaleString()} / ${c.total.toLocaleString()}`}
        hint="pgvector embeddings"
        accent={c.coverage === 1 ? "success" : c.coverage >= 0.9 ? "brand" : "warning"}
      />
      <StatCard
        label="Pipeline throughput (30d)"
        value={String(data.jobs.created_last_30d)}
        hint={`${data.jobs.created_last_7d} in the last 7 days`}
      />
      <StatCard
        label="Revisions per job"
        value={data.jobs.total ? data.jobs.avg_revisions.toFixed(2) : "0.00"}
        hint={`${data.jobs.with_revisions} job${data.jobs.with_revisions === 1 ? "" : "s"} required revision`}
      />
    </div>
  );
}

function SeriesBreakdown({ data }: { data: StatsResponse }) {
  const entries = Object.entries(data.documents.by_series).sort((a, b) => b[1] - a[1]);
  const max = Math.max(1, ...entries.map(([, n]) => n));
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <h2 className="text-sm font-semibold text-gray-900">Doctrine by series</h2>
      <div className="mt-4 space-y-2">
        {entries.map(([series, count]) => (
          <div key={series} className="flex items-center gap-3">
            <span className="w-10 shrink-0 text-xs font-medium text-gray-500">Doc {series}</span>
            <div className="h-2 flex-1 overflow-hidden rounded-full bg-gray-100" aria-hidden="true">
              <div className="h-full rounded-full bg-brand-500" style={{ width: `${(count / max) * 100}%` }} />
            </div>
            <span className="w-8 shrink-0 text-right text-xs text-gray-600" style={{ fontVariantNumeric: "tabular-nums" }}>
              {count}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function JobBreakdown({ data }: { data: StatsResponse }) {
  const byStatus = Object.entries(data.jobs.by_status).sort((a, b) => b[1] - a[1]);
  const variants: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
    approved: "success",
    awaiting_approval: "warning",
    running: "info",
    failed: "danger",
    cancelled: "default",
    abandoned: "default",
  };
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-900">Pipeline status</h2>
        <span className="text-xs text-gray-500">{data.jobs.total} jobs</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {byStatus.map(([status, count]) => (
          <span
            key={status}
            className="inline-flex items-center gap-2 rounded-md border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm"
          >
            <Badge variant={variants[status] ?? "default"}>
              {STATUS_LABELS[status] ?? status}
            </Badge>
            <span className="font-semibold text-gray-900" style={{ fontVariantNumeric: "tabular-nums" }}>
              {count}
            </span>
          </span>
        ))}
        {byStatus.length === 0 && <p className="text-sm text-gray-500">No jobs yet.</p>}
      </div>
      {data.jobs.failed_stages > 0 && (
        <div className="mt-4 rounded border border-red-100 bg-red-50 px-3 py-2 text-sm text-red-700">
          {data.jobs.failed_stages} failed pipeline stage{data.jobs.failed_stages === 1 ? "" : "s"} on record.
        </div>
      )}
      <div className="mt-4 flex flex-wrap gap-2">
        {Object.entries(data.documents.by_doc_type)
          .filter(([t]) => t !== "misc")
          .map(([type, count]) => (
            <span key={type} className="text-xs text-gray-500">
              <span className="font-medium text-gray-700">{DOC_TYPE_LABELS[type] ?? type}</span>: {count}
            </span>
          ))}
      </div>
    </div>
  );
}