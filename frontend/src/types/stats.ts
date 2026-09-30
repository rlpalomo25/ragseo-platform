export interface DocumentsStats {
  total: number;
  active: number;
  by_doc_type: Record<string, number>;
  by_series: Record<string, number>;
  by_status: Record<string, number>;
}

export interface ChunksStats {
  total: number;
  embedded: number;
  coverage: number; // 0..1
}

export interface JobsStats {
  total: number;
  by_status: Record<string, number>;
  avg_revisions: number;
  with_revisions: number;
  created_last_7d: number;
  created_last_30d: number;
  failed_stages: number;
}

export type SystemHealth = "healthy" | "warning" | "degraded";

export interface SystemStats {
  active_users: number;
  queued_jobs: number;
  avg_latency_seconds: number | null;
  health: SystemHealth;
}

export interface StatsResponse {
  documents: DocumentsStats;
  chunks: ChunksStats;
  jobs: JobsStats;
  system: SystemStats;
}