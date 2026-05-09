# Technical Design: AI Design System Diagram Assistant

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                     │
│                                                              │
│  Landing Page → Workspace (Chat Panel + Diagram Panel)      │
│                                                              │
│  - Text/Voice Input                                          │
│  - GitHub URL Input (Mode Selection)                         │
│  - Diagram Type & Theme Selectors                            │
│  - Enhanced Prompt Preview                                   │
│  - Mermaid Renderer                                          │
│  - Conversation History                                      │
│  - Version History                                           │
│  - Export Panel                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
┌──────────────────────────▼──────────────────────────────────┐
│                        Backend (FastAPI)                      │
│                                                              │
│  API Layer → Services → Provider Abstraction → AI (OpenAI)  │
│                                                              │
│  - Prompt Enhancement Service                                │
│  - Codebase Analysis Service (GitHub Integration)            │
│  - Diagram Generation Service                                │
│  - Refinement Service                                        │
│  - Conversation Context Service                              │
│  - Versioning Service                                        │
│  - Export Service                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Frontend Architecture

### Framework & Stack
- **Next.js 14+** with App Router
- **TypeScript** (strict mode)
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Mermaid.js** for diagram rendering
- **Zustand** for client state management

### Route Structure
```
/                  → Landing page
/workspace         → Main workspace (chat + diagram)
```

### Component Architecture
```
app/
├── layout.tsx                  # Root layout
├── page.tsx                    # Landing page
├── workspace/
│   └── page.tsx               # Workspace page
components/
├── landing/
│   ├── Hero.tsx
│   ├── ExamplePrompts.tsx
│   └── FeatureCards.tsx
├── workspace/
│   ├── WorkspaceLayout.tsx    # Split panel layout
│   ├── ChatPanel.tsx          # Left panel
│   ├── DiagramPanel.tsx       # Right panel
│   ├── InputModeToggle.tsx    # Prompt vs GitHub selection
│   ├── PromptInput.tsx        # Text input + type selector
│   ├── CodebaseInput.tsx      # GitHub URL + type + theme selectors
│   ├── VoiceInput.tsx         # Mic button + transcript
│   ├── EnhancedPromptPreview.tsx
│   ├── ConversationHistory.tsx
│   ├── MermaidRenderer.tsx
│   ├── VersionHistory.tsx
│   └── ExportPanel.tsx
├── ui/                        # shadcn/ui components
└── shared/
    ├── LoadingState.tsx
    ├── ErrorState.tsx
    └── EmptyState.tsx
```

### State Management (Zustand)
```typescript
type InputMode = "prompt" | "codebase";

interface WorkspaceState {
  inputMode: InputMode;
  conversationId: string | null;
  messages: Message[];
  currentDiagram: DiagramVersion | null;
  diagramVersions: DiagramVersion[];
  enhancedPrompt: EnhancementResult | null;
  isEnhancing: boolean;
  isGenerating: boolean;
  isRefining: boolean;
  isAnalyzing: boolean;
  error: string | null;
}
```

### Client-Side Persistence
- **Storage**: `localStorage` via clean adapter at `lib/storage/workspace-storage.ts`
- **Key**: `ai-design-system-diagram-assistant:workspace:v1`
- **Schema version**: `1` (validated on load; invalid/outdated data resets safely)
- **Persisted fields**: conversation, messages, diagram, versions, rawPrompt, selectedDiagramType, selectedNodeTheme, repoUrl, diagramStyle, inputMode
- **Excluded fields**: loading, error, AbortController, tooltip positions, hover state
- **Auto-save**: Zustand `subscribe` writes stable state on every change
- **Hydration**: `useEffect` in `WorkspacePage` calls `hydrateFromStorage()` once on mount; loading is reset to `idle`; no API calls are auto-triggered

### Expensive API Reliability & UX
- **Timeouts**: Backend `with_timeout()` wrapper; frontend `fetchWithTimeout()` with per-API timeouts
  - Enhance: 30s, Refine: 45s, Analyze: 60s
- **Rate Limiting**: In-memory sliding-window `RateLimiter` per client IP; replaceable with Redis
  - Enhance: 10/min, Refine: 8/min, Analyze: 5/min
- **Error Classification**: Frontend `TimeoutError`, `RateLimitError`, `CancelledError` with friendly messages
- **Cancel**: User clicks Cancel → `AbortController` aborts in-flight request; previous state preserved
- **Duplicate Prevention**: Each handler guards with `isBusy`; buttons disabled while loading
- **Safe State**: On any failure, current diagram/conversation is never overwritten

---

## 3. Backend Architecture

### Framework & Stack
- **Python 3.11+**
- **FastAPI**
- **Pydantic v2** for validation
- **OpenAI Python SDK** (GPT-4o)
- **httpx** for GitHub API interaction

