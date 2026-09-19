export interface PublicationSnapshot {
  period_to: string | null;
  position: number | null;
  clicks: number;
  impressions: number;
  ctr: number | null;
  ai_overview_impressions: number;
  calls: number;
  est_visits: number | null;
  movement: number | null;
  movement_ctr: number | null;
  movement_impressions: number | null;
  flags: string[];
}

export interface Publication {
  id: string;
  job_id: string;
  job_title: string;
  publish_url: string;
  publish_date: string | null;
  target_keyword: string | null;
  status: string;
  created_at: string;
  latest: PublicationSnapshot | null;
}

export interface PerformanceSignal {
  id: string;
  publication_id: string;
  publish_url: string;
  source: string;
  observation: string;
  action_taken: string | null;
  result: string | null;
  created_at: string;
}

export interface PublicationsResponse {
  publications: Publication[];
}

export interface FlagsResponse {
  count: number;
  signals: PerformanceSignal[];
}

export interface RecomputeResponse {
  publications: number;
  snapshots: number;
  signals: number;
}

export interface RegisterPublicationBody {
  url: string;
  target_keyword?: string;
  publish_date?: string;
}

export const FLAG_LABELS: Record<string, string> = {
  position_drop: "continued / decreased ranking (>3 positions change)",
  ctr_drop: "CTR change beyond 20%",
  movement: "impressions/visibility change beyond 20%",
  ai_zero: "zero AI-Overview impressions on latest snapshot",
  unmeasurable: "no ranking data matched this publication",
};

export type BadgeVariant = "default" | "success" | "warning" | "danger" | "info";

export function flagBadgeVariant(flag: string): BadgeVariant {
  switch (flag) {
    case "position_drop":
      return "danger";
    case "ctr_drop":
    case "movement":
      return "warning";
    case "ai_zero":
      return "info";
    default:
      return "default";
  }
}