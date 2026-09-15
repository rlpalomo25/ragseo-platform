import useSWR from "swr";
import { apiFetch } from "@/lib/api";
import type { JobDetail, JobSummary } from "@/types/job";

export interface JobFilters {
  status?: string;
  brand?: string;
  content_type?: string;
}

export function useJobs(filters?: JobFilters) {
  const params = new URLSearchParams();
  if (filters?.status) params.set("status", filters.status);
  if (filters?.brand) params.set("brand", filters.brand);
  if (filters?.content_type) params.set("content_type", filters.content_type);
  const query = params.toString();
  const { data, isLoading, mutate } = useSWR<{ jobs: JobSummary[] }>(
    `/api/jobs${query ? `?${query}` : ""}`,
    (url: string) => apiFetch<{ jobs: JobSummary[] }>(url),
    { refreshInterval: 5000 }
  );
  return { jobs: data?.jobs ?? [], isLoading, mutate };
}

export function useJob(jobId: string | null) {
  const { data, isLoading, mutate } = useSWR<JobDetail>(
    jobId ? `/api/jobs/${jobId}` : null,
    (url: string) => apiFetch<JobDetail>(url),
    {
      refreshInterval: (data) =>
        data && ["running", "awaiting_approval"].includes(data.status)
          ? 4000
          : 0,
    }
  );
  return { job: data, isLoading, mutate };
}

export async function createJob(body: {
  request: string;
  title?: string;
  brand?: string;
  content_type?: string;
}): Promise<JobSummary> {
  return apiFetch<JobSummary>("/api/jobs", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function jobAction(
  jobId: string,
  action: "approve" | "cancel"
): Promise<JobSummary> {
  return apiFetch<JobSummary>(`/api/jobs/${jobId}/${action}`, {
    method: "POST",
  });
}
