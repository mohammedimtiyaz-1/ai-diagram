"use client";

import { useWorkspaceStore } from "@/stores/workspace";

export default function VersionHistory() {
  const versions = useWorkspaceStore((s) => s.diagramVersions);
  const currentDiagram = useWorkspaceStore((s) => s.currentDiagram);

  if (versions.length <= 1) return null;

  return (
    <div className="mt-3 rounded-lg border border-gray-200 bg-white p-3">
      <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
        Versions
      </h4>
      <div className="flex flex-col gap-1.5">
        {versions.map((v) => (
          <div
            key={v.diagram_id}
            className={`cursor-pointer rounded-md px-2 py-1.5 text-xs transition ${
              currentDiagram?.diagram_id === v.diagram_id
                ? "bg-black text-white"
                : "hover:bg-gray-100"
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-medium">v{v.version}</span>
              <span className="opacity-70">{v.diagram_type.replace(/-/g, " ")}</span>
            </div>
            {v.changes_summary.length > 0 && (
              <div className="mt-0.5 opacity-80">
                {v.changes_summary.join(", ")}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
