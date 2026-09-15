export interface JobSummary {
  id: string;
  title: string;
  status: string;
  brand: string | null;
  content_type: string | null;
  revision_count: number;
  max_revisions: number;
  created_at: string;
  updated_at: string;
}

export interface StageDetail {
  id: string;
  sequence: number;
  agent_type: string;
  task_id: string | null;
  status: string;
  feedback: string | null;
  task_status: string | null;
  output_data: Record<string, unknown> | null;
  error_message: string | null;
}

export interface JobDetail extends JobSummary {
  request: string;
  notes: string | null;
  stages: StageDetail[];
}

export function jobStatusVariant(
  status: string
): "success" | "warning" | "danger" | "info" | "default" {
  switch (status) {
    case "approved":
      return "success";
    case "awaiting_approval":
      return "warning";
    case "running":
      return "info";
    case "failed":
      return "danger";
    default:
      return "default";
  }
}
