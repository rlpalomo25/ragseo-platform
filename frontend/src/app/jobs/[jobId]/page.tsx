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
import { Input } from "@/components/ui/Input";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import { useJob, jobAction } from "@/lib/hooks/useJobs";
import { registerPublication, usePublications } from "@/lib/hooks/useLearning";
import { jobStatusVariant, type JobDetail, type StageDetail } from "@/types/job";
import { FLAG_LABELS, flagBadgeVariant, type Publication } from "@/types/learning";

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

      <PublishedContentPanel job={job} />

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

function PublishedContentPanel({ job }: { job: JobDetail }) {
  const { publications, isLoading, mutate } = usePublications();
  const pub = publications.find((p) => p.job_id === job.id);
  const [url, setUrl] = useState("");
  const [keyword, setKeyword] = useState("");
  const [pubDate, setPubDate] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setSaving(true);
      setError("");
      setDone(false);
      try {
        await registerPublication(job.id, {
          url: url.trim(),
          target_keyword: keyword.trim() || undefined,
          publish_date: pubDate || undefined,
        });
        setDone(true);
        await mutate();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to link publication");
      } finally {
        setSaving(false);
      }
    },
    [job.id, url, keyword, pubDate, mutate]
  );

  if (isLoading) {
    return (
      <Card className="mt-4">
        <CardHeader>
          <h2 className="text-sm font-semibold text-gray-900">Published Content</h2>
        </CardHeader>
        <CardContent>
          <Spinner size="sm" />
        </CardContent>
      </Card>
    );
  }

  if (pub) {
    return (
      <Card className="mt-4">
        <CardHeader className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-gray-900">Published Content</h2>
          <Badge variant="success">tracking</Badge>
        </CardHeader>
        <CardContent>
          <p className="text-sm font-medium text-gray-900">{pub.publish_url}</p>
          <p className="mt-1 text-xs text-gray-500">
            {pub.target_keyword ? `Target keyword: ${pub.target_keyword}` : "No target keyword"}
            {pub.publish_date ? ` · Published ${pub.publish_date}` : ""}
          </p>
          <SnapshotMetrics snapshot={pub.latest} />
        </CardContent>
      </Card>
    );
  }

  if (job.status !== "approved") return null;

  return (
    <Card className="mt-4">
      <CardHeader>
        <h2 className="text-sm font-semibold text-gray-900">Published Content</h2>
      </CardHeader>
      <CardContent>
        <p className="mb-3 text-xs text-gray-500">
          Link this job to the URL it went live on. Weekly GSC / AI-Overview / GA4 / calls data will be
          measured against it and recalled as Performance Memory for future briefs (Doc 203 §7.0).
        </p>
        <form onSubmit={handleSubmit} className="space-y-3">
          <Input
            label="Published URL"
            name="publish_url"
            type="url"
            required
            placeholder="https://example.com/slug/"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <div className="grid gap-3 sm:grid-cols-2">
            <Input
              label="Target keyword (optional)"
              name="target_keyword"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
            />
            <Input
              label="Publish date (optional)"
              name="publish_date"
              type="date"
              value={pubDate}
              onChange={(e) => setPubDate(e.target.value)}
            />
          </div>
          {error && <p className="text-sm text-red-600" role="alert">{error}</p>}
          {done && (
            <p className="text-sm text-green-600" role="status">
              Publication linked — tracking started.
            </p>
          )}
          <div className="flex justify-end">
            <Button type="submit" loading={saving}>Link Publication</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

function SnapshotMetrics({ snapshot }: { snapshot: Publication["latest"] }) {
  if (!snapshot) {
    return (
      <p className="mt-3 text-xs text-gray-500">
        No performance snapshot yet — it will appear after the next weekly exports import.
      </p>
    );
  }
  return (
    <div className="mt-3 rounded border border-gray-100 bg-gray-50 p-3">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-gray-700">
        {snapshot.position != null && (
          <span>Pos <strong>{snapshot.position.toFixed(1)}</strong></span>
        )}
        <span>{snapshot.impressions.toLocaleString()} imp</span>
        <span>{snapshot.clicks.toLocaleString()} clicks</span>
        {snapshot.ctr != null && <span>CTR <strong>{snapshot.ctr.toFixed(1)}%</strong></span>}
        <span>{snapshot.ai_overview_impressions} AI-imp</span>
        <span>{snapshot.calls} calls</span>
        {snapshot.movement != null && (
          <span
            className={
              snapshot.movement > 0
                ? "font-medium text-red-600"
                : "font-medium text-green-600"
            }
          >
            {snapshot.movement > 0 ? "▼" : "▲"} {Math.abs(snapshot.movement).toFixed(1)} pos
          </span>
        )}
      </div>
      {snapshot.flags.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {snapshot.flags.map((flag) => (
            <span key={flag} title={FLAG_LABELS[flag] ?? flag}>
              <Badge variant={flagBadgeVariant(flag)}>{flag}</Badge>
            </span>
          ))}
        </div>
      )}
    </div>
  );
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
