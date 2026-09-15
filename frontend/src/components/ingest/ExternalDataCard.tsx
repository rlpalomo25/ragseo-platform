"use client";

import { useCallback, useMemo, useRef, useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { useAuth } from "@/lib/hooks/useAuth";
import {
  useExternalStatus,
  runExternalImport,
  uploadExternalFiles,
  deleteExternalFiles,
} from "@/lib/hooks/useIngest";
import type {
  ExternalFileStatus,
  ExternalImportResultResponse,
  ExternalTotals,
} from "@/types/ingest";

const SOURCE_LABELS: Record<string, string> = {
  search_console: "GSC",
  ai_overview: "AI Overview",
  ga4_event: "GA4",
  call_tracking: "Calls",
  lead_summary: "Leads",
  keyword_estimate: "Keywords",
  backlink: "Backlinks",
  top_page: "Top pages",
  traffic: "Traffic report",
  backlinks_report: "Backlink report",
};

const BULK_CONFIRM = "__bulk__";

export function ExternalDataCard() {
  const { data, isLoading, error, mutate } = useExternalStatus();
  const { user } = useAuth();
  const [running, setRunning] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [result, setResult] = useState<ExternalImportResultResponse | null>(null);
  const [deleteMessage, setDeleteMessage] = useState<string | null>(null);
  const [actionError, setActionError] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [confirming, setConfirming] = useState<string | null>(null);
  const [filesToUpload, setFilesToUpload] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const deletableFiles = useMemo(
    () => (data?.files ?? []).filter((f) => f.deletable),
    [data]
  );

  const onFilesChosen = useCallback((files: FileList | null) => {
    if (!files) {
      setFilesToUpload([]);
      return;
    }
    setFilesToUpload(Array.from(files));
  }, []);

  const upload = useCallback(async () => {
    if (filesToUpload.length === 0) return;
    setRunning(true);
    setActionError("");
    setResult(null);
    try {
      const res = await uploadExternalFiles(filesToUpload);
      setResult(res);
      setFilesToUpload([]);
      if (fileInputRef.current) fileInputRef.current.value = "";
      mutate();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setRunning(false);
    }
  }, [filesToUpload, mutate]);

  const runImport = useCallback(async () => {
    setRunning(true);
    setActionError("");
    setResult(null);
    try {
      const res = await runExternalImport();
      setResult(res);
      mutate();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Import failed");
    } finally {
      setRunning(false);
    }
  }, [mutate]);

  const deleteFiles = useCallback(
    async (names: string[]) => {
      if (names.length === 0) return;
      setDeleting(true);
      setActionError("");
      setDeleteMessage(null);
      try {
        const res = await deleteExternalFiles(names);
        setDeleteMessage(res.message);
        setSelected(new Set());
        mutate();
      } catch (err) {
        setActionError(err instanceof Error ? err.message : "Delete failed");
      } finally {
        setDeleting(false);
        setConfirming(null);
      }
    },
    [mutate]
  );

  const toggleFile = useCallback((filename: string, checked: boolean) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (checked) next.add(filename);
      else next.delete(filename);
      return next;
    });
  }, []);

  const toggleAll = useCallback(
    (checked: boolean) => {
      setSelected(checked ? new Set(deletableFiles.map((f) => f.filename)) : new Set());
    },
    [deletableFiles]
  );

  const isAdmin = user?.role === "admin";
  const allSelected = deletableFiles.length > 0 && selected.size === deletableFiles.length;

  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">External market data</h2>
          <p className="text-sm text-gray-500">
            Weekly GSC / AI-Overview / GA4 / Ubersuggest / calls / leads exports. Idempotent by file hash.
          </p>
        </div>
        {isAdmin && (
          <div className="flex items-center gap-3">
            <Button onClick={runImport} loading={running} variant="secondary">
              {running ? "Importing…" : "Import Exports"}
            </Button>
          </div>
        )}
      </div>

      <div className="mt-5 rounded-lg border border-dashed border-gray-300 bg-gray-50 p-4">
        <p className="text-sm font-medium text-gray-700">Upload this week&apos;s exports</p>
        <p className="mt-0.5 text-xs text-gray-500">
          Pick all exported files at once (.zip, .csv, .txt, .md) — they&apos;re saved, imported, and
          deduped by content hash automatically. Delete old weeks from the table below when they&apos;re
          no longer needed.
        </p>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".zip,.csv,.txt,.md"
            onChange={(e) => onFilesChosen(e.target.files)}
            className="block w-full max-w-sm text-sm text-gray-700 file:mr-3 file:rounded-md file:border-0 file:bg-brand-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-brand-700 sm:max-w-md"
            aria-label="Choose weekly export files to upload"
          />
          <Button onClick={upload} loading={running} disabled={filesToUpload.length === 0}>
            {running ? "Uploading…" : `Upload & Import${filesToUpload.length ? ` (${filesToUpload.length})` : ""}`}
          </Button>
        </div>
        {filesToUpload.length > 0 && (
          <ul className="mt-3 space-y-1">
            {filesToUpload.map((f) => (
              <li key={f.name} className="flex items-center justify-between gap-3 text-xs text-gray-600">
                <span className="truncate">{f.name}</span>
                <span className="shrink-0 tabular-nums text-gray-400">
                  {(f.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </li>
            ))}
          </ul>
        )}
        {actionError && <p className="mt-2 text-sm text-red-600" role="alert">{actionError}</p>}
      </div>

      {isLoading ? (
        <div className="flex justify-center py-8"><Spinner /></div>
      ) : error || !data ? (
        <p className="py-6 text-sm text-red-600" role="alert">
          Failed to load external export status. Is the backend running and the upload folder mounted?
        </p>
      ) : (
        <>
          <p className="mt-3 text-xs text-gray-400">
            Folder: <code className="rounded bg-gray-100 px-1.5 py-0.5">{data.external_data_path}</code>
          </p>
          <ExternalSummaryTotals totals={data.totals} />
          {result && <ExternalImportResult result={result} />}
          {deleteMessage && (
            <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-4">
              <h3 className="text-sm font-semibold text-green-800">{deleteMessage}</h3>
            </div>
          )}

          {deletableFiles.length > 0 && (
            <div className="mt-3 flex flex-wrap items-center justify-between gap-3 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2">
              <label className="flex cursor-pointer items-center gap-2 text-xs font-medium text-gray-700">
                <input
                  type="checkbox"
                  checked={allSelected}
                  onChange={(e) => toggleAll(e.target.checked)}
                  aria-label="Select all deletable exports"
                />
                Select all ({deletableFiles.length} deletable)
              </label>
              {confirming === BULK_CONFIRM ? (
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium text-red-700" role="alert">
                    Delete {selected.size} file{selected.size === 1 ? "" : "s"}? This removes their data too.
                  </span>
                  <Button
                    variant="danger"
                    size="sm"
                    loading={deleting}
                    onClick={() => deleteFiles(Array.from(selected))}
                  >
                    Confirm
                  </Button>
                  <Button variant="ghost" size="sm" disabled={deleting} onClick={() => setConfirming(null)}>
                    Cancel
                  </Button>
                </div>
              ) : (
                <Button
                  variant="danger"
                  size="sm"
                  disabled={selected.size === 0}
                  onClick={() => setConfirming(BULK_CONFIRM)}
                >
                  Delete selected ({selected.size})
                </Button>
              )}
            </div>
          )}

          <ExternalFileList
            files={data.files}
            selected={selected}
            confirming={confirming}
            deleting={deleting}
            onToggle={toggleFile}
            onRequestDelete={setConfirming}
            onConfirmDelete={deleteFiles}
            onCancelDelete={() => setConfirming(null)}
          />
        </>
      )}
    </section>
  );
}

