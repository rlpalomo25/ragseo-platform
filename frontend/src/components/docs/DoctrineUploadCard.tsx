"use client";

import { useCallback, useRef, useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { uploadDoctrineFiles } from "@/lib/hooks/useIngest";
import { useAuth } from "@/lib/hooks/useAuth";
import type { DoctrineUploadResultResponse } from "@/types/ingest";

/** Mirrors the server-side caps in app/routers/ingest.py. */
const MAX_BYTES = 10 * 1024 * 1024;
const MAX_NAME_LEN = 255;
const MAX_FILES = 20;
const MAX_TOTAL_BYTES = 50 * 1024 * 1024;

/**
 * The filename contract the ingestion parser depends on. `DOC_PATTERN` needs a
 * `_` or `:` after the number; anything else is rejected with a 400 because
 * `extract_doc_number` would fall back to the whole filename and burn the doc
 * number permanently under the partial unique index. Catching it here turns a
 * server error into immediate, actionable feedback.
 */
const DOC_NAME = /^Doc\s+\d+(?:-\w+)?\s*[_:]\s*.+/i;

export function DoctrineUploadCard({ onUploaded }: { onUploaded?: () => void }) {
  const { user } = useAuth();
  const [files, setFiles] = useState<File[]>([]);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<DoctrineUploadResultResponse | null>(null);
  const [error, setError] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  // Batch-level caps, mirroring MAX_FILES / MAX_TOTAL_BYTES on the server.
  // Checked here as well as there because the server rejects the whole batch:
  // finding out client-side before the upload starts saves re-sending 50 MB to
  // receive a 413. These are appended after the per-file problems so the message
  // is stable and reads the same way every time.
  const batchProblems: string[] = [];
  if (files.length > MAX_FILES) {
    batchProblems.push(`${files.length} files selected: at most ${MAX_FILES} per upload`);
  }
  const totalBytes = files.reduce((sum, f) => sum + f.size, 0);
  if (totalBytes > MAX_TOTAL_BYTES) {
    batchProblems.push(
      `Total ${(totalBytes / 1024 / 1024).toFixed(1)} MB exceeds the 50 MB per-upload limit`,
    );
  }

  const localProblems = files
    .map((f) => {
      if (!f.name.toLowerCase().endsWith(".md")) return `${f.name}: must be a .md file`;
      if (f.name.length > MAX_NAME_LEN) return `${f.name}: name longer than ${MAX_NAME_LEN} characters`;
      if (f.size > MAX_BYTES) return `${f.name}: larger than 10 MB`;
      if (!DOC_NAME.test(f.name)) {
        return `${f.name}: needs a doc number and title, e.g. "Doc 100_Master Content Doctrine.md"`;
      }
      return null;
    })
    .filter((p): p is string => p !== null)
    .concat(batchProblems);

  const reset = useCallback(() => {
    setFiles([]);
    if (inputRef.current) inputRef.current.value = "";
  }, []);

  const submit = useCallback(async () => {
    if (files.length === 0 || localProblems.length > 0) return;
    setRunning(true);
    setError("");
    setResult(null);
    try {
      const res = await uploadDoctrineFiles(files);
      setResult(res);
      reset();
      onUploaded?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setRunning(false);
    }
  }, [files, localProblems.length, reset, onUploaded]);

  // The endpoint is writer-gated; hide the affordance entirely for a read-only
  // role rather than offering a button that answers 403.
  if (!user || (user.role !== "admin" && user.role !== "writer")) return null;

  const blocked = files.length > 0 && localProblems.length > 0;

  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Upload doctrine</h2>
      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
        Add or replace a doctrine document. Files are ingested immediately and become
        retrievable by the agents on their very next job.
      </p>

      <div className="mt-4 rounded-lg border border-dashed border-gray-300 bg-gray-50 p-4 dark:border-gray-600 dark:bg-gray-900/40">
        <p className="text-sm font-medium text-gray-700 dark:text-gray-200">
          Markdown only, named <code className="rounded bg-gray-200 px-1 dark:bg-gray-700">Doc &lt;number&gt;_&lt;Title&gt;.md</code>
        </p>
        <p className="mt-0.5 text-xs text-gray-500 dark:text-gray-400">
          Up to {MAX_FILES} files and 50 MB per upload, 10 MB each. Re-uploading the same
          filename replaces that document; uploading a different filename with an
          existing doc number supersedes the current one. Library documents shipped with
          the app are read-only here.
        </p>

        <div className="mt-3 flex flex-wrap items-center gap-3">
          <input
            ref={inputRef}
            type="file"
            multiple
            accept=".md,text/markdown"
            onChange={(e) => {
              setFiles(Array.from(e.target.files ?? []));
              setResult(null);
              setError("");
            }}
            className="block w-full max-w-sm text-sm text-gray-700 file:mr-3 file:rounded-md file:border-0 file:bg-brand-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-brand-700 sm:max-w-md dark:text-gray-300"
            aria-label="Choose doctrine markdown files to upload"
          />
          <Button
            onClick={submit}
            loading={running}
            disabled={files.length === 0 || blocked}
          >
            {running
              ? "Uploading…"
              : `Upload${files.length ? ` (${files.length})` : ""}`}
          </Button>
          {files.length > 0 && !running && (
            <Button variant="ghost" size="sm" onClick={reset}>
              Clear
            </Button>
          )}
        </div>

        {files.length > 0 && (
          <ul className="mt-3 space-y-1">
            {files.map((f) => (
              <li key={f.name} className="flex items-center justify-between gap-3 text-xs text-gray-600 dark:text-gray-400">
                <span className="truncate">{f.name}</span>
                <span className="shrink-0 tabular-nums text-gray-400">
                  {(f.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </li>
            ))}
          </ul>
        )}

        {localProblems.length > 0 && (
          <ul className="mt-3 space-y-1" role="alert">
            {localProblems.map((p) => (
              <li key={p} className="rounded bg-red-100 px-2 py-1 text-xs text-red-700 dark:bg-red-950 dark:text-red-300">
                {p}
              </li>
            ))}
          </ul>
        )}

        {error && (
          <p className="mt-2 text-sm text-red-600 dark:text-red-400" role="alert">
            {error}
          </p>
        )}
      </div>

      {result && <DoctrineUploadResult result={result} />}
    </section>
  );
}

function DoctrineUploadResult({ result }: { result: DoctrineUploadResultResponse }) {
  const tone =
    result.errors > 0
      ? "border-yellow-300 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-950/40"
      : "border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-950/40";

  return (
    <div className={`mt-4 rounded-lg border p-4 ${tone}`}>
      <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">{result.message}</h3>
      <div className="mt-2 flex flex-wrap gap-x-6 gap-y-1 text-xs text-gray-700 dark:text-gray-300">
        <span>Created: <b>{result.created}</b></span>
        <span>Updated: <b>{result.updated}</b></span>
        <span>Unchanged: <b>{result.unchanged}</b></span>
        <span>Chunks: <b>{result.chunks}</b></span>
        <span>Errors: <b>{result.errors}</b></span>
      </div>
      <ul className="mt-3 space-y-1">
        {result.files.map((f) => (
          <li
            key={f.filename}
            className="flex flex-wrap items-center gap-2 rounded bg-white/60 px-2 py-1 text-xs dark:bg-gray-900/40"
          >
            <span className="font-medium text-gray-900 dark:text-gray-100">
              Doc {f.doc_number}
            </span>
            <span className="truncate text-gray-600 dark:text-gray-400">{f.title || f.filename}</span>
            <Badge variant={f.status === "error" ? "danger" : "success"}>{f.status}</Badge>
            {f.chunks > 0 && (
              <span className="tabular-nums text-gray-500 dark:text-gray-400">
                {f.chunks} chunks
              </span>
            )}
            {f.superseded && (
              <span className="text-amber-700 dark:text-amber-400">
                superseded Doc {f.superseded}
              </span>
            )}
            {f.error && <span className="text-red-600 dark:text-red-400">{f.error}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
