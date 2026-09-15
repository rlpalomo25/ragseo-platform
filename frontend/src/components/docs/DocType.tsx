"use client";

const TYPES = [
  { value: "", label: "All types" },
  { value: "doctrine", label: "Doctrine" },
  { value: "agent", label: "Agents" },
  { value: "playbook", label: "Playbooks" },
  { value: "brand_module", label: "Brand" },
  { value: "system", label: "System" },
  { value: "schema", label: "Schema" },
  { value: "sop", label: "SOP" },
  { value: "misc", label: "Other" },
];

interface DocTypeProps {
  value: string;
  onChange: (value: string) => void;
}

export function DocType({ value, onChange }: DocTypeProps) {
  return (
    <label className="flex items-center gap-2 text-sm text-gray-500">
      <span className="shrink-0">Type</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-gray-200 bg-gray-100 px-2 py-1.5 text-xs font-medium text-gray-600 transition-colors focus:outline-none focus:ring-2 focus:ring-brand-500"
      >
        {TYPES.map((t) => (
          <option key={t.value} value={t.value}>
            {t.label}
          </option>
        ))}
      </select>
    </label>
  );
}