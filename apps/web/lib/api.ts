const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  (process.env.NODE_ENV === "development" ? "http://localhost:8000" : "");

// ── Timeouts per API (seconds) ──
export const TIMEOUTS = {
  enhance: 30_000,
  refine: 45_000,
  analyze: 60_000,
  generate: 30_000,
  export: 15_000,
  listVersions: 10_000,
  updateStyle: 10_000,
} as const;

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public code?: string,
    public retryAllowed = false,
  ) {
    super(message);
  }
}

export class TimeoutError extends ApiError {
  constructor(message = "This is taking longer than expected. Please try again with a shorter input.") {
    super(504, message, "REQUEST_TIMEOUT", true);
  }
}

export class RateLimitError extends ApiError {
  constructor(message = "You're sending requests too quickly. Please wait a moment and try again.") {
    super(429, message, "RATE_LIMIT_EXCEEDED", true);
  }
}

export class CancelledError extends ApiError {
  constructor(message = "Request cancelled. Your current work was not changed.") {
    super(0, message, "REQUEST_CANCELLED", true);
  }
}

function classifyError(status: number, body: any, originalError?: Error): ApiError {
  if (originalError?.name === "AbortError") {
    return new CancelledError();
  }
  if (status === 429) {
    return new RateLimitError(body?.message || "Rate limit exceeded");
  }
  if (status === 504) {
    return new TimeoutError(body?.message || body?.suggestion);
  }
  return new ApiError(
    status,
    body?.message || body?.detail || "Something went wrong while processing. Your previous work is safe.",
    body?.code,
    body?.retry_allowed ?? false,
  );
}

interface FetchOptions {
  method?: string;
  body?: unknown;
  timeoutMs?: number;
  signal?: AbortSignal;
}

async function fetchWithTimeout<T>(path: string, opts: FetchOptions = {}): Promise<T> {
  const { method = "GET", body, timeoutMs = 10_000, signal } = opts;

  if (!API_BASE) {
    throw new ApiError(
      0,
      "Production API URL is not configured. Set NEXT_PUBLIC_API_BASE_URL to your Render backend URL and redeploy.",
      "MISSING_API_BASE_URL",
      false,
    );
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  // Merge external signal (e.g. user cancel) with timeout controller
  if (signal) {
    signal.addEventListener("abort", () => controller.abort());
  }

  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      throw classifyError(res.status, errBody);
    }
    return res.json();
  } catch (err) {
    clearTimeout(timeoutId);
    if (err instanceof ApiError) throw err;
    if (err instanceof Error && err.name === "AbortError") {
      throw new CancelledError();
    }
    throw new ApiError(0, "Network issue detected. Please check your connection and try again.", "NETWORK_ERROR", true);
  }
}

async function post<T>(path: string, body: unknown, timeoutMs = 10_000, signal?: AbortSignal): Promise<T> {
  return fetchWithTimeout<T>(path, { method: "POST", body, timeoutMs, signal });
}

async function get<T>(path: string, timeoutMs = 10_000): Promise<T> {
  return fetchWithTimeout<T>(path, { method: "GET", timeoutMs });
}

async function patch<T>(path: string, body: unknown, timeoutMs = 10_000): Promise<T> {
  return fetchWithTimeout<T>(path, { method: "PATCH", body, timeoutMs });
}

export interface NodeMetadata {
  tooltip_title: string;
  tooltip_description: string;
  role: string;
  importance: string;
  connections_summary: string;
  related_files?: string[];
}

export interface DiagramNode {
  id: string;
  label: string;
  type: string;
  metadata: NodeMetadata;
  style: {
    background_color: string | null;
    font_color: string | null;
  };
}

export interface EdgeMetadata {
  tooltip_title: string;
  tooltip_description: string;
  relationship_type: string;
  source_to_target_summary: string;
  importance: string;
  related_files?: string[];
}

export interface DiagramEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  description?: string;
  metadata: EdgeMetadata;
}

export interface DiagramStyle {
  font_family: string;
  font_size: string;
  font_color: string;
  node_background_color: string;
  diagram_background_color: string;
  node_theme?: string;
}

