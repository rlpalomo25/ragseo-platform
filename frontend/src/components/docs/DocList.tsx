"use client";

import { useEffect, useState } from "react";
import { useDocs } from "@/lib/hooks/useDocs";
import { DocSearch } from "./DocSearch";
import { DocSeries } from "./DocSeries";
import { DocType } from "./DocType";
import { DocCard } from "./DocCard";
import { Spinner } from "@/components/ui/Spinner";

export function DocList() {
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [series, setSeries] = useState("");
  const [docType, setDocType] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    const t = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1);
    }, 300);
    return () => clearTimeout(t);
  }, [search]);

  const { data, isLoading, error } = useDocs({
    page,
    series: series || undefined,
    doc_type: docType || undefined,
    search: debouncedSearch || undefined,
  });

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <DocSearch
          value={search}
          onChange={setSearch}
        />
        <DocType
          value={docType}
          onChange={(v) => {
            setDocType(v);
            setPage(1);
          }}
        />
      </div>
      <DocSeries
        value={series}
        onChange={(v) => {
          setSeries(v);
          setPage(1);
        }}
      />

      {isLoading && (
        <div className="flex justify-center py-12">
          <Spinner size="lg" />
        </div>
      )}

      {error && (
        <p className="py-8 text-center text-sm text-red-600" role="alert">
          Failed to load documents. Please try again.
        </p>
      )}

      {data && data.documents.length === 0 && (
        <p className="py-12 text-center text-sm text-gray-500">
          No documents found. Try adjusting your search or filters.
        </p>
      )}

      {data && data.documents.length > 0 && (
        <>
          <p className="text-sm text-gray-500">
            {data.total.toLocaleString()} document{data.total !== 1 ? "s" : ""}
          </p>
          <div className="space-y-3">
            {data.documents.map((doc) => (
              <DocCard key={doc.id} doc={doc} search={search} />
            ))}
          </div>
          {data.total > data.page_size && (
            <div className="flex justify-center gap-2 pt-4">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="rounded-md px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 disabled:opacity-50"
              >
                Previous
              </button>
              <span className="flex items-center px-3 text-sm text-gray-500">
                Page {page} of {Math.ceil(data.total / data.page_size)}
              </span>
              <button
                onClick={() => setPage((p) => p + 1)}
                disabled={page >= Math.ceil(data.total / data.page_size)}
                className="rounded-md px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 disabled:opacity-50"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
