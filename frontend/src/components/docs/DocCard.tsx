import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import type { Document } from "@/types/document";

const typeColors: Record<string, "success" | "warning" | "info" | "default" | "danger"> = {
  doctrine: "info",
  agent: "success",
  playbook: "warning",
  brand_module: "default",
  system: "danger",
  schema: "info",
  sop: "warning",
};

function escapeRegExp(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function Highlighted({ text, terms }: { text: string; terms: string[] }) {
  const active = terms.filter((t) => t.length > 0);
  if (active.length === 0) return <>{text}</>;
  const pattern = new RegExp(`(${active.map(escapeRegExp).join("|")})`, "gi");
  const parts = text.split(pattern);
  return (
    <>
      {parts.map((part, i) =>
        active.some((t) => t.toLowerCase() === part.toLowerCase()) ? (
          <mark key={i} className="rounded-sm bg-amber-100 px-0.5 text-gray-900">
            {part}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

export function DocCard({ doc, search }: { doc: Document; search?: string }) {
  const hasCoverage = doc.chunk_count != null && doc.chunk_count > 0;
  const embedded = doc.embedded_chunks ?? 0;
  const coveragePct = hasCoverage ? Math.round((embedded / doc.chunk_count!) * 100) : null;
  const terms = (search || "").split(/\s+/);

  return (
    <Link
      href={`/docs/${doc.id}`}
      className="block rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <h3 className="truncate text-sm font-semibold text-gray-900">
            <Highlighted text={doc.title} terms={terms} />
          </h3>
          <p className="mt-1 truncate text-xs text-gray-500">
            <Highlighted text={doc.filename} terms={terms} />
          </p>
        </div>
        <div className="flex shrink-0 gap-1">
          {doc.series && <Badge variant="info">Doc {doc.series}</Badge>}
          {doc.doc_type && (
            <Badge variant={typeColors[doc.doc_type] || "default"}>
              {doc.doc_type}
            </Badge>
          )}
        </div>
      </div>
      {doc.snippet && (
        <p className="mt-3 line-clamp-2 text-xs leading-relaxed text-gray-600">
          <Highlighted text={doc.snippet} terms={terms} />
        </p>
      )}
      <div className="mt-3 flex items-center gap-3 text-xs text-gray-500">
        {doc.version && <span>v{doc.version}</span>}
        {doc.word_count != null && (
          <span style={{ fontVariantNumeric: "tabular-nums" }}>
            {doc.word_count.toLocaleString()} words
          </span>
        )}
        {doc.score != null && (
          <span style={{ fontVariantNumeric: "tabular-nums" }}>
            relevance {(doc.score * 100).toFixed(0)}%
          </span>
        )}
        <Badge variant={doc.status === "active" ? "success" : "warning"}>
          {doc.status}
        </Badge>
      </div>
      {hasCoverage && (
        <div className="mt-3">
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-500">Embedded</span>
            <span
              className={coveragePct === 100 ? "font-medium text-green-600" : "text-gray-600"}
              style={{ fontVariantNumeric: "tabular-nums" }}
            >
              {embedded} / {doc.chunk_count} chunks
            </span>
          </div>
          <div
            className="mt-1 h-1.5 overflow-hidden rounded-full bg-gray-100"
            role="progressbar"
            aria-valuenow={coveragePct ?? 0}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`${coveragePct}% of chunks embedded`}
          >
            <div
              className={`h-full rounded-full ${
                coveragePct === 100 ? "bg-green-500" : coveragePct! < 90 ? "bg-amber-500" : "bg-brand-500"
              }`}
              style={{ width: `${coveragePct}%` }}
            />
          </div>
        </div>
      )}
    </Link>
  );
}
