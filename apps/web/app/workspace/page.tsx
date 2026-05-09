"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Menu, X, MessageSquarePlus } from "lucide-react";
import PromptInput from "@/components/workspace/PromptInput";
import CodebaseInput from "@/components/workspace/CodebaseInput";
import ConversationHistory from "@/components/workspace/ConversationHistory";
import DiagramPreview from "@/components/workspace/DiagramPreview";
import FollowUpInput from "@/components/workspace/FollowUpInput";
import LoadingOverlay from "@/components/workspace/LoadingOverlay";
import { useWorkspaceStore } from "@/stores/workspace";
import { api } from "@/lib/api";

export default function WorkspacePage() {
  const store = useWorkspaceStore();
  const loading = store.loading;
  const error = store.error;
  const conversationId = store.conversationId;
  const currentDiagram = store.currentDiagram;
  const inputMode = store.inputMode;

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [hydrationError, setHydrationError] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);

  // Hydrate from localStorage on first mount
  useEffect(() => {
    const result = store.hydrateFromStorage();
    if (result.error) {
      setHydrationError(result.error);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const isBusy = loading !== "idle";

  const handleCancel = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    store.setLoading("idle");
  }, [store]);

  const handleGenerate = useCallback(
    async (prompt: string, diagramType: string) => {
      store.setLoading("enhancing");
      store.setError(null);
      store.addMessage({ role: "user", content: prompt, type: "input" });

      const controller = new AbortController();
      abortControllerRef.current = controller;

      const timeoutId = setTimeout(() => {
        controller.abort();
      }, 10000);

      try {
        // Step 1: Enhance prompt
        const enhancement = await api.enhancePrompt(prompt, diagramType, "text", controller.signal);
        clearTimeout(timeoutId);
        abortControllerRef.current = null;

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
      } catch (err: any) {
        clearTimeout(timeoutId);
        abortControllerRef.current = null;

        if (err.name === "AbortError" || (err instanceof Error && err.message.includes("timed out"))) {
          const timeoutMsg = "This is taking longer than expected. Please try again with a shorter prompt.";
          store.setError(timeoutMsg);
          store.addMessage({ role: "assistant", content: timeoutMsg, type: "error" });
        } else {
          const msg = err instanceof Error ? err.message : "Something went wrong";
          store.setError(msg);
          store.addMessage({ role: "assistant", content: msg, type: "error" });
        }
        store.setLoading("idle");
      }
    },
    [store],
  );

  const handleCodebaseSubmit = useCallback(
    async (repoUrl: string, diagramType: string, nodeTheme: string) => {
      store.setLoading("analyzing");
      store.setError(null);
      store.addMessage({ role: "user", content: `Analyze repository: ${repoUrl}`, type: "input" });

      try {
        // Step 1: Analyze codebase
        const analysis = await api.analyzeCodebase(repoUrl, diagramType);
        store.addMessage({
          role: "assistant",
          content: analysis.architecture_summary,
          type: "analysis",
        });
        
        store.setLoading("generating");

        // Step 2: Generate diagram
        const diagram = await api.generateCodebaseDiagram(
          repoUrl,
          diagramType,
          nodeTheme,
          undefined,
        );

        store.setConversationId(diagram.conversation_id);
        store.setCurrentDiagram(diagram);
        store.setLoading("idle");

        store.addMessage({
          role: "assistant",
          content: `Generated "${diagram.title}" based on codebase analysis. ${diagram.explanation}`,
          type: "diagram",
        });
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Codebase analysis failed";
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

      const controller = new AbortController();
      abortControllerRef.current = controller;

      const timeoutId = setTimeout(() => {
        controller.abort();
      }, 10000);

      try {
        const diagram = await api.refineDiagram(
          conversationId,
          currentDiagram.diagram_id,
          followup,
          currentDiagram.diagram_source,
          currentDiagram.nodes,
          currentDiagram.edges,
          "mermaid",
          controller.signal,
        );

        clearTimeout(timeoutId);
        abortControllerRef.current = null;

        store.addDiagramVersion(diagram);
        store.addMessage({
          role: "assistant",
          content: `Refined diagram — ${diagram.changes_summary.join(", ") || "Updated"}`,
          type: "diagram",
        });
        store.setLoading("idle");
      } catch (err: any) {
        clearTimeout(timeoutId);
        abortControllerRef.current = null;

        if (err.name === "AbortError" || (err instanceof Error && err.message.includes("timed out"))) {
          const timeoutMsg = "This is taking longer than expected. Please try again with a shorter prompt.";
          store.setError(timeoutMsg);
          store.addMessage({ role: "assistant", content: timeoutMsg, type: "error" });
        } else {
          const msg = err instanceof Error ? err.message : "Refinement failed";
          store.setError(msg);
          store.addMessage({ role: "assistant", content: msg, type: "error" });
        }
        store.setLoading("idle");
      }
    },
    [store, conversationId, currentDiagram],
  );

  return (
    <main className="flex h-[100dvh] flex-col bg-white">
      <LoadingOverlay
        visible={isBusy && (loading === "enhancing" || loading === "refining" || loading === "generating")}
        message={
          loading === "enhancing"
            ? "Improving your prompt..."
            : loading === "refining"
            ? "Updating your diagram safely..."
            : "Generating your diagram..."
        }
        onCancel={handleCancel}
      />
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-200 px-3 py-2.5 lg:px-6 lg:py-3 shrink-0">
        <div className="flex items-center gap-2 lg:gap-3">
          {/* Mobile hamburger to open sidebar */}
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden rounded-lg p-1.5 text-gray-600 hover:bg-gray-100 transition"
            aria-label="Open chat sidebar"
          >
            <Menu className="w-5 h-5" />
          </button>
          <Link
            href="/"
            className="text-xs font-semibold text-gray-900 hover:underline sm:text-sm truncate"
          >
            AI Design System Diagram Assistant
          </Link>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              if (store.messages.length > 0 || store.currentDiagram) {
                const confirmed = window.confirm(
                  "Start a new conversation? Your current workspace will be saved in history."
                );
                if (!confirmed) return;
              }
              store.startNewConversation();
            }}
            className="flex items-center gap-1.5 rounded-lg border border-gray-200 px-2.5 py-1.5 text-[11px] sm:text-xs font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition"
            title="New Conversation"
          >
            <MessageSquarePlus className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">New</span>
          </button>
          {isBusy && (
            <div className="flex items-center gap-2 text-xs sm:text-sm text-gray-500">
              <div className="h-3.5 w-3.5 sm:h-4 sm:w-4 animate-spin rounded-full border-2 border-gray-300 border-t-black" />
              <span className="hidden sm:inline">
                {loading === "enhancing" && "Enhancing prompt..."}
                {loading === "generating" && "Generating diagram..."}
                {loading === "refining" && "Refining diagram..."}
              </span>
            </div>
          )}
        </div>
      </header>

      {/* Main workspace */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Mobile sidebar overlay backdrop */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/40 z-40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Left: Chat Panel */}
        <section
          className={`flex flex-col border-r border-gray-200 bg-gray-50/50
            lg:w-2/5 lg:min-w-0 lg:max-w-md lg:static lg:translate-x-0
            fixed inset-y-0 left-0 z-50 w-80 transition-transform duration-300 ease-in-out
            ${sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
          `}
        >
          {/* Mobile sidebar header with close button */}
          <div className="lg:hidden flex items-center justify-between border-b border-gray-200 px-3 py-2 bg-white">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Chat</span>
            <button
              onClick={() => setSidebarOpen(false)}
              className="rounded-lg p-1.5 text-gray-500 hover:bg-gray-100 transition"
              aria-label="Close sidebar"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Conversation history */}
          <div className="flex-1 overflow-y-auto px-3 py-3 lg:px-4 lg:py-4">
            <ConversationHistory />
          </div>

          {/* Recovery / hydration error banner */}
          {hydrationError && (
            <div className="mx-3 lg:mx-4 mb-2 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-800">
              <strong>Notice:</strong> {hydrationError}
              <button
                onClick={() => setHydrationError(null)}
                className="ml-2 underline hover:text-amber-900"
              >
                Dismiss
              </button>
            </div>
          )}

          {/* Error banner */}
          {error && (
            <div className="mx-3 lg:mx-4 mb-2 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Input area */}
          <div className="border-t border-gray-200 bg-white p-3 lg:p-4">
            {currentDiagram ? (
              <FollowUpInput onSubmit={handleRefine} disabled={isBusy} />
            ) : (
              <>
                <div className="mb-3 lg:mb-4 flex rounded-lg bg-gray-100 p-1">
                  <button
                    onClick={() => store.setInputMode("prompt")}
                    className={`flex-1 rounded-md py-1.5 text-[10px] sm:text-xs font-medium transition ${
                      inputMode === "prompt"
                        ? "bg-white text-black shadow-sm"
                        : "text-gray-500 hover:text-gray-700"
                    }`}
                  >
                    Design Prompt
                  </button>
                  <button
                    onClick={() => store.setInputMode("codebase")}
                    className={`flex-1 rounded-md py-1.5 text-[10px] sm:text-xs font-medium transition ${
                      inputMode === "codebase"
                        ? "bg-white text-black shadow-sm"
                        : "text-gray-500 hover:text-gray-700"
                    }`}
                  >
                    GitHub URL
                  </button>
                </div>

                {inputMode === "prompt" ? (
                  <PromptInput onSubmit={handleGenerate} disabled={isBusy} />
                ) : (
                  <CodebaseInput onSubmit={handleCodebaseSubmit} disabled={isBusy} />
                )}
              </>
            )}
          </div>
        </section>

        {/* Right: Diagram Panel */}
        <section className="flex flex-1 flex-col bg-white p-2 sm:p-3 lg:p-4 min-w-0">
          <DiagramPreview />
        </section>
      </div>
    </main>
  );
}
