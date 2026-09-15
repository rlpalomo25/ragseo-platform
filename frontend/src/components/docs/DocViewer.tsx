"use client";

import ReactMarkdown from "react-markdown";

export function DocViewer({ content }: { content: string }) {
  return (
    <article className="prose prose-gray max-w-none prose-headings:scroll-mt-20 prose-a:text-brand-600 prose-code:text-sm prose-pre:bg-gray-900">
      <ReactMarkdown
        components={{
          h1: ({ children, ...props }) => (
            <h1 id={slugify(children)} {...props}>{children}</h1>
          ),
          h2: ({ children, ...props }) => (
            <h2 id={slugify(children)} {...props}>{children}</h2>
          ),
          h3: ({ children, ...props }) => (
            <h3 id={slugify(children)} {...props}>{children}</h3>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </article>
  );
}

function slugify(children: React.ReactNode): string {
  const text = extractText(children);
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function extractText(node: React.ReactNode): string {
  if (typeof node === "string") return node;
  if (typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(extractText).join("");
  if (node && typeof node === "object" && "props" in node) {
    return extractText((node as React.ReactElement).props.children);
  }
  return "";
}
