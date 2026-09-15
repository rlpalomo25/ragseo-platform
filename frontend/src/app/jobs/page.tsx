"use client";

import Link from "next/link";
import { useState, useCallback } from "react";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";
import { useJobs, createJob, jobAction } from "@/lib/hooks/useJobs";
import { jobStatusVariant, type JobSummary } from "@/types/job";

const BRANDS = [
  { value: "", label: "Auto-detect" },
  { value: "mastershield", label: "MasterShield" },
  { value: "klean_gutter", label: "Klean Gutter" },
  { value: "mmgg", label: "MMGG" },
];

const CONTENT_TYPES = [
  { value: "", label: "Auto-detect" },
  { value: "comparison", label: "Comparison" },
  { value: "local_page", label: "Local Page" },
  { value: "blog_post", label: "Blog Post" },
  { value: "service_page", label: "Service Page" },
  { value: "faq_page", label: "FAQ Page" },
];

const JOB_STATUSES = [
  { value: "", label: "All statuses" },
  { value: "running", label: "Running" },
  { value: "awaiting_approval", label: "Awaiting review" },
  { value: "approved", label: "Approved" },
  { value: "failed", label: "Failed" },
  { value: "cancelled", label: "Cancelled" },
];

const selectClass =
  "rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-700 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500";

export default function JobsPage() {
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <JobsContent />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function JobsContent() {
  const [status, setStatus] = useState("");
  const [brand, setBrand] = useState("");
  const [contentType, setContentType] = useState("");
  const { jobs, isLoading, mutate } = useJobs({
    status: status || undefined,
    brand: brand || undefined,
    content_type: contentType || undefined,
  });
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div>
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Pipeline</h1>
          <p className="mt-1 text-sm text-gray-500">
            Content jobs run through the router → writer → auditor pipeline.
          </p>
        </div>
        <Button onClick={() => setShowCreate(true)}>New Job</Button>
      </div>

      <div className="mb-4 flex flex-wrap items-center gap-3" role="group" aria-label="Filter jobs">
        <select className={selectClass} value={status} onChange={(e) => setStatus(e.target.value)} aria-label="Filter by status">
          {JOB_STATUSES.map((s) => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
        <select className={selectClass} value={brand} onChange={(e) => setBrand(e.target.value)} aria-label="Filter by brand">
          {BRANDS.map((b) => (
            <option key={b.value} value={b.value}>{b.label}</option>
          ))}
        </select>
        <select className={selectClass} value={contentType} onChange={(e) => setContentType(e.target.value)} aria-label="Filter by content type">
          {CONTENT_TYPES.map((t) => (
            <option key={t.value} value={t.value}>{t.label}</option>
          ))}
        </select>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : jobs.length === 0 ? (
        <p className="text-sm text-gray-500">
          No jobs match the current filters. Start one with “New Job”.
        </p>
      ) : (
        <div className="space-y-3">
          {jobs.map((job) => (
            <JobRow key={job.id} job={job} onMutate={mutate} />
          ))}
        </div>
      )}

      {showCreate && (
        <CreateJobModal
          onClose={() => setShowCreate(false)}
          onCreated={() => {
            setShowCreate(false);
            mutate();
          }}
        />
      )}
    </div>
  );
}

function JobRow({ job, onMutate }: { job: JobSummary; onMutate: () => void }) {
  const [acting, setActing] = useState<string | null>(null);
  const [actionError, setActionError] = useState("");

  const act = useCallback(
    async (action: "approve" | "cancel", e: React.MouseEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setActing(action);
      setActionError("");
      try {
        await jobAction(job.id, action);
        onMutate();
      } catch (err) {
        setActionError(err instanceof Error ? err.message : "Action failed");
      } finally {
        setActing(null);
      }
    },
    [job.id, onMutate]
  );

  const canApprove = job.status === "awaiting_approval";
  const canCancel = job.status === "running" || job.status === "awaiting_approval";

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-colors hover:bg-gray-50">
      <div className="flex items-center justify-between gap-4">
        <Link
          href={`/jobs/${job.id}`}
          className="min-w-0 flex-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
        >
          <h3 className="truncate text-sm font-medium text-gray-900">{job.title}</h3>
          <p className="mt-1 text-xs text-gray-500">
            {job.brand ?? "unrouted"} · {job.content_type ?? "—"} ·{" "}
            {job.revision_count}/{job.max_revisions} revisions
          </p>
        </Link>
        <div className="flex shrink-0 items-center gap-3">
          <span className="hidden text-xs text-gray-500 sm:inline">
            {new Intl.DateTimeFormat("en-US", {
              dateStyle: "medium",
              timeStyle: "short",
            }).format(new Date(job.created_at))}
          </span>
          <Badge variant={jobStatusVariant(job.status)}>
            {job.status.replace("_", " ")}
          </Badge>
          {actionError && (
            <span className="text-xs text-red-600" role="alert">{actionError}</span>
          )}
          {canApprove && (
            <Button size="sm" loading={acting === "approve"} onClick={(e) => act("approve", e)}>
              Approve
            </Button>
          )}
          {canCancel && (
            <Button
              size="sm"
              variant="secondary"
              loading={acting === "cancel"}
              onClick={(e) => act("cancel", e)}
            >
              Cancel
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

function CreateJobModal({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: () => void;
}) {
  const [request, setRequest] = useState("");
  const [title, setTitle] = useState("");
  const [brand, setBrand] = useState("");
  const [contentType, setContentType] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setLoading(true);
      setError("");
      try {
        await createJob({
          request,
          title: title || undefined,
          brand: brand || undefined,
          content_type: contentType || undefined,
        });
        onCreated();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to create job");
      } finally {
        setLoading(false);
      }
    },
    [request, title, brand, contentType, onCreated]
  );

  return (
    <Modal open={true} onClose={onClose} title="New Content Job">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="job-request" className="block text-sm font-medium text-gray-700">
            Content Brief
          </label>
          <textarea
            id="job-request"
            rows={5}
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="e.g. Write a MasterShield vs LeafFilter comparison page"
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            required
            minLength={10}
          />
        </div>
        <Input
          id="job-title"
          label="Title (optional)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Defaults to the first line of the brief"
        />
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="job-brand" className="block text-sm font-medium text-gray-700">
              Brand
            </label>
            <select
              id="job-brand"
              value={brand}
              onChange={(e) => setBrand(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            >
              {BRANDS.map((b) => (
                <option key={b.value} value={b.value}>{b.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="job-type" className="block text-sm font-medium text-gray-700">
              Content Type
            </label>
            <select
              id="job-type"
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            >
              {CONTENT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>
        </div>
        {error && <p className="text-sm text-red-600" role="alert">{error}</p>}
        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={loading}>Start Pipeline</Button>
        </div>
      </form>
    </Modal>
  );
}
