"use client";

import { useCallback, useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { useAuth } from "@/lib/hooks/useAuth";
import {
  useDoctrineUploads,
  deleteDoctrineFiles,
  restoreDoctrineFiles,
} from "@/lib/hooks/useIngest";
import type { DoctrineUploadedDoc } from "@/types/ingest";

/**
 * Delete and undo for documents uploaded through the website.
 *
 * The list is the point: `/api/docs` only shows `active` rows and cannot say
 * which of them came from an upload, so this card is what makes the delete and
 * restore endpoints reachable at all. Deleted rows stay listed precisely so
 * undo is still available after the row leaves the doctrine list.
 *
 * Library documents never appear here — the server refuses to delete them, and
 * offering a button that would answer "library" would be worse than no button.
 */
export function DoctrineManageCard({ onChanged }: { onChanged?: () => void }) {
  const { user } = useAuth();
  const { data, isLoading, error, mutate } = useDoctrineUploads();
  const [busy, setBusy] = useState<string | null>(null);
  const [confirming, setConfirming] = useState<string | null>(null);
  const [notice, setNotice] = useState("");
  const [actionError, setActionError] = useState("");

  const uploads = data?.uploads ?? [];

  const run = useCallback(
    async (doc: DoctrineUploadedDoc, action: "delete" | "restore") => {
      setBusy(doc.filename);
      setActionError("");
      setNotice("");
      try {
        const res =
          action === "delete"
            ? await deleteDoctrineFiles([doc.filename])
            : await restoreDoctrineFiles([doc.filename]);
        setNotice(res.message);
        // A delete or restore changes the totals, the series breakdown and the
        // row itself, so revalidate the doctrine lists too, not just this one.
        await mutate();
        onChanged?.();
      } catch (err) {
        setActionError(err instanceof Error ? err.message : `${action} failed`);
      } finally {
        setBusy(null);
        setConfirming(null);
      }
    },
    [mutate, onChanged]
  );

  if (!user || (user.role !== "admin" && user.role !== "writer")) return null;

  return (
    <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Your uploaded doctrine
        </h2>
        {uploads.length > 0 && (
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {uploads.length} document{uploads.length === 1 ? "" : "s"}
          </span>
        )}
      </div>
      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
        Documents added through this website. Deleting one removes it from the agents&apos;
        retrieval immediately; undo brings it back with its chunks rebuilt.
      </p>

      {isLoading && (
        <div className="flex justify-center py-6">
          <Spinner />
        </div>
      )}

      {error && (
        <p className="mt-3 text-sm text-red-600 dark:text-red-400" role="alert">
          Could not load your uploaded documents.
        </p>
      )}

      {!isLoading && !error && uploads.length === 0 && (
        <p className="mt-3 text-sm text-gray-500 dark:text-gray-400">
          Nothing uploaded yet. Documents added with the upload form above appear here.
        </p>
      )}

      {uploads.length > 0 && (
        <ul className="mt-4 space-y-2">
          {uploads.map((doc) => {
            const isDeleted = doc.status === "deleted";
            const isBusy = busy === doc.filename;
            const isConfirming = confirming === doc.filename;
            return (
              <li
                key={doc.filename}
                className={`rounded-lg border p-3 ${
                  isDeleted
                    ? "border-gray-200 bg-gray-50 dark:border-gray-700 dark:bg-gray-900/40"
                    : "border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800"
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-gray-900 dark:text-gray-100">
                      Doc {doc.doc_number} &middot; {doc.title || doc.filename}
                    </p>
                    <p className="truncate text-xs text-gray-500 dark:text-gray-400">
                      {doc.filename}
                      {doc.chunks > 0 && <> &middot; {doc.chunks} chunks</>}
                    </p>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    <Badge variant={isDeleted ? "danger" : doc.status === "active" ? "success" : "warning"}>
                      {doc.status}
                    </Badge>
                    {isDeleted ? (
                      <Button
                        size="sm"
                        variant="secondary"
                        loading={isBusy}
                        onClick={() => run(doc, "restore")}
                      >
                        Undo
                      </Button>
                    ) : isConfirming ? (
                      <>
                        <Button
                          size="sm"
                          variant="danger"
                          loading={isBusy}
                          onClick={() => run(doc, "delete")}
                        >
                          Confirm delete
                        </Button>
                        <Button size="sm" variant="ghost" onClick={() => setConfirming(null)}>
                          Cancel
                        </Button>
                      </>
                    ) : (
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => setConfirming(doc.filename)}
                      >
                        Delete
                      </Button>
                    )}
                  </div>
                </div>
                {isConfirming && (
                  <p className="mt-2 text-xs text-amber-700 dark:text-amber-400">
                    Removes Doc {doc.doc_number} from agent retrieval. You can undo this
                    afterwards from this list.
                  </p>
                )}
              </li>
            );
          })}
        </ul>
      )}

      {notice && (
        <p className="mt-3 text-sm text-green-700 dark:text-green-400" role="status">
          {notice}
        </p>
      )}
      {actionError && (
        <p className="mt-3 text-sm text-red-600 dark:text-red-400" role="alert">
          {actionError}
        </p>
      )}
    </section>
  );
}
