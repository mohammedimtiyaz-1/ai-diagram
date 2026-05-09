"use client";

import React, { useMemo } from "react";
import { NodeMetadata } from "@/lib/api";
import { Info, FileText, Activity } from "lucide-react";

interface NodeTooltipProps {
  label: string;
  type: string;
  metadata: NodeMetadata;
  position: { x: number; y: number };
  visible: boolean;
  isPinned: boolean;
}

const TOOLTIP_WIDTH = 256; // w-64
const TOOLTIP_HEIGHT_ESTIMATE = 280;
const MARGIN = 12;

export default function NodeTooltip({
  label,
  type,
  metadata,
  position,
  visible,
  isPinned,
}: NodeTooltipProps) {
  if (!visible) return null;

  const adjustedPosition = useMemo(() => {
    const maxWidth = typeof window !== "undefined" ? window.innerWidth : 375;
    const maxHeight = typeof window !== "undefined" ? window.innerHeight : 812;
    let left = position.x + 10;
    let top = position.y + 10;
    if (left + TOOLTIP_WIDTH + MARGIN > maxWidth) {
      left = Math.max(MARGIN, position.x - TOOLTIP_WIDTH - 10);
    }
    if (top + TOOLTIP_HEIGHT_ESTIMATE + MARGIN > maxHeight) {
      top = Math.max(MARGIN, position.y - TOOLTIP_HEIGHT_ESTIMATE - 10);
    }
    return { left, top };
  }, [position.x, position.y]);

  const importanceColors = {
    high: "bg-red-50 text-red-700 border-red-100",
    medium: "bg-blue-50 text-blue-700 border-blue-100",
    low: "bg-gray-50 text-gray-700 border-gray-100",
  };

  return (
    <div
      className={`fixed z-[200] w-56 sm:w-64 bg-white rounded-xl shadow-2xl border border-gray-100 p-3 sm:p-4 animate-in fade-in zoom-in duration-200 transition-all ${
        visible ? "opacity-100 scale-100" : "opacity-0 scale-95"
      } ${isPinned ? "pointer-events-auto" : "pointer-events-none"}`}
      style={{
        left: adjustedPosition.left,
        top: adjustedPosition.top,
      }}
    >
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-bold text-gray-900 text-sm leading-tight">
          {metadata.tooltip_title || label}
        </h4>
        <span
          className={`text-[9px] uppercase tracking-wider font-black px-1.5 py-0.5 rounded border ${
            importanceColors[metadata.importance as keyof typeof importanceColors] ||
            importanceColors.medium
          }`}
        >
          {metadata.importance}
        </span>
      </div>

      <p className="text-xs text-gray-600 mb-3 leading-relaxed italic">
        {metadata.tooltip_description || "No description available."}
      </p>

      <div className="space-y-2.5">
        {metadata.role && (
          <div className="flex items-start gap-2">
            <Info className="w-3 h-3 text-blue-500 mt-0.5 shrink-0" />
            <div>
              <span className="block text-[10px] font-bold text-gray-400 uppercase">Role</span>
              <span className="text-[11px] text-gray-700">{metadata.role}</span>
            </div>
          </div>
        )}

        {metadata.connections_summary && (
          <div className="flex items-start gap-2">
            <Activity className="w-3 h-3 text-green-500 mt-0.5 shrink-0" />
            <div>
              <span className="block text-[10px] font-bold text-gray-400 uppercase">Interaction</span>
              <span className="text-[11px] text-gray-700">{metadata.connections_summary}</span>
            </div>
          </div>
        )}

        {metadata.related_files && metadata.related_files.length > 0 && (
          <div className="flex items-start gap-2 border-t border-gray-50 pt-2">
            <FileText className="w-3 h-3 text-purple-500 mt-0.5 shrink-0" />
            <div>
              <span className="block text-[10px] font-bold text-gray-400 uppercase">Files</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {metadata.related_files.map((file, idx) => (
                  <code key={idx} className="text-[9px] bg-purple-50 text-purple-700 px-1 py-0.5 rounded">
                    {file.split('/').pop()}
                  </code>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