export interface EnhancementResult {
  enhanced_prompt: string;
  diagram_goal: string;
  detected_diagram_type: string;
  entities: string[];
  relationships: { from: string; to: string; type: string }[];
  structure_hints: string;
  assumptions: string[];
  recommended_provider: string;
}

export interface DiagramResult {
  diagram_id: string;
  conversation_id: string;
  version: number;
  title: string;
  diagram_type: string;
  provider: string;
  diagram_source: string;
  diagram_format: string;
  explanation: string;
  nodes: DiagramNode[];
  edges: DiagramEdge[];
  style: DiagramStyle;
  change_intent: string;
  is_full_regeneration: boolean;
  base_diagram_id: string | null;
  parent_diagram_id: string | null;
  changes_summary: string[];
  metadata: {
    node_count: number;
    edge_count: number;
    generated_at?: string;
  };
}

export interface ExportResult {
  format: string;
  content: string;
  filename_suggestion: string;
}

export interface VersionListItem {
  diagram_id: string;
  version: number;
  title: string;
  diagram_type: string;
  changes_summary: string[];
  created_at: string;
}

export interface VersionListResponse {
  conversation_id: string;
  versions: VersionListItem[];
}

export interface CodebaseAnalysisResponse {
  analysis_id: string;
  repo_name: string;
  detected_stack: string[];
  important_files: string[];
  project_summary: string;
  architecture_summary: string;
  recommended_diagram_type: string;
  enhanced_prompt: string;
  warnings: string[];
}

export const api = {
  enhancePrompt: (raw_prompt: string, diagram_type: string = "auto", source: string = "text", signal?: AbortSignal) =>
    post<EnhancementResult>("/api/prompts/enhance", { raw_prompt, diagram_type, source }, TIMEOUTS.enhance, signal),

  generateDiagram: (
    raw_prompt: string,
    enhanced_prompt: string,
    diagram_type: string,
    provider: string = "mermaid",
    conversation_id?: string,
  ) =>
    post<DiagramResult>("/api/diagrams/generate", {
      raw_prompt,
      enhanced_prompt,
      diagram_type,
      provider,
      conversation_id,
    }, TIMEOUTS.generate),

  refineDiagram: (
    conversation_id: string,
    diagram_id: string,
    followup_prompt: string,
    current_diagram_source: string,
    nodes: DiagramNode[],
    edges: DiagramEdge[],
    provider: string = "mermaid",
    signal?: AbortSignal,
  ) =>
    post<DiagramResult>("/api/diagrams/refine", {
      conversation_id,
      diagram_id,
      followup_prompt,
      current_diagram_source,
      nodes,
      edges,
      provider,
    }, TIMEOUTS.refine, signal),

  updateDiagramStyle: (diagram_id: string, style: DiagramStyle) =>
    patch<{ diagram_id: string; style: DiagramStyle; updated_at: string }>(
      `/api/diagrams/${diagram_id}/style`,
      { style },
      TIMEOUTS.updateStyle,
    ),

  exportDiagram: (conversation_id: string, diagram_id: string, format: string) =>
    post<ExportResult>("/api/diagrams/export", {
      conversation_id,
      diagram_id,
      format,
    }, TIMEOUTS.export),

  listVersions: (conversation_id: string) =>
    get<VersionListResponse>(`/api/conversations/${conversation_id}/versions`, TIMEOUTS.listVersions),

  analyzeCodebase: (repo_url: string, diagram_type: string = "auto", signal?: AbortSignal) =>
    post<CodebaseAnalysisResponse>("/api/codebase/analyze", { repo_url, diagram_type }, TIMEOUTS.analyze, signal),

  generateCodebaseDiagram: (
    repo_url: string,
    diagram_type: string = "architecture",
    node_theme: string = "default",
    conversation_id?: string,
  ) =>
    post<DiagramResult>("/api/codebase/generate-diagram", {
      repo_url,
      diagram_type,
      node_theme,
      conversation_id,
    }, TIMEOUTS.generate),
};
