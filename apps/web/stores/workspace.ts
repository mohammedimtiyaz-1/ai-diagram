"use client";

import { create } from "zustand";
import type { EnhancementResult, DiagramResult } from "@/lib/api";

type LoadingState = "idle" | "enhancing" | "generating" | "refining" | "exporting" | "analyzing";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  type: "input" | "enhancement" | "diagram" | "refinement" | "error" | "analysis";
  timestamp: number;
}

interface WorkspaceState {
  // Messages
  messages: Message[];
  conversationId: string | null;

  // Current diagram
  currentDiagram: DiagramResult | null;
  diagramVersions: DiagramResult[];

  // Enhanced prompt (last enhancement result)
  lastEnhancement: EnhancementResult | null;

  // Loading & error
  loading: LoadingState;
  error: string | null;

  // Input mode
  inputMode: "prompt" | "codebase";

  // Actions
  addMessage: (msg: Omit<Message, "id" | "timestamp">) => void;
  setConversationId: (id: string) => void;
  setCurrentDiagram: (diagram: DiagramResult) => void;
  addDiagramVersion: (diagram: DiagramResult) => void;
  setLastEnhancement: (result: EnhancementResult | null) => void;
  setLoading: (state: LoadingState) => void;
  setError: (error: string | null) => void;
  setInputMode: (mode: "prompt" | "codebase") => void;
  clearError: () => void;
  reset: () => void;
}

let messageId = 0;

export const useWorkspaceStore = create<WorkspaceState>((set, get) => ({
  messages: [],
  conversationId: null,
  currentDiagram: null,
  diagramVersions: [],
  lastEnhancement: null,
  loading: "idle",
  error: null,
  inputMode: "prompt",

  addMessage: (msg) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...msg,
          id: `msg-${++messageId}`,
          timestamp: Date.now(),
        },
      ],
    })),

  setConversationId: (id) => set({ conversationId: id }),

  setCurrentDiagram: (diagram) =>
    set((state) => ({
      currentDiagram: diagram,
      diagramVersions: [...state.diagramVersions, diagram],
    })),

  addDiagramVersion: (diagram) =>
    set((state) => ({
      currentDiagram: diagram,
      diagramVersions: [...state.diagramVersions, diagram],
    })),

  setLastEnhancement: (result) => set({ lastEnhancement: result }),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error, loading: "idle" }),

  setInputMode: (inputMode) => set({ inputMode }),

  clearError: () => set({ error: null }),

  reset: () =>
    set({
      messages: [],
      conversationId: null,
      currentDiagram: null,
      diagramVersions: [],
      lastEnhancement: null,
      loading: "idle",
      error: null,
    }),
}));
