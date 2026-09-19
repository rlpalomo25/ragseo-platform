"use client";

import { useCallback, useState } from "react";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { useAuth } from "@/lib/hooks/useAuth";
import {
  recomputeSnapshots,
  useFlags,
  usePublications,
} from "@/lib/hooks/useLearning";
import {
  FLAG_LABELS,
  flagBadgeVariant,
  type PerformanceSignal,
  type Publication,
} from "@/types/learning";

export default function LearningPage() {
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <LearningContent />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function LearningContent() {
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";
  const { publications, isLoading, mutate: mutatePublications } = usePublications();
  const { flags, isLoading: flagsLoading, mutate: mutateFlags } = useFlags(isAdmin);
  const [recomputing, setRecomputing] = useState(false);
  const [recomputeMsg, setRecomputeMsg] = useState<{ success: boolean; text: string } | null>(null);

  const runRecompute = useCallback(async () => {
    setRecomputing(true);
    setRecomputeMsg(null);
    try {
      const res = await recomputeSnapshots();
      await mutatePublications();
      await mutateFlags();
      setRecomputeMsg({
        success: true,
        text: `Recomputed ${res.snapshots} snapshot(s) across ${res.publications} publication(s), ${res.signals} new signal(s).`,
      });
    } catch (err) {
      setRecomputeMsg({
        success: false,
        text: err instanceof Error ? err.message : "Recompute failed",
      });
    } finally {
      setRecomputing(false);
    }
  }, [mutatePublications, mutateFlags]);

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Performance Memory</h1>
          <p className="mt-1 text-sm text-gray-500">
            Published content linked to pipeline jobs, and the weekly flags the learning loop
            generates from GSC / AI-Overview / GA4 / calls data (Doc 203 §7.0).
          </p>
        </div>
        {isAdmin && (
          <Button loading={recomputing} onClick={runRecompute}>
            Recompute now
          </Button>
        )}
      </div>

      {recomputeMsg && (
        <p
          className={`text-sm ${recomputeMsg.success ? "text-green-600" : "text-red-600"}`}
          role={recomputeMsg.success ? "status" : "alert"}
        >
          {recomputeMsg.text}
        </p>
      )}

      <section>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Registered Publications</h2>
        {isLoading ? (
          <div className="flex justify-center py-8">
            <Spinner />
          </div>
        ) : publications.length === 0 ? (
          <EmptyState text="No publications linked yet. Link one from an approved job&apos;s detail page." />
        ) : (
          <ul className="space-y-3">
            {publications.map((pub) => (
              <li key={pub.id}>
                <PublicationCard pub={pub} />
              </li>
            ))}
          </ul>
        )}
      </section>

      {isAdmin && (
        <section>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Flag Signals</h2>
            {flags && (
              <Badge variant={flags.count > 0 ? "warning" : "success"}>
                {flags.count} active
              </Badge>
            )}
          </div>
          {flagsLoading ? (
            <div className="flex justify-center py-8">
              <Spinner />
            </div>
          ) : !flags || flags.signals.length === 0 ? (
            <EmptyState text="No flag signals yet — register publications and run weekly exports." />
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Flag</th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">URL</th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Observation</th>
                    <th scope="col" className="px-4 py-3 text-right text-xs font-semibold uppercase text-gray-500">When</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {flags.signals.map((signal) => (
                    <SignalRow key={signal.id} signal={signal} />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

function PublicationCard({ pub }: { pub: Publication }) {
  return (
    <Card>
      <CardContent>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="text-sm font-medium text-gray-900">{pub.publish_url}</p>
            <p className="mt-0.5 text-xs text-gray-500">
              {pub.job_title || "Unlinked job"}
              {pub.target_keyword ? ` · Keyword: ${pub.target_keyword}` : ""}
              {pub.publish_date ? ` · Published ${pub.publish_date}` : ""}
            </p>
          </div>
          <Badge variant={pub.status === "active" ? "success" : "default"}>{pub.status}</Badge>
        </div>
        {pub.latest ? (
          <div className="mt-3 rounded border border-gray-100 bg-gray-50 p-3 text-sm text-gray-700">
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
              {pub.latest.position != null && (
                <span>Pos <strong>{pub.latest.position.toFixed(1)}</strong></span>
              )}
              <span>{pub.latest.impressions.toLocaleString()} imp</span>
              <span>{pub.latest.clicks.toLocaleString()} clicks</span>
              {pub.latest.ctr != null && <span>CTR <strong>{pub.latest.ctr.toFixed(1)}%</strong></span>}
              <span>{pub.latest.ai_overview_impressions} AI-imp</span>
              <span>{pub.latest.calls} calls</span>
              {pub.latest.est_visits != null && (
                <span>~{pub.latest.est_visits.toLocaleString()} visits</span>
              )}
              {pub.latest.movement != null && (
                <span
                  className={
                    pub.latest.movement > 0
                      ? "font-medium text-red-600"
                      : "font-medium text-green-600"
                  }
                >
                  {pub.latest.movement > 0 ? "▼" : "▲"} {Math.abs(pub.latest.movement).toFixed(1)} pos
                </span>
              )}
            </div>
            {pub.latest.flags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {pub.latest.flags.map((flag) => (
                  <span key={flag} title={FLAG_LABELS[flag] ?? flag}>
                    <Badge variant={flagBadgeVariant(flag)}>{flag}</Badge>
                  </span>
                ))}
              </div>
            )}
          </div>
        ) : (
          <p className="mt-3 text-xs text-gray-500">
            No snapshot yet — it will appear after the next exports import.
          </p>
        )}
      </CardContent>
    </Card>
  );
}

function SignalRow({ signal }: { signal: PerformanceSignal }) {
  const shortName = signal.source.replace(/^pub_perf:/, "");
  return (
    <tr>
      <td className="whitespace-nowrap px-4 py-3 text-sm">
        <span title={FLAG_LABELS[shortName] ?? signal.source}>
          <Badge variant={flagBadgeVariant(shortName)}>{shortName}</Badge>
        </span>
      </td>
      <td className="px-4 py-3 text-sm text-gray-900">{signal.publish_url || "—"}</td>
      <td className="px-4 py-3 text-sm text-gray-600">{signal.observation}</td>
      <td className="whitespace-nowrap px-4 py-3 text-right text-sm text-gray-500">
        {new Intl.DateTimeFormat("en-US", { dateStyle: "medium", timeStyle: "short" }).format(
          new Date(signal.created_at)
        )}
      </td>
    </tr>
  );
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="rounded-lg border border-dashed border-gray-300 bg-gray-50 p-6 text-center text-sm text-gray-500">
      {text}
    </div>
  );
}