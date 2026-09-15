"use client";

interface DocSearchProps {
  value: string;
  onChange: (value: string) => void;
}

export function DocSearch({ value, onChange }: DocSearchProps) {
  return (
    <div className="relative">
      <label htmlFor="doc-search" className="sr-only">
        Search documents
      </label>
      <input
        id="doc-search"
        type="search"
        placeholder="Search documents…"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        autoComplete="off"
        spellCheck={false}
        className="w-full rounded-md border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm shadow-sm placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
      />
      <svg
        className="absolute left-3 top-2.5 h-4 w-4 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
  );
}
