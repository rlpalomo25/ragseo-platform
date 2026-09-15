"use client";

import { use } from "react";
import Link from "next/link";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { DocViewer } from "@/components/docs/DocViewer";
import { DocTableOfContents } from "@/components/docs/DocTableOfContents";
import { useDoc } from "@/lib/hooks/useDocs";
import { useDocReferences } from "@/lib/hooks/useDocReferences";

export default function DocDetailPage({ params }: { params: Promise<{ docId: string }> }) {
  const { docId } = use(params);
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <DocDetailContent docId={docId} />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function DocDetailContent({ docId }: { docId: string }) {
  const { data: doc, isLoading, error } = useDoc(docId);
  const { data: refs } = useDocReferences(docId);

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !doc) {
    return (
      <p className="py-12 text-center text-sm text-red-600" role="alert">
        Failed to load document.
      </p>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <Link
          href="/docs"
          className="text-sm text-brand-600 hover:text-brand-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
        >
          ← Back to documents
        </Link>
        <div className="mt-2 flex items-start gap-3">
          <h1 className="text-2xl font-bold text-gray-900">{doc.title}</h1>
          {doc.version && <Badge>v{doc.version}</Badge>}
          {doc.doc_type && <Badge>{doc.doc_type}</Badge>}
        </div>
        <p className="mt-1 text-sm text-gray-500">{doc.filename}</p>
        {doc.chunk_count != null && (
          <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
            <span>Embedded</span>
            <div className="h-1.5 w-40 overflow-hidden rounded-full bg-gray-100" aria-hidden="true">
              <div
                className={`h-full rounded-full ${
                  doc.embedded_chunks === doc.chunk_count
                    ? "bg-green-500"
                    : (doc.embedded_chunks ?? 0) < doc.chunk_count * 0.9
                    ? "bg-amber-500"
                    : "bg-brand-500"
                }`}
                style={{
                  width: `${doc.chunk_count ? Math.round(((doc.embedded_chunks ?? 0) / doc.chunk_count) * 100) : 0}%`,
                }}
              />
            </div>
            <span style={{ fontVariantNumeric: "tabular-nums" }}>
              {doc.embedded_chunks ?? 0} / {doc.chunk_count} chunks
            </span>
          </div>
        )}
      </div>

      {refs && refs.outgoing.length > 0 && (
        <div className="mb-6 rounded-lg border border-gray-200 bg-gray-50 p-4">
          <h2 className="mb-2 text-sm font-semibold text-gray-700">References</h2>
          <div className="flex flex-wrap gap-1">
            {refs.outgoing.map((r) => (
              <span key={r.target} className="rounded bg-gray-200 px-2 py-0.5 text-xs text-gray-600">
                Doc {r.target}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-8">
        <div className="min-w-0 flex-1">
          <DocViewer content={doc.content} />
        </div>
        <div className="hidden w-56 shrink-0 lg:block">
          <DocTableOfContents content={doc.content} />
        </div>
      </div>
    </div>
  );
}
