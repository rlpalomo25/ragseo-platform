"use client";

import Link from "next/link";
import { useState, useCallback } from "react";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useStats } from "@/lib/hooks/useStats";
import { useJobs, jobAction } from "@/lib/hooks/useJobs";
import type { StatsResponse } from "@/types/stats";
import type { JobSummary } from "@/types/job";

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
  children,
}: {
  label: string;
  value: string;
  hint?: string;
  accent?: "brand" | "success" | "warning" | "danger";
  children?: React.ReactNode;
}) {
  const accents = {
    brand: "from-brand-600 to-brand-400",
    success: "from-green-600 to-green-400",
    warning: "from-amber-500 to-amber-400",
    danger: "from-red-600 to-red-400",
  };
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <p className="text-xs font-semibold uppercase tracking-wide text-gray-400 dark:text-gray-500">
        {label}
      </p>
      <p
        className={`mt-2 bg-gradient-to-r bg-clip-text text-3xl font-bold text-transparent ${accents[accent]}`}
        style={{ fontVariantNumeric: "tabular-nums" }}
      >
        {value}
      </p>
      {children}
      {hint && <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{hint}</p>}
    </div>
  );
}

function FormatLatency({ seconds }: { seconds: number | null }) {
  if (seconds == null) {
    return <span className="mt-2 block bg-gradient-to-r from-gray-500 to-gray-400 bg-clip-text text-3xl font-bold text-transparent">—</span>;
  }
  const text =
    seconds < 60 ? `${seconds.toFixed(1)}s` : seconds < 3600 ? `${(seconds / 60).toFixed(1)}m` : `${(seconds / 3600).toFixed(1)}h`;
  return (
    <span className="mt-2 block bg-gradient-to-r from-brand-600 to-brand-400 bg-clip-text text-3xl font-bold text-transparent">
      {text}
    </span>
  );
}

function CoverageBar({ pct }: { pct: number }) {
  const p = Math.round(pct * 100);
  return (
    <div className="mt-3">
      <div className="h-2 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-800" aria-hidden="true">
        <div
          className={`h-full rounded-full ${p >= 100 ? "bg-green-500" : p >= 90 ? "bg-brand-500" : "bg-amber-500"}`}
          style={{ width: `${Math.min(100, p)}%` }}
        />
      </div>
      <div className="mt-1 flex justify-between text-xs text-gray-500 dark:text-gray-400">
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
      <p className="py-12 text-center text-sm text-red-600 dark:text-red-400" role="alert">
        Failed to load dashboard statistics.
      </p>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Doctrine corpus, embedding health, and content pipeline at a glance.
        </p>
      </div>

      <DashboardTiles data={data} />
      <SystemHealth data={data} />
      <RecentJobsGrid />

      <div className="grid gap-6 lg:grid-cols-2">
        <SeriesBreakdown data={data} />
        <JobBreakdown data={data} />
      </div>
    </div>
  );
}

function DashboardTiles({ data }: { data: StatsResponse }) {
  const c = data.chunks;
  const awaitingApproval = data.jobs.by_status["awaiting_approval"] ?? 0;
  const failedStages = data.jobs.failed_stages;
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
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
      >
        <CoverageBar pct={c.coverage} />
      </StatCard>
      <StatCard
        label="Awaiting review"
        value={String(awaitingApproval)}
        hint={`${failedStages} failed pipeline stage${failedStages === 1 ? "" : "s"} on record`}
        accent={awaitingApproval > 0 ? "warning" : "brand"}
      />
      <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400 dark:text-gray-500">
          Avg agent latency
        </p>
        <FormatLatency seconds={data.system.avg_latency_seconds} />
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">completed agent tasks</p>
      </div>
    </div>
  );
}

function healthBadge(health: StatsResponse["system"]["health"]): "success" | "warning" | "danger" {
  return health === "healthy" ? "success" : health === "warning" ? "warning" : "danger";
}

function SystemHealth({ data }: { data: StatsResponse }) {
  const { system } = data;
  return (
    <div className="flex flex-wrap items-center gap-x-6 gap-y-3 rounded-lg border border-gray-200 bg-white px-5 py-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <div className="flex items-center gap-2">
        <Badge variant={healthBadge(system.health)}>
          {system.health}
        </Badge>
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-300">
        <span className="font-semibold text-gray-900 dark:text-gray-100">{system.active_users}</span>{" "}
        active user{system.active_users === 1 ? "" : "s"}
      </p>
      <p className="text-sm text-gray-600 dark:text-gray-300">
        <span className="font-semibold text-gray-900 dark:text-gray-100">{system.queued_jobs}</span>{" "}
        queued job{system.queued_jobs === 1 ? "" : "s"}
      </p>
      {system.health !== "healthy" && (
        <p className="text-xs text-amber-600 dark:text-amber-400">
          {system.health === "degraded"
            ? "Pipeline degraded — check failed stages and agent latency."
            : "Embedding coverage below 100% — some doctrine retrieves less effectively."}
        </p>
      )}
    </div>
  );
}

function RecentJobsGrid() {
  const { jobs, mutate } = useJobs({ limit: 6 });

  return (
    <section aria-labelledby="recent-jobs-heading">
      <div className="mb-4 flex items-center justify-between">
        <h2 id="recent-jobs-heading" className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Recent Jobs
        </h2>
        <Link
          href="/jobs"
          className="text-sm font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400"
        >
          View all
        </Link>
      </div>
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        {jobs.map((job) => (
          <RecentJobCard key={job.id} job={job} onMutate={mutate} />
        ))}
        {jobs.length === 0 && (
          <p className="col-span-full text-sm text-gray-500 dark:text-gray-400">
            No jobs yet — start one from the Pipeline page, or open an approval item.
          </p>
        )}
      </div>
    </section>
  );
}

