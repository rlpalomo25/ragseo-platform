"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useState, useCallback } from "react";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useJob, jobAction } from "@/lib/hooks/useJobs";
import { jobStatusVariant, type StageDetail } from "@/types/job";

const AGENT_LABELS: Record<string, string> = {
  router: "Router",
  writer: "Writer",
  auditor: "Auditor",
};

export default function JobDetailPage() {
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <JobDetailContent />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function JobDetailContent() {
  const params = useParams<{ jobId: string }>();
  const jobId = typeof params?.jobId === "string" ? params.jobId : null;
  const { job, isLoading, mutate } = useJob(jobId);
  const [actionError, setActionError] = useState("");
  const [acting, setActing] = useState(false);

  const runAction = useCallback(
    async (action: "approve" | "cancel") => {
      if (!job) return;
      setActing(true);
      setActionError("");
      try {
        await jobAction(job.id, action);
        mutate();
      } catch (err) {
        setActionError(err instanceof Error ? err.message : `Failed to ${action} job`);
      } finally {
        setActing(false);
      }
    },
    [job, mutate]
  );

  if (isLoading || !job) {
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  const latestWriterStage = [...job.stages]
    .reverse()
    .find((s) => s.agent_type === "writer");
  const latestAuditStage = [...job.stages]
    .reverse()
    .find((s) => s.agent_type === "auditor");

  return (
    <div className="mx-auto max-w-4xl">
      <Link href="/jobs" className="text-sm text-brand-600 hover:text-brand-700">
        ← Back to Pipeline
      </Link>

      <div className="mt-3 flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-gray-900">{job.title}</h1>
          <p className="mt-1 text-sm text-gray-500">
            {job.brand ?? "unrouted"} · {job.content_type ?? "—"} ·{" "}
            {job.revision_count}/{job.max_revisions} revisions
          </p>
        </div>
        <Badge variant={jobStatusVariant(job.status)}>
          {job.status.replace("_", " ")}
        </Badge>
      </div>

      <div className="mt-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
        <h2 className="text-xs font-semibold uppercase text-gray-400">Request</h2>
        <p className="mt-1 whitespace-pre-wrap text-sm text-gray-700">{job.request}</p>
        {job.notes && (
          <>
            <h2 className="mt-3 text-xs font-semibold uppercase text-gray-400">Notes</h2>
            <p className="mt-1 whitespace-pre-wrap text-sm text-gray-700">{job.notes}</p>
          </>
        )}
      </div>

      {actionError && (
        <p className="mt-3 text-sm text-red-600" role="alert">{actionError}</p>
      )}

      {job.status === "awaiting_approval" && (
        <div className="mt-4 flex items-center justify-between rounded-lg border border-yellow-200 bg-yellow-50 p-4">
          <p className="text-sm text-yellow-800">
            Draft passed audit and is waiting for human approval.
          </p>
          <div className="flex shrink-0 gap-2">
            <Button
              variant="secondary"
              loading={acting}
              onClick={() => runAction("cancel")}
            >
              Reject & Cancel
            </Button>
            <Button loading={acting} onClick={() => runAction("approve")}>
              Approve
            </Button>
          </div>
        </div>
      )}

      {(job.status === "running" || job.status === "failed") && (
        <div className="mt-4 flex justify-end">
          <Button
            variant="danger"
            loading={acting}
            onClick={() => runAction("cancel")}
          >
            Cancel Job
          </Button>
        </div>
      )}

      <h2 className="mb-3 mt-6 text-lg font-semibold text-gray-900">Stages</h2>
      <ol className="space-y-3">
        {job.stages.map((stage, idx) => (
          <li key={stage.id} className="relative pl-8">
            <span
              aria-hidden="true"
              className={`absolute left-[13px] top-5 h-2.5 w-2.5 -translate-x-1/2 rounded-full ring-2 ring-white ${dotColor(stage.status)}`}
            />
            {idx < job.stages.length - 1 && (
              <span aria-hidden="true" className="absolute bottom-[-12px] left-[13px] top-9 w-px bg-gray-200" />
            )}
            <StageCard stage={stage} />
          </li>
        ))}
      </ol>

      {latestWriterStage?.output_data && (
        <DraftPreview stage={latestWriterStage} />
      )}
      {latestAuditStage?.output_data && (
        <AuditSummary stage={latestAuditStage} />
      )}
    </div>
  );
}

function dotColor(status: string): string {
  switch (status) {
    case "completed":
      return "bg-green-500";
    case "running":
    case "dispatched":
      return "animate-pulse bg-brand-500";
    case "failed":
      return "bg-red-500";
    default:
      return "bg-gray-300";
  }
}

function stageVariant(status: string): "success" | "warning" | "danger" | "info" | "default" {
  switch (status) {
    case "completed":
      return "success";
    case "pending":
      return "warning";
    case "dispatched":
    case "running":
      return "info";
    case "failed":
      return "danger";
    default:
      return "default";
  }
}

function StageCard({ stage }: { stage: StageDetail }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <li className="rounded-lg border border-gray-200 bg-white shadow-sm">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between p-4 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
      >
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-gray-900">
            {stage.sequence}. {AGENT_LABELS[stage.agent_type] ?? stage.agent_type}
          </span>
          <Badge variant={stageVariant(stage.status)}>{stage.status}</Badge>
        </div>
        <span className="text-xs text-gray-500">{expanded ? "Hide" : "Details"}</span>
      </button>
      {expanded && (
        <div className="border-t border-gray-100 px-4 pb-4">
          {stage.feedback && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold uppercase text-gray-400">
                Revision Feedback
              </h4>
              <pre className="mt-1 overflow-x-auto whitespace-pre-wrap rounded bg-yellow-50 p-3 text-xs text-yellow-900">
                {stage.feedback}
              </pre>
            </div>
          )}
          {stage.error_message && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold uppercase text-red-400">Error</h4>
              <pre className="mt-1 overflow-x-auto whitespace-pre-wrap rounded bg-red-50 p-3 text-xs text-red-700">
                {stage.error_message}
              </pre>
            </div>
          )}
          {stage.output_data && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold uppercase text-gray-400">Output</h4>
              <pre className="mt-1 max-h-64 overflow-auto rounded bg-gray-50 p-3 text-xs text-gray-700">
                {JSON.stringify(stage.output_data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </li>
  );
}

function DraftPreview({ stage }: { stage: StageDetail }) {
  const output = (stage.output_data?.output ?? {}) as Record<string, unknown>;
  const content = output.content_markdown as string | undefined;
  const provenance = (stage.output_data?.provenance ?? []) as unknown[];

  if (!content) return null;

  return (
    <div className="mt-6 rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Latest Draft</h2>
        <span className="text-xs text-gray-500">
          {provenance.length} doctrine source{provenance.length === 1 ? "" : "s"}
        </span>
      </div>
      <pre className="mt-3 max-h-[32rem] overflow-auto whitespace-pre-wrap rounded bg-gray-50 p-4 text-sm text-gray-800">
        {content}
      </pre>
    </div>
  );
}

function AuditSummary({ stage }: { stage: StageDetail }) {
  const output = (stage.output_data?.output ?? {}) as Record<string, unknown>;
  const verdict = output.verdict as string | undefined;
  const summary = output.summary as string | undefined;
  const findings = (output.findings ?? []) as Array<Record<string, unknown>>;

  if (!verdict) return null;

  return (
    <div className="mt-6 rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Audit Result</h2>
        <Badge variant={verdict === "fail" ? "danger" : verdict === "pass" ? "success" : "warning"}>
          {verdict.replace(/_/g, " ")}
        </Badge>
      </div>
      {summary && <p className="mt-2 text-sm text-gray-700">{summary}</p>}
      {findings.length > 0 && (
        <ul className="mt-3 space-y-2">
          {findings.map((f, i) => (
            <li key={i} className="rounded border border-gray-100 bg-gray-50 p-3 text-sm">
              <span className="font-medium text-gray-900">
                {String(f.check ?? "Finding")}
              </span>{" "}
              <Badge variant={f.severity === "critical" ? "danger" : f.severity === "major" ? "warning" : "default"}>
                {String(f.severity ?? "minor")}
              </Badge>
              {f.notes ? <p className="mt-1 text-gray-600">{String(f.notes)}</p> : null}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
