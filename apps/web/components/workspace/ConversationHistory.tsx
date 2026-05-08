"use client";

import { useWorkspaceStore } from "@/stores/workspace";

export default function ConversationHistory() {
  const messages = useWorkspaceStore((s) => s.messages);

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-center text-sm text-gray-400">
        <p>No messages yet.</p>
        <p className="mt-1">Enter a prompt above to start.</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 overflow-y-auto">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[85%] rounded-lg px-4 py-2.5 text-sm ${
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
    </div>
  );
}
