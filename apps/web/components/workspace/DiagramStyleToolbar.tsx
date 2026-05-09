"use client";

import { DiagramStyle } from "@/lib/api";
import { useWorkspaceStore } from "@/stores/workspace";
import { api } from "@/lib/api";

const COLOR_SWATCHES = [
  { id: "default", hex: "#eff6ff" },
  { id: "white", hex: "#ffffff" },
  { id: "soft-blue", hex: "#f0f9ff" },
  { id: "soft-purple", hex: "#faf5ff" },
  { id: "soft-gray", hex: "#f9fafb" },
];

export default function DiagramStyleToolbar() {
  const currentDiagram = useWorkspaceStore((s) => s.currentDiagram);
  const setCurrentDiagram = useWorkspaceStore((s) => s.setCurrentDiagram);
  
  if (!currentDiagram) return null;

  const style = currentDiagram.style;

  const updateStyle = async (newStyle: Partial<DiagramStyle>) => {
    const updatedStyle = { ...style, ...newStyle };
    try {
      // Optimistic update
      setCurrentDiagram({
        ...currentDiagram,
        style: updatedStyle,
      });
      
      await api.updateDiagramStyle(currentDiagram.diagram_id, updatedStyle);
    } catch (err) {
      console.error("Failed to update style", err);
    }
  };

  return (
    <div className="mb-3 flex flex-wrap items-center gap-4 rounded-lg border border-gray-100 bg-white/90 p-2.5 shadow-sm backdrop-blur-md">
      {/* Font Family */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Typography</label>
        <div className="flex gap-1">
          {["Inter", "Arial", "Roboto", "System"].map((f) => (
            <button
              key={f}
              onClick={() => updateStyle({ font_family: f })}
              className={`rounded-md px-2 py-1 text-xs font-medium transition-all ${
                style.font_family === f 
                  ? "bg-gray-900 text-white shadow-sm" 
                  : "bg-gray-50 text-gray-600 hover:bg-gray-100"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="h-8 w-px bg-gray-100" />

      {/* Font Size */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Scale</label>
        <div className="flex gap-1">
          {["small", "medium", "large"].map((s) => (
            <button
              key={s}
              onClick={() => updateStyle({ font_size: s })}
              className={`rounded-md px-2 py-1 text-xs font-medium capitalize transition-all ${
                style.font_size === s 
                  ? "bg-gray-900 text-white shadow-sm" 
                  : "bg-gray-50 text-gray-600 hover:bg-gray-100"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="h-8 w-px bg-gray-100" />

      {/* Node Color Swatches */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Node Base</label>
        <div className="flex items-center gap-2">
          {COLOR_SWATCHES.map((item) => (
            <button
              key={item.id}
              onClick={() => updateStyle({ node_background_color: item.id })}
              className={`group relative h-6 w-6 rounded-full transition-all hover:scale-110 active:scale-95 ${
                style.node_background_color === item.id ? "ring-2 ring-blue-500 ring-offset-2" : "ring-1 ring-gray-200 ring-offset-1"
              }`}
              style={{ backgroundColor: item.hex }}
            >
              <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 scale-0 rounded bg-gray-900 px-1 py-0.5 text-[8px] text-white transition-all group-hover:scale-100">
                {item.id}
              </span>
            </button>
          ))}
        </div>
      </div>

      <div className="h-8 w-px bg-gray-100" />

      {/* Visual Themes */}
      <div className="flex flex-col gap-1.5">
        <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Aesthetic Theme</label>
        <div className="flex gap-1">
          {["default", "technical", "soft", "colorful", "dark", "enterprise"].map((t) => (
            <button
              key={t}
              onClick={() => updateStyle({ node_theme: t })}
              className={`rounded-md px-2 py-1 text-[10px] font-bold uppercase tracking-tighter transition-all ${
                style.node_theme === t 
                  ? "bg-blue-600 text-white shadow-sm" 
                  : "bg-gray-50 text-gray-600 hover:bg-gray-100"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="ml-auto hidden items-center gap-2 lg:flex">
        <div className="h-1.5 w-1.5 animate-pulse rounded-full bg-green-500" />
        <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-tighter">
          Instant Live Styling
        </span>
      </div>
    </div>
  );
}
