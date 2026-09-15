"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/hooks/useAuth";

const navItems = [
  { href: "/", label: "Dashboard", icon: "📊" },
  { href: "/docs", label: "Doctrine", icon: "📖" },
  { href: "/exports", label: "Weekly Exports", icon: "📤" },
  { href: "/jobs", label: "Pipeline", icon: "🔄" },
  { href: "/agents", label: "Agents", icon: "🤖" },
];

const adminItems = [
  { href: "/ingest", label: "Data Ingest", icon: "📥" },
  { href: "/admin/users", label: "Users", icon: "👥" },
];

export function Sidebar() {
  const { user } = useAuth();
  const pathname = usePathname();

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <aside className="fixed left-0 top-0 z-30 h-screen w-64 border-r border-gray-200 bg-white">
      <div className="flex h-14 items-center border-b border-gray-200 px-4">
        <Link href="/" className="text-lg font-bold text-gray-900">
          RAGSEO
        </Link>
      </div>
      <nav className="space-y-1 px-3 py-4" aria-label="Main navigation">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 ${
              isActive(item.href)
                ? "bg-brand-50 text-brand-700"
                : "text-gray-700"
            }`}
          >
            <span className="mr-3" aria-hidden="true">{item.icon}</span>
            {item.label}
          </Link>
        ))}

        {user?.role === "admin" && (
          <>
            <div className="my-2 border-t border-gray-200" role="separator" />
            <p className="px-3 py-1 text-xs font-semibold uppercase text-gray-400">
              Admin
            </p>
            {adminItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 ${
                  isActive(item.href)
                    ? "bg-brand-50 text-brand-700"
                    : "text-gray-700"
                }`}
              >
                <span className="mr-3" aria-hidden="true">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </>
        )}
      </nav>
    </aside>
  );
}
