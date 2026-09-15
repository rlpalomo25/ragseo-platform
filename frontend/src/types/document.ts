export interface Document {
  id: string;
  doc_number: string;
  title: string;
  filename: string;
  version?: string;
  series?: string;
  doc_type?: string;
  status: string;
  word_count?: number;
  last_updated?: string;
  snippet?: string;
  score?: number;
  chunk_count?: number;
  embedded_chunks?: number;
}

export interface DocumentDetail extends Document {
  content: string;
  file_hash?: string;
}

export interface DocumentListResponse {
  documents: Document[];
  total: number;
  page: number;
  page_size: number;
}

export interface DocReference {
  outgoing: { target: string; type: string }[];
  incoming: { doc_number: string; title: string }[];
}
