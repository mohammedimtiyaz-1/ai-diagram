"use client";

import { useCallback } from "react";
import Link from "next/link";
import PromptInput from "@/components/workspace/PromptInput";
import ConversationHistory from "@/components/workspace/ConversationHistory";
import DiagramPreview from "@/components/workspace/DiagramPreview";
import FollowUpInput from "@/components/workspace/FollowUpInput";
import { useWorkspaceStore } from "@/stores/workspace";
import { api } from "@/lib/api";

export default function WorkspacePage() {
  const store = useWorkspaceStore();
  const loading = store.loading;
  const error = store.error;
  const conversationId = store.conversationId;
  const currentDiagram = store.currentDiagram;

  const isBusy = loading !== "idle";

  const handleGenerate = useCallback(
    async (prompt: string, diagramType: string) => {
      store.setLoading("enhancing");
      store.setError(null);
      store.addMessage({ role: "user", content: prompt, type: "input" });

      try {
        // Step 1: Enhance prompt
        const enhancement = await api.enhancePrompt(prompt, diagramType);
        store.setLastEnhancement(enhancement);
        store.setLoading("generating");

        // Show enhancement in conversation
        store.addMessage({
          role: "assistant",
          content: enhancement.enhanced_prompt,
          type: "enhancement",
        });

        // Step 2: Generate diagram
        const diagram = await api.generateDiagram(
          prompt,
          enhancement.enhanced_prompt,
          enhancement.detected_diagram_type,
          "mermaid",
          undefined,
        );

        store.setConversationId(diagram.conversation_id);
        store.setCurrentDiagram(diagram);
        store.setLoading("idle");

        store.addMessage({
          role: "assistant",
          content: `Generated "${diagram.title}" — ${diagram.explanation}`,
          type: "diagram",
        });
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Something went wrong";
        store.setError(msg);
        store.addMessage({ role: "assistant", content: msg, type: "error" });
        store.setLoading("idle");
      }
    },
    [store],
  );

  const handleRefine = useCallback(
    async (followup: string) => {
      if (!conversationId || !currentDiagram) return;
      store.setLoading("refining");
      store.setError(null);
      store.addMessage({ role: "user", content: followup, type: "refinement" });

      try {
        const diagram = await api.refineDiagram(
          conversationId,
          currentDiagram.diagram_id,
          followup,
          currentDiagram.diagram_source,
          currentDiagram.nodes,
          "mermaid",
        );

        store.addDiagramVersion(diagram);
        store.addMessage({
          role: "assistant",
          content: `Refined diagram — ${diagram.changes_summary.join(", ") || "Updated"}`,
          type: "diagram",
        });
        store.setLoading("idle");
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Refinement failed";
        store.setError(msg);
        store.addMessage({ role: "assistant", content: msg, type: "error" });
        store.setLoading("idle");
      }
    },
    [store, conversationId, currentDiagram],
  );

  return (
    <main className="flex h-screen flex-col bg-white">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-200 px-6 py-3">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="text-sm font-semibold text-gray-900 hover:underline"
          >
            AI Design System Diagram Assistant
          </Link>
        </div>
        {isBusy && (
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-black" />
            {loading === "enhancing" && "Enhancing prompt..."}
            {loading === "generating" && "Generating diagram..."}
            {loading === "refining" && "Refining diagram..."}
          </div>
        )}
      </header>

      {/* Main workspace */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Chat Panel */}
        <section className="flex w-2/5 min-w-[360px] flex-col border-r border-gray-200 bg-gray-50/50">
          {/* Conversation history */}
          <div className="flex-1 overflow-y-auto px-4 py-4">
            <ConversationHistory />
          </div>

          {/* Error banner */}
          {error && (
            <div className="mx-4 mb-2 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Input area */}
          <div className="border-t border-gray-200 bg-white p-4">
            {currentDiagram ? (
              <FollowUpInput onSubmit={handleRefine} disabled={isBusy} />
            ) : (
              <PromptInput onSubmit={handleGenerate} disabled={isBusy} />
            )}
          </div>
        </section>

        {/* Right: Diagram Panel */}
        <section className="flex flex-1 flex-col bg-white p-4">
          <DiagramPreview />
        </section>
      </div>
    </main>
  );
}
