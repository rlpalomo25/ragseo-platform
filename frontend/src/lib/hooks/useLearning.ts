import useSWR from "swr";
import { apiFetch } from "@/lib/api";
import type {
  FlagsResponse,
  Publication,
  PublicationsResponse,
  RecomputeResponse,
  RegisterPublicationBody,
} from "@/types/learning";

export function usePublications() {
  const { data, isLoading, mutate } = useSWR<PublicationsResponse>(
    "/api/publications",
    (url: string) => apiFetch<PublicationsResponse>(url)
  );
  return { publications: data?.publications ?? [], isLoading, mutate };
}

export function useFlags(enabled = true) {
  const key = enabled ? "/api/learning/flags" : null;
  const { data, isLoading, mutate } = useSWR<FlagsResponse>(
    key,
    (url: string) => apiFetch<FlagsResponse>(url)
  );
  return { flags: data, isLoading, mutate };
}

export async function registerPublication(
  jobId: string,
  body: RegisterPublicationBody
): Promise<Publication> {
  return apiFetch<Publication>(`/api/jobs/${jobId}/publication`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function recomputeSnapshots(): Promise<RecomputeResponse> {
  return apiFetch<RecomputeResponse>("/api/learning/recompute", {
    method: "POST",
  });
}