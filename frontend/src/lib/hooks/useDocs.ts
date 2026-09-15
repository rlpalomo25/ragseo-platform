"use client";

import useSWR from "swr";
import { apiFetch } from "@/lib/api";
import type { DocumentListResponse, DocumentDetail } from "@/types/document";

const fetcher = (url: string) => apiFetch<DocumentListResponse>(url);

export function useDocs(params: {
  page?: number;
  series?: string;
  doc_type?: string;
  search?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.set("page", String(params.page));
  if (params.series) searchParams.set("series", params.series);
  if (params.doc_type) searchParams.set("doc_type", params.doc_type);

  let url = "/api/docs";
  if (params.search) {
    url = `/api/docs/search?q=${encodeURIComponent(params.search)}`;
    if (params.page) searchParams.set("page", String(params.page));
  }

  const query = searchParams.toString();
  const fullUrl = query ? `${url}?${query}` : url;

  return useSWR<DocumentListResponse>(fullUrl, fetcher, {
    revalidateOnFocus: false,
  });
}

export function useDoc(id: string | null) {
  return useSWR<DocumentDetail>(
    id ? `/api/docs/${id}` : null,
    (url) => apiFetch<DocumentDetail>(url),
    { revalidateOnFocus: false }
  );
}