function RecentJobCard({ job, onMutate }: { job: JobSummary; onMutate: () => void }) {
  const [retrying, setRetrying] = useState(false);
  const [retryError, setRetryError] = useState("");

  const retry = useCallback(async () => {
    setRetrying(true);
    setRetryError("");
    try {
      await jobAction(job.id, "retry");
      onMutate();
    } catch (err) {
      setRetryError(err instanceof Error ? err.message : "Retry failed");
    } finally {
      setRetrying(false);
    }
  }, [job.id, onMutate]);

  const canRetry = job.status === "failed" || job.status === "cancelled";

  return (
    <div className="flex flex-col justify-between rounded-lg border border-gray-200 bg-white p-5 shadow-sm transition-colors hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-900 dark:hover:bg-gray-800/50">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="truncate text-sm font-medium text-gray-900 dark:text-gray-100">{job.title}</h3>
          <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {job.brand ?? "unrouted"} · {job.content_type ?? "—"} · {job.revision_count}/{job.max_revisions} revisions
          </p>
          <p className="mt-1 text-xs text-gray-400 dark:text-gray-500">
            {new Intl.DateTimeFormat("en-US", {
              dateStyle: "medium",
              timeStyle: "short",
            }).format(new Date(job.created_at))}
          </p>
        </div>
        <Badge variant={jobStatusVariant(job.status)}>
          {STATUS_LABELS[job.status] ?? job.status}
        </Badge>
      </div>
      <div className="mt-4 flex items-center justify-between gap-3">
        {retryError ? (
          <span className="text-xs text-red-600 dark:text-red-400" role="alert">{retryError}</span>
        ) : (
          <span className="text-xs text-gray-400 dark:text-gray-500">View logs for stage-by-stage detail.</span>
        )}
        <div className="flex shrink-0 items-center gap-2">
          {canRetry && (
            <Button size="sm" variant="secondary" loading={retrying} onClick={retry}>
              Retry
            </Button>
          )}
          <Link
            href={`/jobs/${job.id}`}
            className="inline-flex h-8 items-center rounded-md px-3 text-sm font-medium text-brand-600 transition-colors hover:bg-brand-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 dark:text-brand-400 dark:hover:bg-brand-900/30"
          >
            View logs
          </Link>
        </div>
      </div>
    </div>
  );
}

function jobStatusVariant(status: string): "success" | "warning" | "danger" | "info" | "default" {
  switch (status) {
    case "approved":
      return "success";
    case "awaiting_approval":
      return "warning";
    case "running":
      return "info";
    case "failed":
      return "danger";
    default:
      return "default";
  }
}

function SeriesBreakdown({ data }: { data: StatsResponse }) {
  const entries = Object.entries(data.documents.by_series).sort((a, b) => b[1] - a[1]);
  const max = Math.max(1, ...entries.map(([, n]) => n));
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Doctrine by series</h2>
      <div className="mt-4 space-y-2">
        {entries.map(([series, count]) => (
          <div key={series} className="flex items-center gap-3">
            <span className="w-10 shrink-0 text-xs font-medium text-gray-500 dark:text-gray-400">Doc {series}</span>
            <div className="h-2 flex-1 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-800" aria-hidden="true">
              <div className="h-full rounded-full bg-brand-500" style={{ width: `${(count / max) * 100}%` }} />
            </div>
            <span className="w-8 shrink-0 text-right text-xs text-gray-600 dark:text-gray-300" style={{ fontVariantNumeric: "tabular-nums" }}>
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
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Pipeline status</h2>
        <span className="text-xs text-gray-500 dark:text-gray-400">{data.jobs.total} jobs</span>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {byStatus.map(([status, count]) => (
          <span
            key={status}
            className="inline-flex items-center gap-2 rounded-md border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm dark:border-gray-700 dark:bg-gray-800"
          >
            <Badge variant={variants[status] ?? "default"}>
              {STATUS_LABELS[status] ?? status}
            </Badge>
            <span className="font-semibold text-gray-900 dark:text-gray-100" style={{ fontVariantNumeric: "tabular-nums" }}>
              {count}
            </span>
          </span>
        ))}
        {byStatus.length === 0 && <p className="text-sm text-gray-500 dark:text-gray-400">No jobs yet.</p>}
      </div>
      {data.jobs.failed_stages > 0 && (
        <div className="mt-4 rounded border border-red-100 bg-red-50 px-3 py-2 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-900/30 dark:text-red-300">
          {data.jobs.failed_stages} failed pipeline stage{data.jobs.failed_stages === 1 ? "" : "s"} on record.
        </div>
      )}
      <div className="mt-4 flex flex-wrap gap-2">
        {Object.entries(data.documents.by_doc_type)
          .filter(([t]) => t !== "misc")
          .map(([type, count]) => (
            <span key={type} className="text-xs text-gray-500 dark:text-gray-400">
              <span className="font-medium text-gray-700 dark:text-gray-300">{DOC_TYPE_LABELS[type] ?? type}</span>: {count}
            </span>
          ))}
      </div>
    </div>
  );
}