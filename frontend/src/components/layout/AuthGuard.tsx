"use client";

import { useAuth } from "@/lib/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Spinner } from "@/components/ui/Spinner";

export function AuthGuard({ children, requireAdmin = false }: { children: React.ReactNode; requireAdmin?: boolean }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // replace, not push: the login-gated URL must not linger in the back-stack,
    // or Back after signing in bounces straight back to /login.
    if (!loading && !user) {
      router.replace("/login");
    }
    if (!loading && requireAdmin && user?.role !== "admin") {
      router.replace("/docs");
    }
  }, [user, loading, router, requireAdmin]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!user) return null;
  if (requireAdmin && user.role !== "admin") return null;

  return <>{children}</>;
}
