"use client";

import { useState, useCallback } from "react";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ExternalDataCard } from "@/components/ingest/ExternalDataCard";
import {
  useIngestStatus,
  runReingest,
} from "@/lib/hooks/useIngest";
import type {
  IngestFileStatus,
  IngestResultResponse,
  IngestTotals,
} from "@/types/ingest";

const STATUS_VARIANT: Record<string, "success" | "warning" | "info" | "danger" | "default"> = {
  new: "info",
  changed: "warning",
  unchanged: "success",
  error: "danger",
};

export default function IngestPage() {
  return (
    <AuthGuard requireAdmin>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <IngestContent />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function IngestContent() {
  const { data, isLoading, error, mutate } = useIngestStatus();
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<IngestResultResponse | null>(null);
  const [actionError, setActionError] = useState("");

  const reingest = useCallback(async () => {
    setRunning(true);
    setActionError("");
    setResult(null);
    try {
      const res = await runReingest();
      setResult(res);
      mutate();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Reingest failed");
    } finally {
      setRunning(false);
    }
  }, [mutate]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Data Ingest</h1>
        <p className="mt-1 text-sm text-gray-500">
          Scan the doctrine folder, preview changes, then re-ingest.
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      ) : error || !data ? (
        <p className="py-12 text-center text-sm text-red-600" role="alert">
          Failed to load ingest status. Is the backend running?
        </p>
      ) : (
        <>
          <div className="flex flex-wrap items-center justify-between gap-4">
            <p className="text-sm text-gray-500">
              Doctrine folder: <code className="rounded bg-gray-100 px-1.5 py-0.5 text-xs">{data.doctrine_path}</code>
              {" "}· add/edit <code className="rounded bg-gray-100 px-1.5 py-0.5 text-xs">.md</code> files there, then click Reingest.
            </p>
            <div className="flex items-center gap-3">
              {actionError && (
                <span className="text-sm text-red-600" role="alert">{actionError}</span>
              )}
              <Button onClick={reingest} loading={running}>
                {running ? "Ingesting…" : "Reingest Now"}
              </Button>
            </div>
          </div>

          <SummaryTiles totals={data.totals} />

          {result && <IngestResult result={result} />}

          <FileTable files={data.files} />

          <ExternalDataCard />
        </>
      )}
    </div>
  );
}

function SummaryTiles({ totals }: { totals: IngestTotals }) {
  const tiles = [
    { label: "Files on disk", value: totals.files, accent: "text-gray-900" },
    { label: "New", value: totals.new, accent: "text-brand-600" },
    { label: "Changed", value: totals.changed, accent: "text-amber-600" },
    { label: "Unchanged", value: totals.unchanged, accent: "text-green-600" },
  ];
  const coveragePct = totals.chunks ? Math.round(totals.embedded / totals.chunks * 100) : 0;
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
      {tiles.map((t) => (
        <div key={t.label} className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">{t.label}</p>
          <p className={`mt-1 text-2xl font-bold ${t.accent}`} style={{ fontVariantNumeric: "tabular-nums" }}>
            {t.value}
          </p>
        </div>
      ))}
      <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">Embed coverage</p>
        <p className="mt-1 text-2xl font-bold text-gray-900" style={{ fontVariantNumeric: "tabular-nums" }}>
          {coveragePct}%
        </p>
        <p className="text-xs text-gray-500">
          {totals.embedded.toLocaleString()} / {totals.chunks.toLocaleString()} chunks
        </p>
      </div>
    </div>
  );
}

function IngestResult({ result }: { result: IngestResultResponse }) {
  const { stats } = result;
  const rows = [
    { label: "Created", value: stats.created },
    { label: "Updated", value: stats.updated },
    { label: "Skipped", value: stats.skipped },
    { label: "Chunks written", value: stats.chunks },
    { label: "Embedding failures", value: stats.embedding_failures },
  ];
  return (
    <div className="rounded-lg border border-green-200 bg-green-50 p-4">
      <h2 className="text-sm font-semibold text-green-800">Last reingest · {result.message}</h2>
      <div className="mt-3 flex flex-wrap gap-x-8 gap-y-2">
        {rows.map((r) => (
          <div key={r.label}>
            <p className="text-xs text-green-700">{r.label}</p>
            <p className="text-lg font-bold text-green-900" style={{ fontVariantNumeric: "tabular-nums" }}>
              {r.value}
            </p>
          </div>
        ))}
      </div>
      {stats.errors.length > 0 && (
        <ul className="mt-3 space-y-1">
          {stats.errors.map((e, i) => (
            <li key={i} className="rounded bg-red-100 px-2 py-1 text-xs text-red-700">{e}</li>
          ))}
        </ul>
      )}
      {stats.embedding_failures > 0 && (
        <p className="mt-2 text-sm text-amber-700">
          {stats.embedding_failures} chunk{stats.embedding_failures === 1 ? "" : "s"} stored without embeddings.
        </p>
      )}
    </div>
  );
}

function FileTable({ files }: { files: IngestFileStatus[] }) {
  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">File</th>
            <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Doc</th>
            <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Words</th>
            <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Embedded</th>
            <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {files.map((f) => (
            <tr key={f.filename}>
              <td className="px-4 py-3 text-sm text-gray-900">
                <span className="block max-w-[26rem] truncate font-medium">{f.title}</span>
                <span className="block text-xs text-gray-500">{f.filename}</span>
              </td>
              <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-600">
                {f.doc_number || "—"}
                {f.series && <span className="ml-1 text-xs text-gray-400">(series {f.series})</span>}
              </td>
              <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-600" style={{ fontVariantNumeric: "tabular-nums" }}>
                {f.word_count.toLocaleString()}
              </td>
              <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-600" style={{ fontVariantNumeric: "tabular-nums" }}>
                {f.chunk_count > 0 ? `${f.embedded_chunks} / ${f.chunk_count}` : "—"}
              </td>
              <td className="whitespace-nowrap px-4 py-3 text-sm">
                {f.status === "error" ? (
                  <span className="text-xs text-red-600">{f.error}</span>
                ) : (
                  <Badge variant={STATUS_VARIANT[f.status] ?? "default"}>{f.status}</Badge>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}