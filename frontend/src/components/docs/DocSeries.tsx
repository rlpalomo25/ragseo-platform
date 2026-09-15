"use client";

const SERIES = [
  { value: "", label: "All" },
  { value: "100", label: "100 — Doctrine" },
  { value: "130", label: "130 — Brand" },
  { value: "140", label: "140 — Conversion" },
  { value: "150", label: "150 — Strategy" },
  { value: "160", label: "160 — Page Types" },
  { value: "170", label: "170 — Playbooks" },
  { value: "200", label: "200 — Performance" },
  { value: "220", label: "220 — Architecture" },
  { value: "300", label: "300 — Agents" },
  { value: "316", label: "316 — Companions" },
  { value: "350", label: "350 — SOT Pipeline" },
  { value: "430", label: "430 — Knowledge Graph" },
  { value: "900", label: "900 — Validation" },
];

interface DocSeriesProps {
  value: string;
  onChange: (value: string) => void;
}

export function DocSeries({ value, onChange }: DocSeriesProps) {
  return (
    <div className="flex flex-wrap gap-1" role="tablist" aria-label="Document series">
      {SERIES.map((s) => (
        <button
          key={s.value}
          role="tab"
          aria-selected={value === s.value}
          onClick={() => onChange(s.value)}
          className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 ${
            value === s.value
              ? "bg-brand-600 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          {s.label}
        </button>
      ))}
    </div>
  );
}
