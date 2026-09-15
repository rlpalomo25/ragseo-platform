"use client";

import { useAuth } from "@/lib/hooks/useAuth";
import { Badge } from "@/components/ui/Badge";

export function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-20 flex h-14 items-center justify-between border-b border-gray-200 bg-white px-6">
      <div />
      <div className="flex items-center gap-3">
        {user && (
          <>
            <span className="text-sm text-gray-600">{user.username}</span>
            <Badge variant={user.role === "admin" ? "info" : "default"}>
              {user.role}
            </Badge>
            <button
              onClick={logout}
              className="rounded-md px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
            >
              Sign out
            </button>
          </>
        )}
      </div>
    </header>
  );
}
