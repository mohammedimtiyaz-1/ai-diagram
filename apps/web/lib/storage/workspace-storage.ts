import type { DiagramResult, EnhancementResult, DiagramStyle } from "@/lib/api";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  type: "input" | "enhancement" | "diagram" | "refinement" | "error" | "analysis";
  timestamp: number;
}

export interface PersistedWorkspaceState {
  schema_version: number;
  conversationId: string | null;
  messages: Message[];
  currentDiagram: DiagramResult | null;
  diagramVersions: DiagramResult[];
  lastEnhancement: EnhancementResult | null;
  inputMode: "prompt" | "codebase";
  rawPrompt: string;
  selectedDiagramType: string;
  selectedNodeTheme: string;
  repoUrl: string;
  diagramStyle: DiagramStyle | null;
  updatedAt: string;
}

const STORAGE_KEY = "ai-design-system-diagram-assistant:workspace:v1";
const SCHEMA_VERSION = 1;

export interface LoadResult {
  state: PersistedWorkspaceState | null;
  recovered: boolean;
  error: string | null;
}

function getDefaultState(): PersistedWorkspaceState {
  return {
    schema_version: SCHEMA_VERSION,
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
  };
}

export function saveWorkspaceState(state: PersistedWorkspaceState): void {
  if (typeof window === "undefined") return;
  try {
    const toSave = {
      ...state,
      schema_version: SCHEMA_VERSION,
      updatedAt: new Date().toISOString(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
  } catch {
    // localStorage quota exceeded or unavailable — silently fail
  }
}

export function loadWorkspaceState(): LoadResult {
  if (typeof window === "undefined") {
    return { state: null, recovered: false, error: null };
  }

  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return { state: null, recovered: false, error: null };
  }

  try {
    const parsed = JSON.parse(raw) as Partial<PersistedWorkspaceState>;

    if (typeof parsed.schema_version !== "number" || parsed.schema_version !== SCHEMA_VERSION) {
      clearWorkspaceState();
      return {
        state: null,
        recovered: false,
        error: "Workspace data was from an older version and has been reset.",
      };
    }

    const validated: PersistedWorkspaceState = {
      schema_version: SCHEMA_VERSION,
      conversationId: typeof parsed.conversationId === "string" ? parsed.conversationId : null,
      messages: Array.isArray(parsed.messages) ? parsed.messages : [],
      currentDiagram: parsed.currentDiagram ?? null,
      diagramVersions: Array.isArray(parsed.diagramVersions) ? parsed.diagramVersions : [],
      lastEnhancement: parsed.lastEnhancement ?? null,
      inputMode: parsed.inputMode === "codebase" ? "codebase" : "prompt",
      rawPrompt: typeof parsed.rawPrompt === "string" ? parsed.rawPrompt : "",
      selectedDiagramType: typeof parsed.selectedDiagramType === "string" ? parsed.selectedDiagramType : "auto",
      selectedNodeTheme: typeof parsed.selectedNodeTheme === "string" ? parsed.selectedNodeTheme : "default",
      repoUrl: typeof parsed.repoUrl === "string" ? parsed.repoUrl : "",
      diagramStyle: parsed.diagramStyle ?? null,
      updatedAt: typeof parsed.updatedAt === "string" ? parsed.updatedAt : new Date().toISOString(),
    };

    return { state: validated, recovered: false, error: null };
  } catch {
    clearWorkspaceState();
    return {
      state: null,
      recovered: false,
      error: "Workspace data was corrupted and has been reset.",
    };
  }
}

export function clearWorkspaceState(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_KEY);
}

export function createNewConversationState(): PersistedWorkspaceState {
  return {
    ...getDefaultState(),
    conversationId: `conv-${Date.now()}`,
  };
}
