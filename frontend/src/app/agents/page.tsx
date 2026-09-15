"use client";

import useSWR from "swr";
import { useState, useCallback } from "react";
import { apiFetch } from "@/lib/api";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";

interface Agent {
  name: string;
  display_name: string;
  status: string;
}

interface AgentTask {
  id: string;
  agent_type: string;
  status: string;
  input_data: Record<string, unknown>;
  output_data: Record<string, unknown> | null;
  error_message: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

const fetcher = (url: string) => apiFetch<{ agents: Agent[] }>(url);
const tasksFetcher = (url: string) => apiFetch<{ tasks: AgentTask[] }>(url);

export default function AgentsPage() {
  return (
    <AuthGuard>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <AgentsContent />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function AgentsContent() {
  const { data, isLoading } = useSWR("/api/agents", fetcher);
  const { data: tasksData, mutate: mutateTasks } = useSWR("/api/agents/tasks?limit=20", tasksFetcher);
  const [runAgent, setRunAgent] = useState<string | null>(null);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Agents</h1>
        <p className="mt-1 text-sm text-gray-500">
          Run AI agents against your doctrine library.
        </p>
      </div>

      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {isLoading ? (
          <div className="flex justify-center py-8 col-span-full">
            <Spinner size="lg" />
          </div>
        ) : (
          data?.agents.map((agent) => (
            <div
              key={agent.name}
              className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {agent.display_name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">{agent.name}</p>
                </div>
                <Badge variant="success">{agent.status}</Badge>
              </div>
              <Button
                onClick={() => setRunAgent(agent.name)}
                className="mt-4 w-full"
              >
                Run Agent
              </Button>
            </div>
          ))
        )}
      </div>

      <div>
        <h2 className="mb-4 text-lg font-semibold text-gray-900">Recent Tasks</h2>
        {tasksData && tasksData.tasks.length === 0 && (
          <p className="text-sm text-gray-500">No tasks run yet.</p>
        )}
        <div className="space-y-3">
          {tasksData?.tasks.map((task) => (
            <TaskRow key={task.id} task={task} />
          ))}
        </div>
      </div>

      {runAgent && (
        <RunAgentModal
          agentType={runAgent}
          onClose={() => setRunAgent(null)}
          onRun={() => {
            setRunAgent(null);
            mutateTasks();
          }}
        />
      )}
    </div>
  );
}

function statusVariant(status: string): "success" | "warning" | "danger" | "info" | "default" {
  switch (status) {
    case "completed": return "success";
    case "running": return "info";
    case "pending": return "warning";
    case "failed": return "danger";
    default: return "default";
  }
}

function TaskRow({ task }: { task: AgentTask }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between p-4 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
      >
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-gray-900">{task.agent_type}</span>
          <Badge variant={statusVariant(task.status)}>{task.status}</Badge>
        </div>
        <span className="text-xs text-gray-500">
          {new Intl.DateTimeFormat("en-US", {
            dateStyle: "medium",
            timeStyle: "short",
          }).format(new Date(task.created_at))}
        </span>
      </button>
      {expanded && (
        <div className="border-t border-gray-100 px-4 pb-4">
          <div className="mt-3">
            <h4 className="text-xs font-semibold uppercase text-gray-400">Input</h4>
            <pre className="mt-1 overflow-x-auto rounded bg-gray-50 p-3 text-xs text-gray-700">
              {JSON.stringify(task.input_data, null, 2)}
            </pre>
          </div>
          {task.output_data && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold uppercase text-gray-400">Output</h4>
              <pre className="mt-1 overflow-x-auto rounded bg-gray-50 p-3 text-xs text-gray-700">
                {JSON.stringify(task.output_data, null, 2)}
              </pre>
            </div>
          )}
          {task.error_message && (
            <div className="mt-3">
              <h4 className="text-xs font-semibold uppercase text-red-400">Error</h4>
              <pre className="mt-1 overflow-x-auto rounded bg-red-50 p-3 text-xs text-red-700">
                {task.error_message}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function RunAgentModal({
  agentType,
  onClose,
  onRun,
}: {
  agentType: string;
  onClose: () => void;
  onRun: () => void;
}) {
  const [request, setRequest] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await apiFetch("/api/agents/run", {
        method: "POST",
        body: JSON.stringify({
          agent_type: agentType,
          input_data: { request },
        }),
      });
      onRun();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to run agent");
    } finally {
      setLoading(false);
    }
  }, [agentType, request, onRun]);

  return (
    <Modal open={true} onClose={onClose} title={`Run ${agentType}`}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="request" className="block text-sm font-medium text-gray-700">
            Request / Content Brief
          </label>
          <textarea
            id="request"
            rows={5}
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="Describe the content request you want the agent to process…"
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            required
          />
        </div>
        {error && <p className="text-sm text-red-600" role="alert">{error}</p>}
        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={loading}>Run</Button>
        </div>
      </form>
    </Modal>
  );
}
