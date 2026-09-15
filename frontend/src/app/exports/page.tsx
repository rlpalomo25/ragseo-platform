"use client";

import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { ExternalDataCard } from "@/components/ingest/ExternalDataCard";

export default function ExportsPage() {
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <div className="space-y-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Weekly Exports</h1>
                <p className="mt-1 text-sm text-gray-500">
                  Upload this week&apos;s GSC / AI-Overview / GA4 / Ubersuggest / calls / leads exports.
                  Files are imported immediately and deduped by content hash.
                </p>
              </div>
              <ExternalDataCard />
            </div>
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}