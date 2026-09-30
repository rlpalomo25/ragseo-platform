"use client";

import { useState, useCallback } from "react";
import { apiFetch } from "@/lib/api";
import type { User } from "@/types/auth";
import useSWR from "swr";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { SkipLink } from "@/components/ui/SkipLink";
import { Spinner } from "@/components/ui/Spinner";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";

const fetcher = (url: string) => apiFetch<{ users: User[]; total: number }>(url);

export default function AdminUsersPage() {
  return (
    <AuthGuard requireAdmin>
      <SkipLink />
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="ml-64 flex-1">
          <Header />
          <main id="main-content" className="p-6" tabIndex={-1}>
            <UsersContent />
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}

function UsersContent() {
  const { data, isLoading, mutate } = useSWR("/api/users", fetcher);
  const [showCreate, setShowCreate] = useState(false);
  const [editUser, setEditUser] = useState<User | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [actionError, setActionError] = useState("");

  const deactivate = useCallback(
    async (user: User) => {
      if (!window.confirm(`Deactivate ${user.username}? They will be signed out and cannot log in again.`)) return;
      setBusyId(user.id);
      setActionError("");
      try {
        await apiFetch(`/api/users/${user.id}`, { method: "DELETE" });
        await mutate();
      } catch (err) {
        setActionError(err instanceof Error ? err.message : "Failed to deactivate user");
      } finally {
        setBusyId(null);
      }
    },
    [mutate]
  );

  const restore = useCallback(
    async (user: User) => {
      setBusyId(user.id);
      setActionError("");
      try {
        await apiFetch(`/api/users/${user.id}/restore`, { method: "POST" });
        await mutate();
      } catch (err) {
        setActionError(err instanceof Error ? err.message : "Failed to restore user");
      } finally {
        setBusyId(null);
      }
    },
    [mutate]
  );

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Users</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage user accounts & access.
          </p>
        </div>
        <Button onClick={() => setShowCreate(true)}>Create User</Button>
      </div>

      {actionError && (
        <p className="mb-4 rounded border border-red-100 bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">
          {actionError}
        </p>
      )}

      <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Username</th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Role</th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Status</th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Last Login</th>
              <th scope="col" className="px-4 py-3 text-right text-xs font-semibold uppercase text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {data?.users.map((user) => (
              <tr key={user.id}>
                <td className="whitespace-nowrap px-4 py-3 text-sm font-medium text-gray-900">{user.username}</td>
                <td className="whitespace-nowrap px-4 py-3 text-sm">
                  <Badge variant={user.role === "admin" ? "info" : "default"}>{user.role}</Badge>
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-sm">
                  {user.deleted_at ? (
                    <Badge variant="danger">Deleted</Badge>
                  ) : (
                    <Badge variant={user.is_active ? "success" : "warning"}>
                      {user.is_active ? "Active" : "Inactive"}
                    </Badge>
                  )}
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-500">
                  {user.last_login
                    ? new Intl.DateTimeFormat("en-US", { dateStyle: "medium", timeStyle: "short" }).format(new Date(user.last_login))
                    : "Never"}
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-right text-sm">
                  <div className="flex items-center justify-end gap-3">
                    {user.deleted_at ? (
                      <Button size="sm" loading={busyId === user.id} onClick={() => restore(user)}>
                        Restore
                      </Button>
                    ) : (
                      <>
                        <button
                          onClick={() => setEditUser(user)}
                          className="text-brand-600 hover:text-brand-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
                        >
                          Edit
                        </button>
                        {user.is_active && (
                          <button
                            onClick={() => deactivate(user)}
                            disabled={busyId === user.id}
                            className="text-red-600 hover:text-red-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 disabled:opacity-50"
                          >
                            Deactivate
                          </button>
                        )}
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <CreateUserModal open={showCreate} onClose={() => setShowCreate(false)} onCreated={() => mutate()} />
      {editUser && (
        <EditUserModal user={editUser} onClose={() => setEditUser(null)} onUpdated={() => mutate()} />
      )}
    </div>
  );
}

function CreateUserModal({ open, onClose, onCreated }: { open: boolean; onClose: () => void; onCreated: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("writer");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await apiFetch("/api/users", {
        method: "POST",
        body: JSON.stringify({ username, password, role }),
      });
      onCreated();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }, [username, password, role, onCreated, onClose]);

  return (
    <Modal open={open} onClose={onClose} title="Create User">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Username"
          name="username"
          autoComplete="off"
          spellCheck={false}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <Input
          label="Password"
          name="password"
          type="password"
          autoComplete="new-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <div>
          <label htmlFor="role" className="block text-sm font-medium text-gray-700">Role</label>
          <select
            id="role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          >
            <option value="writer">Writer</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        {error && <p className="text-sm text-red-600" role="alert">{error}</p>}
        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={loading}>Create</Button>
        </div>
      </form>
    </Modal>
  );
}

function EditUserModal({ user, onClose, onUpdated }: { user: User; onClose: () => void; onUpdated: () => void }) {
  const [role, setRole] = useState(user.role);
  const [isActive, setIsActive] = useState(user.is_active);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await apiFetch(`/api/users/${user.id}`, {
        method: "PUT",
        body: JSON.stringify({ role, is_active: isActive }),
      });
      onUpdated();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update user");
    } finally {
      setLoading(false);
    }
  }, [user.id, role, isActive, onUpdated, onClose]);

  return (
    <Modal open={true} onClose={onClose} title={`Edit ${user.username}`}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="edit-role" className="block text-sm font-medium text-gray-700">Role</label>
          <select
            id="edit-role"
            value={role}
            onChange={(e) => setRole(e.target.value as "admin" | "writer")}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          >
            <option value="writer">Writer</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div className="flex items-center gap-2">
          <input
            id="edit-active"
            type="checkbox"
            checked={isActive}
            onChange={(e) => setIsActive(e.target.checked)}
            className="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500"
          />
          <label htmlFor="edit-active" className="text-sm text-gray-700">Active</label>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={loading}>Save</Button>
        </div>
      </form>
    </Modal>
  );
}
