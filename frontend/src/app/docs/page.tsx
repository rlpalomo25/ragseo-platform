"use client";

import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { DocList } from "@/components/docs/DocList";

export default function DocsPage() {
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-gray-900">Doctrine Reference</h1>
              <p className="mt-1 text-sm text-gray-500">
                Browse, search, and cross-reference all RAGSEO doctrine documents.
              </p>
            </div>
            <DocList />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}
