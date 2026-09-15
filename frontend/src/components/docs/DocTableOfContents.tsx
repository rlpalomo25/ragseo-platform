"use client";

import { useState, useMemo } from "react";

interface Heading {
  id: string;
  text: string;
  level: number;
}

export function DocTableOfContents({ content }: { content: string }) {
  const headings = useMemo(() => {
    const result: Heading[] = [];
    const lines = content.split("\n");
    for (const line of lines) {
      const match = line.match(/^(#{1,6})\s+(.+)/);
      if (match) {
        const level = match[1].length;
        const text = match[2].trim();
        const id = text
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/(^-|-$)/g, "");
        result.push({ id, text, level });
      }
    }
    return result;
  }, [content]);

  if (headings.length === 0) return null;

  return (
    <nav aria-label="Table of contents" className="sticky top-20">
      <h2 className="mb-2 text-xs font-semibold uppercase text-gray-400">
        On this page
      </h2>
      <ul className="space-y-1 text-sm">
        {headings.map((h) => (
          <li key={h.id} style={{ paddingLeft: `${(h.level - 1) * 12}px` }}>
            <a
              href={`#${h.id}`}
              className="block truncate text-gray-600 hover:text-brand-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
            >
              {h.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