### Project Structure
```
backend/
├── app/
│   ├── main.py                # FastAPI app initialization
│   ├── api/
│   │   ├── router.py         # Route registration
│   │   ├── prompts.py        # /api/prompts/* endpoints
│   │   ├── codebase.py       # /api/codebase/* endpoints (NEW)
│   │   ├── diagrams.py       # /api/diagrams/* endpoints
│   │   └── health.py         # /health endpoint
│   ├── services/
│   │   ├── enhancement.py    # Prompt enhancement logic
│   │   ├── codebase.py       # GitHub tree fetching & file selection (NEW)
│   │   ├── generation.py     # Diagram generation orchestration
│   │   ├── refinement.py     # Follow-up refinement logic
│   │   ├── conversation.py   # Context management
│   │   ├── versioning.py     # Diagram version tracking
│   │   └── export.py         # Export formatting
│   ├── providers/
│   │   ├── base.py           # Abstract DiagramProvider
│   │   ├── mermaid.py        # MermaidProvider implementation
│   ├── schemas/
│   │   ├── requests.py       # API request models
│   │   ├── codebase.py       # Codebase analysis models (NEW)
│   │   ├── diagram.py        # Diagram/Version models
│   │   └── conversation.py   # Conversation/Message models
│   ├── prompts/
│   │   ├── enhancement.py    # Enhancement prompt templates
│   │   ├── codebase.py       # Codebase analysis templates (NEW)
│   │   ├── generation.py     # Generation prompt templates
│   │   └── refinement.py     # Refinement prompt templates
```

---

## 4. AI Workflow Architecture

### Flow A: Prompt Enhancement
- Identical to existing design-system flow.

### Flow B: Codebase Analysis (NEW)
```
1. Repository Parsing
   - Extract owner/repo from GitHub URL
   - Validate public accessibility

2. Tree Extraction
   - Fetch recursive tree from GitHub API
   - Filter out node_modules, dist, hidden files
   - Identify "important" files (package.json, tsconfig, etc.)

3. Content Fetching (Selective)
   - Read content of package.json for stack detection
   - Read README.md for project overview
   - Fetch entry points (main.ts, app.py, etc.)
   - Fetch route definitions if possible

4. Architecture Summary (AI Call #1 - Codebase Analyzer)
   - Input: Filtered tree + Selected file contents
   - Output: Tech stack, major modules, architecture pattern, summary

5. Diagram Prompt Generation (AI Call #2 - Codebase Enhancer)
   - Convert analysis into a structured diagram prompt based on selected type

6. Diagram Generation (AI Call #3 - Provider)
   - Generate Mermaid source with node metadata (related_files included)
```

---

## 5. Provider Abstraction & Themes

### Node Themes System
Node themes are visual-only customizations that map theme names to Mermaid styling configurations.

**Supported Themes:**
- **Default**: standard design-system colors
- **Minimal**: grayscale, thin borders
- **Soft**: pastel backgrounds, rounded corners
- **Technical**: high contrast, mono fonts
- **Colorful**: vibrant per-type colors
- **Dark**: neon colors on dark backgrounds
- **Enterprise**: deep blues, formal structure

**Implementation Rule:**
Theme changes should apply via CSS variable updates in the `MermaidRenderer` or by appending `style` / `classDef` blocks to the Mermaid source without calling the AI, unless a complete regeneration is required by the user.

---

## 6. Data Models

### DiagramNode (Updated)
```python
class DiagramNode(BaseModel):
    id: str
    label: str
    type: str
    metadata: dict = {
        "tooltip_title": str,
        "tooltip_description": str,
        "role": str,
        "importance": "low | medium | high",
        "connections_summary": str,
        "related_files": list[str] | None  # NEW: Paths in the codebase
    }
    style: dict
```

### CodebaseAnalysisResponse (NEW)
```python
class CodebaseAnalysisResponse(BaseModel):
    analysis_id: str
    repo_name: str
    detected_stack: list[str]
    important_files: list[str]
    project_summary: str
    architecture_summary: str
    recommended_diagram_type: str
    enhanced_prompt: str
    warnings: list[str]
```

---

## 8. Security Considerations

- **GitHub Public API**: Use public endpoints; enforce rate-limit awareness in UI.
- **Selective Fetching**: Never fetch entire repositories; limit total bytes read.
- **Secret Redaction**: AI analyzer prompt includes instructions to ignore/redact `.env` patterns or credentials.
- **No Private Repos**: MVP strictly enforces public GitHub URL check.
- **CORS & Proxying**: All GitHub requests are proxied through the backend to protect client IP and manage rate limits centrally.
