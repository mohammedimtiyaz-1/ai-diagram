"use client";

import { create } from "zustand";
import type { EnhancementResult, DiagramResult, DiagramStyle } from "@/lib/api";
import {
  saveWorkspaceState,
  loadWorkspaceState,
  clearWorkspaceState,
  createNewConversationState,
  type PersistedWorkspaceState,
} from "@/lib/storage/workspace-storage";

type LoadingState = "idle" | "enhancing" | "generating" | "refining" | "exporting" | "analyzing";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  type: "input" | "enhancement" | "diagram" | "refinement" | "error" | "analysis";
  timestamp: number;
}

interface WorkspaceState extends PersistedWorkspaceState {
  // Transient — never persisted
  loading: LoadingState;
  error: string | null;

  // Actions
  addMessage: (msg: Omit<Message, "id" | "timestamp">) => void;
  setConversationId: (id: string | null) => void;
  setCurrentDiagram: (diagram: DiagramResult | null) => void;
  addDiagramVersion: (diagram: DiagramResult) => void;
  setLastEnhancement: (result: EnhancementResult | null) => void;
  setLoading: (state: LoadingState) => void;
  setError: (error: string | null) => void;
  setInputMode: (mode: "prompt" | "codebase") => void;
  setRawPrompt: (prompt: string) => void;
  setSelectedDiagramType: (type: string) => void;
  setSelectedNodeTheme: (theme: string) => void;
  setRepoUrl: (url: string) => void;
  setDiagramStyle: (style: DiagramStyle | null) => void;
  clearError: () => void;
  hydrateFromStorage: () => { recovered: boolean; error: string | null };
  startNewConversation: () => void;
}

let messageId = 0;

function createInitialState(): Omit<
  WorkspaceState,
  keyof Omit<WorkspaceState, keyof PersistedWorkspaceState> | "hydrateFromStorage" | "startNewConversation"
> & { loading: LoadingState; error: string | null } {
  return {
    schema_version: 1,
    conversationId: null,
    messages: [],
    currentDiagram: null,
    diagramVersions: [],
    lastEnhancement: null,
    inputMode: "prompt",
    rawPrompt: "",
    selectedDiagramType: "auto",
    selectedNodeTheme: "default",
    repoUrl: "",
    diagramStyle: null,
    updatedAt: new Date().toISOString(),
    loading: "idle",
    error: null,
  };
}

export const useWorkspaceStore = create<WorkspaceState>((set, get) => ({
  ...createInitialState(),

  addMessage: (msg) =>
    set((state) => ({
      messages: [
        ...state.messages,
        { ...msg, id: `msg-${++messageId}`, timestamp: Date.now() },
      ],
    })),

  setConversationId: (id) => set({ conversationId: id }),

  setCurrentDiagram: (diagram) =>
    set((state) => ({
      currentDiagram: diagram,
      diagramVersions: diagram ? [...state.diagramVersions, diagram] : state.diagramVersions,
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

  setRawPrompt: (rawPrompt) => set({ rawPrompt }),

  setSelectedDiagramType: (selectedDiagramType) => set({ selectedDiagramType }),

  setSelectedNodeTheme: (selectedNodeTheme) => set({ selectedNodeTheme }),

  setRepoUrl: (repoUrl) => set({ repoUrl }),

  setDiagramStyle: (diagramStyle) => set({ diagramStyle }),

  clearError: () => set({ error: null }),

  hydrateFromStorage: () => {
    const { state, recovered, error } = loadWorkspaceState();
    if (state) {
      set({
        ...state,
        loading: "idle",
        error: error,
      });
    }
    return { recovered, error };
  },

  startNewConversation: () => {
    const fresh = createNewConversationState();
    set({
      ...fresh,
      loading: "idle",
      error: null,
    });
    saveWorkspaceState(fresh);
  },
}));

// ──────────────────────────────────────────────────────────────────────────────
// Auto-persist stable state on every change
// ──────────────────────────────────────────────────────────────────────────────

useWorkspaceStore.subscribe((state) => {
  // Only persist stable fields; skip transient UI state
  const toSave: PersistedWorkspaceState = {
    schema_version: state.schema_version,
    conversationId: state.conversationId,
    messages: state.messages,
    currentDiagram: state.currentDiagram,
    diagramVersions: state.diagramVersions,
    lastEnhancement: state.lastEnhancement,
    inputMode: state.inputMode,
    rawPrompt: state.rawPrompt,
    selectedDiagramType: state.selectedDiagramType,
    selectedNodeTheme: state.selectedNodeTheme,
    repoUrl: state.repoUrl,
    diagramStyle: state.diagramStyle,
    updatedAt: new Date().toISOString(),
  };
  saveWorkspaceState(toSave);
});
