"use client";

import { useWorkspaceStore } from "@/stores/workspace";

export default function ConversationHistory() {
  const messages = useWorkspaceStore((s) => s.messages);
  const loading = useWorkspaceStore((s) => s.loading);

  const isBusy = loading !== "idle";

  const loaderText =
    loading === "enhancing"
      ? "Enhancing prompt..."
      : loading === "refining"
        ? "Refining diagram..."
        : loading === "analyzing"
          ? "Analyzing codebase..."
          : loading === "generating"
            ? "Generating diagram..."
            : "";

  if (messages.length === 0 && !isBusy) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-center text-sm text-gray-400">
        <p>No messages yet.</p>
        <p className="mt-1">Enter a prompt above to start.</p>
      </div>
    );
  }

  return (
    <div className="relative flex flex-col gap-3 overflow-y-auto min-h-full">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[90%] sm:max-w-[85%] rounded-lg px-3 py-2 sm:px-4 sm:py-2.5 text-sm ${
              msg.role === "user"
                ? "bg-black text-white"
                : msg.type === "error"
                  ? "border border-red-200 bg-red-50 text-red-800"
                  : "border border-gray-200 bg-gray-50 text-gray-800"
            }`}
          >
            {msg.type === "enhancement" && msg.role === "assistant" && (
              <div className="mb-1 text-xs font-medium text-gray-500">Enhanced Prompt</div>
            )}
            {msg.type === "diagram" && msg.role === "assistant" && (
              <div className="mb-1 text-xs font-medium text-gray-500">Diagram Generated</div>
            )}
            <div className="whitespace-pre-wrap">{msg.content}</div>
          </div>
        </div>
      ))}

      {/* Chat Loading Overlay */}
      {isBusy && (
        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-white/60 backdrop-blur-[2px] animate-in fade-in duration-300">
          <div className="flex flex-col items-center gap-3 rounded-2xl bg-white p-6 shadow-xl ring-1 ring-gray-100 max-w-[80%] text-center">
            <div className="relative">
              <div className="h-10 w-10 animate-spin rounded-full border-3 border-gray-100 border-t-black" />
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="h-1 w-1 rounded-full bg-black animate-pulse" />
              </div>
            </div>
            <div className="space-y-1">
              <p className="text-sm font-bold text-gray-900">{loaderText}</p>
              <p className="text-[10px] text-gray-500 italic">We're processing your request...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