function ExternalSummaryTotals({ totals }: { totals: ExternalTotals }) {
  const tiles = [
    { label: "Exports on disk", value: totals.files, accent: "text-gray-900" },
    { label: "Imported", value: totals.imported, accent: "text-green-600" },
    { label: "Errors", value: totals.errors, accent: "text-red-600" },
    { label: "Rows in DB", value: totals.rows, accent: "text-brand-600" },
  ];
  return (
    <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {tiles.map((t) => (
        <div key={t.label} className="rounded-lg border border-gray-200 bg-gray-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">{t.label}</p>
          <p className={`mt-1 text-2xl font-bold ${t.accent}`} style={{ fontVariantNumeric: "tabular-nums" }}>
            {t.value.toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
}

function ExternalImportResult({ result }: { result: ExternalImportResultResponse }) {
  return (
    <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-4">
      <h3 className="text-sm font-semibold text-green-800">{result.message}</h3>
      <div className="mt-2 flex flex-wrap gap-x-8 gap-y-1">
        <p className="text-xs text-green-700">Imported: <b>{result.imported}</b></p>
        <p className="text-xs text-green-700">Skipped: <b>{result.skipped}</b></p>
        <p className="text-xs text-green-700">Errors: <b>{result.errors}</b></p>
      </div>
      {result.errors > 0 && (
        <ul className="mt-2 space-y-1">
          {result.files.filter((f) => f.status === "error").map((f, i) => (
            <li key={i} className="rounded bg-red-100 px-2 py-1 text-xs text-red-700">
              {f.filename}: {f.error}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

type ExternalFileListProps = {
  files: ExternalFileStatus[];
  selected: Set<string>;
  confirming: string | null;
  deleting: boolean;
  onToggle: (filename: string, checked: boolean) => void;
  onRequestDelete: (filename: string) => void;
  onConfirmDelete: (filenames: string[]) => void;
  onCancelDelete: () => void;
};

function ExternalFileList({
  files,
  selected,
  confirming,
  deleting,
  onToggle,
  onRequestDelete,
  onConfirmDelete,
  onCancelDelete,
}: ExternalFileListProps) {
  return (
    <div className="mt-4 overflow-hidden rounded-lg border border-gray-200">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="w-10 px-4 py-2.5 text-left text-xs font-semibold uppercase text-gray-500">
              <span className="sr-only">Select</span>
            </th>
            <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold uppercase text-gray-500">File</th>
            <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold uppercase text-gray-500">Type</th>
            <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold uppercase text-gray-500">Domain</th>
            <th scope="col" className="px-4 py-2.5 text-right text-xs font-semibold uppercase text-gray-500">Rows</th>
            <th scope="col" className="px-4 py-2.5 text-left text-xs font-semibold uppercase text-gray-500">Status</th>
            <th scope="col" className="w-24 px-4 py-2.5 text-right text-xs font-semibold uppercase text-gray-500">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {files.map((f) => {
            const confirmingThis = confirming === f.filename;
            return (
              <tr key={f.filename} className={confirmingThis ? "bg-red-50" : ""}>
                <td className="px-4 py-2.5">
                  {f.deletable ? (
                    <input
                      type="checkbox"
                      checked={selected.has(f.filename)}
                      onChange={(e) => onToggle(f.filename, e.target.checked)}
                      aria-label={`Select ${f.filename}`}
                    />
                  ) : (
                    <span className="text-xs text-gray-300" title="Baked into the base dataset; cannot be deleted">
                      —
                    </span>
                  )}
                </td>
                <td className="max-w-[24rem] truncate px-4 py-2.5 text-sm text-gray-900">{f.filename}</td>
                <td className="whitespace-nowrap px-4 py-2.5 text-sm text-gray-600">
                  {SOURCE_LABELS[f.source_type ?? ""] ?? f.source_type ?? "—"}
                </td>
                <td className="whitespace-nowrap px-4 py-2.5 text-sm text-gray-600">{f.domain ?? "—"}</td>
                <td className="whitespace-nowrap px-4 py-2.5 text-right text-sm text-gray-600" style={{ fontVariantNumeric: "tabular-nums" }}>
                  {f.rows.toLocaleString()}
                </td>
                <td className="whitespace-nowrap px-4 py-2.5 text-sm">
                  {f.status === "error" ? (
                    <span className="text-xs text-red-600">{f.error}</span>
                  ) : (
                    <Badge variant={f.status === "imported" ? "success" : "default"}>{f.status}</Badge>
                  )}
                </td>
                <td className="whitespace-nowrap px-4 py-2.5 text-right">
                  {f.deletable ? (
                    confirmingThis ? (
                      <span className="inline-flex items-center gap-2">
                        <span className="text-xs font-medium text-red-700" role="alert">Delete this file + data?</span>
                        <Button
                          variant="danger"
                          size="sm"
                          loading={deleting}
                          onClick={() => onConfirmDelete([f.filename])}
                        >
                          Confirm
                        </Button>
                        <Button variant="ghost" size="sm" disabled={deleting} onClick={onCancelDelete}>
                          Cancel
                        </Button>
                      </span>
                    ) : (
                      <Button variant="ghost" size="sm" disabled={deleting} onClick={() => onRequestDelete(f.filename)}>
                        Delete
                      </Button>
                    )
                  ) : (
                    <span className="text-xs text-gray-300" title="Baked into the base dataset">baked</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}