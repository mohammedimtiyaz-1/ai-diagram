"use client";

import React from "react";
import { DiagramEdge } from "@/lib/api";
import { Share2, ArrowRight } from "lucide-react";

interface EdgeRelationshipPanelProps {
  edges: DiagramEdge[];
  onEdgeClick: (edge: DiagramEdge) => void;
}

export default function EdgeRelationshipPanel({
  edges,
  onEdgeClick,
}: EdgeRelationshipPanelProps) {
  if (!edges || edges.length === 0) return null;

  return (
    <div className="mt-4 border-t border-gray-100 pt-4">
      <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3 px-1">
        Diagram Relationships
      </h4>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
        {edges.map((edge) => (
          <button
            key={edge.id}
            onClick={() => onEdgeClick(edge)}
            className="flex items-center justify-between p-2 rounded-lg border border-gray-100 bg-white hover:border-blue-200 hover:bg-blue-50 transition-all text-left group shadow-sm"
          >
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-1.5 mb-0.5">
                <Share2 className="w-3 h-3 text-gray-400 group-hover:text-blue-500" />
                <span className="text-[11px] font-bold text-gray-800 truncate">
                  {edge.metadata.tooltip_title || edge.label || "Relationship"}
                </span>
              </div>
              <div className="flex items-center gap-1 text-[9px] text-gray-500 font-medium">
                <span className="truncate max-w-[60px]">{edge.source}</span>
                <ArrowRight className="w-2 h-2 text-gray-300" />
                <span className="truncate max-w-[60px]">{edge.target}</span>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
