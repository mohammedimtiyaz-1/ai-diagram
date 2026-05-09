"use client";

import { X } from "lucide-react";

interface LoadingOverlayProps {
  message: string;
  subtext?: string;
  onCancel?: () => void;
  visible: boolean;
}

export default function LoadingOverlay({ message, subtext, onCancel, visible }: LoadingOverlayProps) {
  if (!visible) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-white/80 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="flex flex-col items-center gap-4 sm:gap-6 rounded-2xl bg-white p-6 sm:p-10 lg:p-12 shadow-2xl ring-1 ring-gray-100 max-w-[90vw] sm:max-w-sm w-full text-center">
        <div className="relative">
          <div className="h-12 w-12 sm:h-16 sm:w-16 animate-spin rounded-full border-4 border-gray-100 border-t-black" />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-1.5 w-1.5 sm:h-2 sm:w-2 rounded-full bg-black animate-pulse" />
          </div>
        </div>

        <div className="space-y-1.5 sm:space-y-2">
          <h3 className="text-base sm:text-lg font-bold text-gray-900">{message}</h3>
          <p className="text-xs sm:text-sm text-gray-500 italic">
            {subtext || "This usually takes a few seconds..."}
          </p>
        </div>

        {onCancel && (
          <button
            onClick={onCancel}
            className="flex items-center gap-2 rounded-full border border-gray-200 bg-white px-6 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-50 hover:border-gray-300 active:scale-95"
          >
            <X className="w-4 h-4" />
            Cancel Request
          </button>
        )}
      </div>
    </div>
  );
}
