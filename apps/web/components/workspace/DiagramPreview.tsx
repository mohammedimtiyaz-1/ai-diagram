"use client";

import { useEffect, useRef, useState, useMemo } from "react";
import { useWorkspaceStore } from "@/stores/workspace";
import DiagramStyleToolbar from "./DiagramStyleToolbar";
import NodeTooltip from "./NodeTooltip";
import { NodeMetadata } from "@/lib/api";
import { Download, FileJson, Code } from "lucide-react";

const FONT_MAP: Record<string, string> = {
  Inter: "'Inter', sans-serif",
  Arial: "Arial, sans-serif",
  Roboto: "'Roboto', sans-serif",
  System: "system-ui, sans-serif",
};

const SIZE_MAP: Record<string, string> = {
  small: "10px",
  medium: "13px",
  large: "16px",
};

const BG_MAP: Record<string, string> = {
  default: "#eff6ff", // blue-50
  white: "#ffffff",
  "soft-blue": "#f0f9ff", // sky-50
  "soft-purple": "#faf5ff", // purple-50
  "soft-gray": "#f9fafb", // gray-50
};

const THEME_MAP: Record<string, string> = {
  default: "",
  technical: `
    classDef default fill:#f8fafc,stroke:#334155,stroke-width:1px,color:#0f172a,rx:2,ry:2;
    classDef component fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af;
    classDef token fill:#f0fdf4,stroke:#16a34a,stroke-width:1px,color:#166534,stroke-dasharray: 5 5;
  `,
  soft: `
    classDef default fill:#ffffff,stroke:#e2e8f0,stroke-width:1px,rx:10,ry:10;
    classDef component fill:#fdf4ff,stroke:#d946ef,stroke-width:1px;
    classDef token fill:#fff7ed,stroke:#f97316,stroke-width:1px;
  `,
  colorful: `
    classDef default fill:#ffffff,stroke:#000000,stroke-width:2px;
    classDef token fill:#ffe4e6,stroke:#e11d48,stroke-width:2px;
    classDef component fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef documentation fill:#fef9c3,stroke:#ca8a04,stroke-width:2px;
  `,
  dark: `
    classDef default fill:#1e293b,stroke:#475569,stroke-width:1px,color:#f8fafc;
    classDef component fill:#1e1b4b,stroke:#4f46e5,stroke-width:2px,color:#e0e7ff;
    classDef token fill:#064e3b,stroke:#10b981,stroke-width:1px,color:#d1fae5;
  `,
  enterprise: `
    classDef default fill:#f1f5f9,stroke:#64748b,stroke-width:1px,rx:0,ry:0;
    classDef component fill:#0f172a,stroke:#0f172a,stroke-width:1px,color:#ffffff,rx:0,ry:0;
    classDef token fill:#ffffff,stroke:#cbd5e1,stroke-width:1px,rx:0,ry:0;
  `,
};

