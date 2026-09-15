"use client";

import { apiFetch } from "@/lib/api";
import type { DocReference } from "@/types/document";
import useSWR from "swr";

export function useDocReferences(docId: string | null) {
  return useSWR<DocReference>(
    docId ? `/api/docs/${docId}/references` : null,
    (url) => apiFetch<DocReference>(url),
    { revalidateOnFocus: false }
  );
}
