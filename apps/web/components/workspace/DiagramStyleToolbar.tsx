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
    <div className="mb-4 flex flex-wrap items-center gap-3 sm:gap-6 rounded-xl border border-gray-100 bg-white/90 p-2.5 sm:p-3 shadow-lg backdrop-blur-md max-w-full">
      {/* Typography */}
      <div className="flex flex-col gap-1">
        <label className="text-[9px] font-black uppercase tracking-widest text-gray-400 px-1">Typography</label>
        <select
          value={style.font_family}
          onChange={(e) => updateStyle({ font_family: e.target.value })}
          className="appearance-none bg-gray-50 border border-gray-100 rounded-lg px-3 py-1.5 text-[11px] font-bold text-gray-700 cursor-pointer hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-black/5"
        >
          {["Inter", "Arial", "Roboto", "System"].map((f) => (
            <option key={f} value={f}>{f}</option>
          ))}
        </select>
      </div>

      {/* Scale */}
      <div className="flex flex-col gap-1">
        <label className="text-[9px] font-black uppercase tracking-widest text-gray-400 px-1">Scale</label>
        <select
          value={style.font_size}
          onChange={(e) => updateStyle({ font_size: e.target.value })}
          className="appearance-none bg-gray-50 border border-gray-100 rounded-lg px-3 py-1.5 text-[11px] font-bold text-gray-700 cursor-pointer hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-black/5"
        >
          {["small", "medium", "large"].map((s) => (
            <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
          ))}
        </select>
      </div>

      {/* Node Color */}
      <div className="flex flex-col gap-1">
        <label className="text-[9px] font-black uppercase tracking-widest text-gray-400 px-1">Node Base</label>
        <select
          value={style.node_background_color}
          onChange={(e) => updateStyle({ node_background_color: e.target.value })}
          className="appearance-none bg-gray-50 border border-gray-100 rounded-lg px-3 py-1.5 text-[11px] font-bold text-gray-700 cursor-pointer hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-black/5"
        >
          {COLOR_SWATCHES.map((item) => (
            <option key={item.id} value={item.id}>{item.id.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}</option>
          ))}
        </select>
      </div>

      {/* Visual Themes */}
      <div className="flex flex-col gap-1">
        <label className="text-[9px] font-black uppercase tracking-widest text-gray-400 px-1">Aesthetic Theme</label>
        <select
          value={style.node_theme}
          onChange={(e) => updateStyle({ node_theme: e.target.value })}
          className="appearance-none bg-blue-50 border border-blue-100 rounded-lg px-3 py-1.5 text-[11px] font-black text-blue-700 cursor-pointer hover:bg-blue-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/10"
        >
          {["default", "technical", "soft", "colorful", "dark", "enterprise"].map((t) => (
            <option key={t} value={t}>{t.toUpperCase()}</option>
          ))}
        </select>
      </div>

      <div className="ml-auto hidden items-center gap-2 lg:flex pr-2">
        <div className="h-1.5 w-1.5 animate-pulse rounded-full bg-green-500" />
        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-tighter">
          Instant Live Styling
        </span>
      </div>
    </div>
  );
}
