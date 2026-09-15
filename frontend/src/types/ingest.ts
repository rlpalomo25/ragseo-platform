export interface IngestFileStatus {
  filename: string;
  doc_number: string;
  title: string;
  series: string | null;
  doc_type: string | null;
  version: string | null;
  word_count: number;
  status: "new" | "changed" | "unchanged" | "error";
  error: string | null;
  chunk_count: number;
  embedded_chunks: number;
}

export interface IngestTotals {
  files: number;
  new: number;
  changed: number;
  unchanged: number;
  errors: number;
  chunks: number;
  embedded: number;
  embedding_coverage: number;
}

export interface IngestStatusResponse {
  doctrine_path: string;
  totals: IngestTotals;
  files: IngestFileStatus[];
}

export interface IngestStats {
  created: number;
  updated: number;
  skipped: number;
  chunks: number;
  embedding_failures: number;
  errors: string[];
}

export interface IngestResultResponse {
  message: string;
  stats: IngestStats;
}

// --- External market-data imports ---

export interface ExternalFileStatus {
  filename: string;
  source_type: string | null;
  domain: string | null;
  brand: string | null;
  status: "new" | "imported" | "error";
  rows: number;
  error: string | null;
  deletable: boolean;
}

export interface ExternalTotals {
  files: number;
  imported: number;
  errors: number;
  rows: number;
}

export interface ExternalStatusResponse {
  external_data_path: string;
  totals: ExternalTotals;
  files: ExternalFileStatus[];
}

export interface ExternalImportItem {
  filename: string;
  source_type: string | null;
  status: string;
  rows: number;
  error: string | null;
}

export interface ExternalImportResultResponse {
  message: string;
  imported: number;
  skipped: number;
  errors: number;
  files: ExternalImportItem[];
}

export interface ExternalDeleteItem {
  filename: string;
  status: "deleted" | "baked" | "not_found";
  message: string | null;
}

export interface ExternalDeleteResultResponse {
  message: string;
  deleted: number;
  baked: number;
  not_found: number;
  files: ExternalDeleteItem[];
}