export default function DiagramPreview() {
  const currentDiagram = useWorkspaceStore((s) => s.currentDiagram);
  const containerRef = useRef<HTMLDivElement>(null);
  const [renderError, setRenderError] = useState<string | null>(null);
  const [isExporting, setIsExporting] = useState(false);

  // Tooltip state
  const [tooltip, setTooltip] = useState<{
    visible: boolean;
    metadata: NodeMetadata | null;
    x: number;
    y: number;
  }>({
    visible: false,
    metadata: null,
    x: 0,
    y: 0,
  });

  // Map nodes for fast lookup by ID
  const nodeMetadataMap = useMemo(() => {
    if (!currentDiagram?.nodes) return new Map();
    return new Map(currentDiagram.nodes.map((n) => [n.id, n.metadata]));
  }, [currentDiagram?.nodes]);

  const handleExport = async (format: "mmd" | "json") => {
    if (!currentDiagram || isExporting) return;
    setIsExporting(true);

    try {
      let content = "";
      let filename = "";
      let mimeType = "text/plain";

      if (format === "mmd") {
        content = currentDiagram.diagram_source;
        filename = "design-system-diagram.mmd";
        mimeType = "text/plain";
      } else {
        content = JSON.stringify(
          {
            diagram_id: currentDiagram.diagram_id,
            title: currentDiagram.title,
            source: currentDiagram.diagram_source,
            nodes: currentDiagram.nodes,
            edges: currentDiagram.edges,
            style: currentDiagram.style,
            explanation: currentDiagram.explanation,
            exportedAt: new Date().toISOString(),
          },
          null,
          2,
        );
        filename = "design-system-diagram.json";
        mimeType = "application/json";
      }

      const blob = new Blob([content], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Export failed:", error);
    } finally {
      setIsExporting(false);
    }
  };

  useEffect(() => {
    if (!currentDiagram?.diagram_source || !containerRef.current) return;

    let cancelled = false;
    setRenderError(null);

    const render = async () => {
      try {
        const mermaid = await import("mermaid");
        
        const style = currentDiagram.style || {
          font_family: "Inter",
          font_size: "medium",
          node_background_color: "default"
        };
        
        const fontFamily = FONT_MAP[style.font_family] || FONT_MAP.Inter;
        const fontSize = SIZE_MAP[style.font_size] || SIZE_MAP.medium;
        const mainBkg = BG_MAP[style.node_background_color] || BG_MAP.default;

        mermaid.default.initialize({
          startOnLoad: false,
          theme: "base",
          themeVariables: {
            fontFamily,
            fontSize,
            mainBkg,
            clusterBkg: "#f8fafc",
            clusterBorder: "#e2e8f0",
            lineColor: "#64748b",
            primaryColor: mainBkg,
            tertiaryColor: "#ffffff",
          },
          securityLevel: "loose",
        });

        if (cancelled || !containerRef.current) return;

        const id = `mermaid-${Date.now()}`;
        
        // Append theme styles to the source
        const themeStyles = THEME_MAP[style.node_theme || "default"] || "";
        const diagramSourceWithTheme = `${currentDiagram.diagram_source}\n${themeStyles}`;

        const { svg } = await mermaid.default.render(
          id,
          diagramSourceWithTheme,
        );

        if (cancelled || !containerRef.current) return;
        containerRef.current.innerHTML = svg;

        // Attach event listeners to nodes
        const nodes = containerRef.current.querySelectorAll(".node, .mermaid-node");
        nodes.forEach((node) => {
          const nodeId = node.id.split("-")[1] || node.id;
          const classList = Array.from(node.classList);
          const possibleId = classList.find(c => c.startsWith('id-'))?.replace('id-', '') || nodeId;

          node.addEventListener("mouseenter", (e: any) => {
            const meta = nodeMetadataMap.get(possibleId) || nodeMetadataMap.get(nodeId);
            if (meta) {
              setTooltip({
                visible: true,
                metadata: meta,
                x: e.clientX,
                y: e.clientY,
              });
            }
          });

          node.addEventListener("mousemove", (e: any) => {
            setTooltip((prev) => ({ ...prev, x: e.clientX, y: e.clientY }));
          });

          node.addEventListener("mouseleave", () => {
            setTooltip((prev) => ({ ...prev, visible: false }));
          });
        });

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
  }, [currentDiagram?.diagram_source, currentDiagram?.style, nodeMetadataMap]);

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
    <div className="flex h-full flex-col relative overflow-hidden">
      {/* Compact Header */}
      <div className="flex items-start justify-between pb-2 border-b border-gray-100 mb-3">
        <div className="flex-1 min-w-0 pr-4">
          <div className="flex items-center gap-2 mb-0.5">
            <h3 className="text-sm font-bold text-gray-900 truncate">
              {currentDiagram.title}
            </h3>
            <span className="text-[10px] bg-gray-100 text-gray-500 px-1.5 py-0.5 rounded-full font-medium">
              v{currentDiagram.version}
            </span>
          </div>
          {currentDiagram.explanation && (
            <p className="text-[11px] text-gray-600 leading-relaxed max-w-2xl line-clamp-2">
              {currentDiagram.explanation}
            </p>
          )}
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <button
            onClick={() => handleExport("mmd")}
            disabled={isExporting}
            className="flex items-center gap-1 px-2 py-1 text-[10px] font-bold bg-white border border-gray-200 rounded hover:bg-gray-50 transition-colors shadow-sm disabled:opacity-50"
            title="Download Mermaid Source (.mmd)"
          >
            <Code className="w-3 h-3" />
            <span>MMD</span>
          </button>
          <button
            onClick={() => handleExport("json")}
            disabled={isExporting}
            className="flex items-center gap-1 px-2 py-1 text-[10px] font-bold bg-white border border-gray-200 rounded hover:bg-gray-50 transition-colors shadow-sm disabled:opacity-50"
            title="Download Data (.json)"
          >
            <FileJson className="w-3 h-3" />
            <span>JSON</span>
          </button>
        </div>
      </div>

      <DiagramStyleToolbar />

      {/* Main Diagram Area - Dominant focus */}
      <div className="flex-1 overflow-auto rounded-xl border border-gray-100 bg-white p-4 shadow-inner ring-1 ring-gray-50 relative group">
        <div ref={containerRef} className="flex justify-center min-h-full">
          {/* Mermaid SVG renders here */}
        </div>
        {renderError && (
          <div className="absolute inset-0 flex items-center justify-center bg-white/90 p-4">
            <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-xs text-red-700 shadow-sm max-w-md">
              <p className="font-bold mb-1">Render Error</p>
              <p className="font-mono text-[10px]">{renderError}</p>
            </div>
          </div>
        )}
      </div>

      {/* Diagram Description - Requested: "plain english format that explains the diagram" */}
      <details className="mt-3 group">
        <summary className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-gray-400 cursor-pointer hover:text-gray-600 transition-colors">
          <span className="w-4 h-4 flex items-center justify-center transition-transform group-open:rotate-90">▶</span>
          Diagram Description
        </summary>
        <div className="mt-2 rounded-lg bg-gray-50 border border-gray-100 p-4 shadow-sm">
          <p className="text-xs leading-relaxed text-gray-700">
            {currentDiagram.explanation || "This diagram visualizes the structure and flow of your design system request."}
          </p>
          {currentDiagram.nodes.length > 0 && (
            <div className="mt-3 border-t border-gray-200 pt-3">
              <h4 className="text-[10px] font-bold uppercase tracking-tighter text-gray-500 mb-2">Components Breakdown</h4>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-2">
                {currentDiagram.nodes.slice(0, 6).map(node => (
                  <li key={node.id} className="flex items-start gap-2">
                    <span className="w-1 h-1 rounded-full bg-blue-400 mt-1.5 shrink-0" />
                    <div className="flex flex-col">
                      <span className="text-[11px] font-bold text-gray-800 leading-tight">{node.label}</span>
                      <span className="text-[10px] text-gray-500 italic leading-tight">{node.metadata.role}</span>
                    </div>
                  </li>
                ))}
                {currentDiagram.nodes.length > 6 && (
                  <li className="text-[10px] text-gray-400 italic mt-1">...and {currentDiagram.nodes.length - 6} more elements</li>
                )}
              </ul>
            </div>
          )}
        </div>
      </details>

      {tooltip.metadata && (
        <NodeTooltip
          metadata={tooltip.metadata}
          x={tooltip.x}
          y={tooltip.y}
          visible={tooltip.visible}
        />
      )}
    </div>
  );
}
