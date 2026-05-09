"use client";

import { NodeMetadata } from "@/lib/api";

interface NodeTooltipProps {
  metadata: NodeMetadata;
  x: number;
  y: number;
  visible: boolean;
}

export default function NodeTooltip({ metadata, x, y, visible }: NodeTooltipProps) {
  if (!visible) return null;

  return (
    <div
      className="fixed z-50 w-64 rounded-lg border border-gray-200 bg-white p-3 shadow-xl ring-1 ring-black ring-opacity-5 transition-all duration-200 animate-in fade-in zoom-in-95"
      style={{
        left: x + 10,
        top: y + 10,
      }}
    >
      <div className="mb-1 flex items-center justify-between">
        <h4 className="text-sm font-bold text-gray-900">{metadata.tooltip_title}</h4>
        <span
          className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
            metadata.importance === "high"
              ? "bg-red-100 text-red-700"
              : metadata.importance === "medium"
                ? "bg-blue-100 text-blue-700"
                : "bg-gray-100 text-gray-700"
          }`}
        >
          {metadata.importance}
        </span>
      </div>
      
      <div className="mb-2 text-[10px] font-medium uppercase tracking-tight text-gray-400">
        Role: {metadata.role}
      </div>

      <p className="mb-2 text-xs leading-relaxed text-gray-600">
        {metadata.tooltip_description}
      </p>

      {metadata.connections_summary && (
        <div className="border-t border-gray-100 pt-2 mb-2">
          <p className="text-[10px] font-semibold text-gray-900 uppercase tracking-tighter mb-0.5">
            Connections
          </p>
          <p className="text-[11px] italic text-gray-500">
            {metadata.connections_summary}
          </p>
        </div>
      )}

      {metadata.related_files && metadata.related_files.length > 0 && (
        <div className="border-t border-gray-100 pt-2">
          <p className="text-[10px] font-semibold text-gray-900 uppercase tracking-tighter mb-1">
            Source Files
          </p>
          <div className="flex flex-wrap gap-1">
            {metadata.related_files.map((file, i) => (
              <span
                key={i}
                className="rounded bg-gray-50 border border-gray-200 px-1.5 py-0.5 text-[9px] font-mono text-gray-600 truncate max-w-full"
                title={file}
              >
                {file.split('/').pop()}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
