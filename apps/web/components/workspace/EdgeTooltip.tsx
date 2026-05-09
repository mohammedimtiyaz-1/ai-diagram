"use client";

import React, { useMemo } from "react";
import { EdgeMetadata } from "@/lib/api";
import { Share2, Zap, ArrowRightLeft } from "lucide-react";

interface EdgeTooltipProps {
  source: string;
  target: string;
  label?: string;
  metadata: EdgeMetadata;
  position: { x: number; y: number };
  visible: boolean;
  isPinned: boolean;
}

const TOOLTIP_WIDTH = 240; // w-60
const TOOLTIP_HEIGHT_ESTIMATE = 240;
const MARGIN = 12;

export default function EdgeTooltip({
  source,
  target,
  label,
  metadata,
  position,
  visible,
  isPinned,
}: EdgeTooltipProps) {
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

  const typeColors = {
    dependency: "text-blue-600 bg-blue-50 border-blue-100",
    "data-flow": "text-green-600 bg-green-50 border-blue-100",
    sequence: "text-purple-600 bg-purple-50 border-blue-100",
    ownership: "text-orange-600 bg-orange-50 border-blue-100",
    composition: "text-red-600 bg-red-50 border-blue-100",
    integration: "text-cyan-600 bg-cyan-50 border-blue-100",
    generic: "text-gray-600 bg-gray-50 border-blue-100",
  };

  return (
    <div
      className={`fixed z-[200] w-52 sm:w-60 bg-white rounded-xl shadow-2xl border border-gray-100 p-3 sm:p-4 animate-in fade-in zoom-in duration-200 transition-all ${
        visible ? "opacity-100 scale-100" : "opacity-0 scale-95"
      } ${isPinned ? "pointer-events-auto" : "pointer-events-none"}`}
      style={{
        left: adjustedPosition.left,
        top: adjustedPosition.top,
      }}
    >
      <div className="flex items-center gap-2 mb-2 pb-2 border-b border-gray-50">
        <Share2 className="w-3.5 h-3.5 text-gray-400" />
        <h4 className="font-bold text-gray-900 text-xs truncate">
          {metadata.tooltip_title || label || "Relationship"}
        </h4>
      </div>

      <div className="flex items-center gap-2 mb-3 px-2 py-1 bg-gray-50 rounded-lg border border-gray-100">
        <span className="text-[10px] font-bold text-gray-500 truncate max-w-[80px]">{source}</span>
        <ArrowRightLeft className="w-2.5 h-2.5 text-gray-300 shrink-0" />
        <span className="text-[10px] font-bold text-gray-500 truncate max-w-[80px]">{target}</span>
      </div>

      <p className="text-[11px] text-gray-600 mb-3 leading-relaxed italic">
        {metadata.tooltip_description || "Defines the connection between these two components."}
      </p>

      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <Zap className="w-3 h-3 text-yellow-500 shrink-0" />
          <span className={`text-[9px] uppercase tracking-wider font-black px-1.5 py-0.5 rounded border ${
            typeColors[metadata.relationship_type as keyof typeof typeColors] || typeColors.generic
          }`}>
            {metadata.relationship_type}
          </span>
        </div>

        {metadata.source_to_target_summary && (
          <div className="pt-1">
            <span className="block text-[9px] font-bold text-gray-400 uppercase mb-0.5 tracking-tight">Flow Summary</span>
            <p className="text-[10px] text-gray-700 leading-snug">
              {metadata.source_to_target_summary}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
