"use client";

import { useEffect, useRef, useState } from "react";
import { useWorkspaceStore } from "@/stores/workspace";
import ExportPanel from "./ExportPanel";

export default function DiagramPreview() {
  const currentDiagram = useWorkspaceStore((s) => s.currentDiagram);
  const containerRef = useRef<HTMLDivElement>(null);
  const [renderError, setRenderError] = useState<string | null>(null);

  useEffect(() => {
    if (!currentDiagram?.diagram_source || !containerRef.current) return;

    let cancelled = false;
    setRenderError(null);

    const render = async () => {
      try {
        const mermaid = await import("mermaid");
        mermaid.default.initialize({
          startOnLoad: false,
          theme: "default",
          securityLevel: "strict",
        });

        if (cancelled || !containerRef.current) return;

        const id = `mermaid-${Date.now()}`;
        const { svg } = await mermaid.default.render(
          id,
          currentDiagram.diagram_source,
        );

        if (cancelled || !containerRef.current) return;
        containerRef.current.innerHTML = svg;
      } catch (err) {
        if (!cancelled) {
          setRenderError(
            err instanceof Error ? err.message : "Failed to render diagram",
          );
          if (containerRef.current) {
            containerRef.current.innerHTML = `<pre class="text-xs text-red-600 bg-red-50 p-3 rounded border border-red-200 overflow-auto">${currentDiagram.diagram_source}</pre>`;
          }
        }
      }
    };

    render();

    return () => {
      cancelled = true;
    };
  }, [currentDiagram?.diagram_source]);

  if (!currentDiagram) {
    return (
      <div className="flex h-full flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 p-8 text-center">
        <div className="mb-3 text-4xl">📐</div>
        <h3 className="mb-1 text-lg font-semibold text-gray-700">No Diagram Yet</h3>
        <p className="max-w-xs text-sm text-gray-500">
          Enter a design system description in the chat panel and we&apos;ll generate a diagram for you.
        </p>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h3 className="text-base font-semibold text-gray-900">
            {currentDiagram.title}
          </h3>
          <p className="text-xs text-gray-500">
            {currentDiagram.diagram_type.replace(/-/g, " ")} &middot; Version{" "}
            {currentDiagram.version}
          </p>
        </div>
      </div>

      <div className="flex-1 overflow-auto rounded-lg border border-gray-200 bg-white p-4">
        <div ref={containerRef} className="flex justify-center">
          {/* Mermaid SVG renders here */}
        </div>
      </div>

      {renderError && (
        <div className="mt-2 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
          Render error: {renderError}. Showing source instead.
        </div>
      )}

      {currentDiagram.explanation && (
        <div className="mt-3 rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-xs text-gray-600">
          <span className="font-medium">Explanation:</span>{" "}
          {currentDiagram.explanation}
        </div>
      )}

      <ExportPanel
        diagramSource={currentDiagram.diagram_source}
        diagramFormat={currentDiagram.diagram_format}
        explanation={currentDiagram.explanation || ""}
      />
    </div>
  );
}
