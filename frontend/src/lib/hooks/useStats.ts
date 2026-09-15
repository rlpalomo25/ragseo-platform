"use client";

import useSWR from "swr";
import { apiFetch } from "@/lib/api";
import type { StatsResponse } from "@/types/stats";

export function useStats() {
  return useSWR<StatsResponse>("/api/stats", (url) => apiFetch<StatsResponse>(url), {
    refreshInterval: 15000,
    revalidateOnFocus: false,
  });
}