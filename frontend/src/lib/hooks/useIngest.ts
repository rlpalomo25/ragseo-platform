"use client";

import useSWR from "swr";
import { apiFetch, apiUpload } from "@/lib/api";
import type {
  IngestStatusResponse,
  IngestResultResponse,
  ExternalStatusResponse,
  ExternalImportResultResponse,
  ExternalDeleteResultResponse,
} from "@/types/ingest";

const ingestFetcher = (url: string) => apiFetch<IngestStatusResponse>(url);
const externalFetcher = (url: string) => apiFetch<ExternalStatusResponse>(url);

export function useIngestStatus() {
  return useSWR<IngestStatusResponse>("/api/ingest/status", ingestFetcher, {
    refreshInterval: 30000,
    revalidateOnFocus: false,
  });
}

export async function runReingest(): Promise<IngestResultResponse> {
  return apiFetch<IngestResultResponse>("/api/ingest/reingest", {
    method: "POST",
  });
}

export function useExternalStatus() {
  return useSWR<ExternalStatusResponse>("/api/ingest/external/status", externalFetcher, {
    refreshInterval: 30000,
    revalidateOnFocus: false,
  });
}

export async function runExternalImport(): Promise<ExternalImportResultResponse> {
  return apiFetch<ExternalImportResultResponse>("/api/ingest/external", {
    method: "POST",
  });
}

export async function uploadExternalFiles(
  files: File[]
): Promise<ExternalImportResultResponse> {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  return apiUpload<ExternalImportResultResponse>("/api/ingest/external/upload", formData);
}

export async function deleteExternalFiles(
  filenames: string[]
): Promise<ExternalDeleteResultResponse> {
  return apiFetch<ExternalDeleteResultResponse>("/api/ingest/external/delete", {
    method: "DELETE",
    body: JSON.stringify({ filenames }),
  });
}
