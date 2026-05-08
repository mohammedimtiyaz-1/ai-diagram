# AI Design System Diagram Assistant — Architecture Blueprint

## Product Summary

AI Design System Diagram Assistant lets users describe design system ideas in plain text or voice, then transforms those raw ideas into polished, structured diagrams. The application uses an AI-first pipeline: raw input is enhanced into a structured prompt, a diagram is generated via a pluggable provider (Mermaid MVP, Eraser future), the diagram is displayed in a split-panel workspace, and users can continue chatting to refine the diagram iteratively. Versions are tracked, and everything can be exported.

The product is a portfolio-grade SaaS MVP — small enough to ship quickly, polished enough to impress.

---

## Core User Journey

```
[LANDING] User sees product explanation + example prompts
           ↓ CTA
[WORKSPACE] User enters text or clicks microphone
           ↓
[ENHANCE] System sends raw input to AI, gets enhanced prompt
           ↓
[PREVIEW] User sees enhanced prompt (entities, assumptions, type)
           ↓
[GENERATE] System sends enhanced prompt to diagram provider
           ↓
[DISPLAY] Diagram renders in right panel, title + explanation shown
           ↓
[CHAT] User sends follow-up message
           ↓
[REFINE] System keeps context, generates updated diagram
           ↓
[VERSION] New version created, history visible
           ↓
[EXPORT] User copies Mermaid, JSON, prompt, or explanation
```

---

## System Context

| Component | Responsibility | MVP Choice | Future |
|-----------|-------------|------------|--------|
| **Frontend** | UI, state, rendering | Next.js App Router | — |
| **Backend** | API, orchestration, validation | FastAPI | — |
| **AI Provider** | Prompt enhancement, generation, refinement | OpenAI GPT-4o | Claude, local models |
| **Diagram Provider** | Generate diagram from enhanced prompt | MermaidProvider | EraserProvider |
| **Storage** | Conversation + version persistence | In-memory + localStorage | PostgreSQL |

---

## Application Layers

### 1. Presentation Layer (Frontend)

**Next.js UI** — Two primary routes:
- `/` — Landing page (hero, features, examples, CTA)
- `/workspace` — Split-panel workspace

**Workspace UI** — Left panel (chat) + Right panel (diagram):
- **Chat Input Panel**: textarea, diagram type selector, submit, example prompts
- **Voice Input Module**: mic button, recording indicator, transcript preview/edit
- **Enhanced Prompt Preview**: collapsible raw vs enhanced, entities list, copy button
- **Conversation History**: user messages + assistant responses (enhancement, diagram, refinement)
- **Diagram Preview Panel**: Mermaid renderer, title, explanation
- **Diagram Version History**: sidebar list, version numbers, change summaries
- **Export Actions**: buttons for Mermaid, JSON, enhanced prompt, explanation
- **Error/Loading/Empty States**: full-screen overlays and inline feedback

### 2. Client State Layer (Frontend)

Managed via **Zustand** stores:

| Store | State |
|-------|-------|
| `useWorkspaceStore` | active panel, layout mode, loading states |
| `useConversationStore` | messages, conversationId, isEnhancing, isGenerating, isRefining |
| `useDiagramStore` | currentDiagram, diagramVersions, enhancedPrompt, error |

Key state transitions:
- `IDLE` → `ENHANCING` → `ENHANCED` → `GENERATING` → `READY`
- `READY` → `REFINING` → `READY` (new version)

### 3. API Layer (Backend)

**FastAPI** with 5 endpoint groups:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Service health check |
| `POST /api/prompts/enhance` | Enhance raw input into structured prompt |
| `POST /api/diagrams/generate` | Generate diagram from enhanced prompt |
| `POST /api/diagrams/refine` | Update diagram from follow-up + context |
| `POST /api/diagrams/export` | Export current diagram in chosen format |
| `GET /api/conversations/{id}/versions` | Get version history |

All endpoints use **Pydantic v2** for request/response validation.
All endpoints return structured error objects (never stack traces).

### 4. AI Workflow Layer (Backend)

Three AI-powered services:

| Service | AI Call | Input | Output |
|---------|---------|-------|--------|
| **Prompt Enhancer** | 1 | Raw prompt + diagram type hint | Enhanced prompt + entities + assumptions |
| **Diagram Generator** | 2 (after enhancement) | Enhanced prompt + provider config | Diagram source (Mermaid) + title + explanation |
| **Refinement Service** | 3+ (per follow-up) | Follow-up + current diagram + context | Updated diagram + changes summary |

**Orchestration rules:**
- Enhancement is mandatory (can be hidden from user if configured, but must run)
- Generation always uses the enhanced prompt, never raw input directly
- Refinement always preserves existing diagram structure unless explicitly changed
- All AI calls use `response_format: { type: "json_object" }`
- Retry once on any AI failure before returning error to client

### 5. Diagram Provider Layer (Backend)

**Provider Interface** (`DiagramProvider` abstract base class):

```
DiagramProvider
├── generate_diagram(enhanced_prompt, context) → DiagramResult
├── refine_diagram(existing_diagram, enhanced_followup, context) → DiagramResult
└── export_diagram(diagram_source, format) → ExportResult
```

**MermaidProvider** (MVP):
- Calls OpenAI with Mermaid-specific prompt template
- Returns valid Mermaid syntax
- Validates basic syntax before returning
- Supports 4 diagram types via different prompt templates

**EraserProvider** (Future placeholder):
- Will adapt enhanced prompt to Eraser API format
- Will call Eraser AI endpoint
- Will return Eraser embed or image URL
- Same interface, different internals

**Registry pattern:** Provider selected by name (`"mermaid"`, `"eraser"`), resolved at runtime.

### 6. Persistence Layer (MVP: In-Memory + Optional localStorage)

**Backend (in-memory):**
- `ConversationService` holds active conversations in dict
- `VersionService` holds diagram versions per conversation
- Data lost on server restart (acceptable for MVP)
- Thread-safe for concurrent requests

**Frontend (localStorage):**
- Optionally cache conversation ID + current diagram
- Survives page refresh
- Not required for MVP demo

**Future (PostgreSQL/SQLite):**
- `conversations` table
- `diagram_versions` table
- `messages` table
- Migration path from in-memory → SQLAlchemy models

---

## Module Dependency Map

```
Frontend (Next.js)
├── pages/
│   ├── landing.tsx       ← no deps
│   └── workspace.tsx     ← Layout
├── components/
│   ├── LandingHero       ← no deps
│   ├── WorkspaceShell    ← ChatPanel + DiagramPanel
│   ├── ChatPanel         ← PromptInput + ConversationHistory + VoiceInput
│   ├── PromptInput       ← calls promptApi
│   ├── VoiceInput        ← Web Speech API
│   ├── EnhancedPreview   ← reads conversationStore
│   ├── DiagramPreview    ← Mermaid.js + diagramStore
│   ├── VersionHistory    ← diagramApi.getVersions
│   └── ExportPanel       ← diagramApi.export
├── stores/
│   ├── useConversationStore
│   ├── useDiagramStore
│   └── useWorkspaceStore
└── api/
    ├── promptApi.ts      → POST /api/prompts/enhance
    ├── diagramApi.ts     → POST /api/diagrams/{generate,refine,export}
    └── voiceApi.ts       → (browser API, no backend call)

Backend (FastAPI)
├── api/routes/
│   ├── health.py         ← no deps
│   ├── prompts.py        ← PromptEnhancerService
│   ├── diagrams.py       ← DiagramGeneratorService + RefinementService + ExportService
│   └── conversations.py  ← ConversationService + VersionService
├── services/
│   ├── prompt_enhancer.py      ← OpenAI client
│   ├── diagram_generator.py    ← ProviderRegistry + AI client
│   ├── refinement_service.py   ← ContextService + ProviderRegistry
│   ├── export_service.py       ← formatting only
│   ├── conversation_service.py ← in-memory store
│   └── version_service.py      ← in-memory store
├── providers/
│   ├── base.py           ← DiagramProvider (ABC)
│   ├── mermaid.py        ← MermaidProvider (MVP)
│   ├── eraser.py         ← EraserProvider (stub)
│   └── registry.py       ← factory pattern
├── schemas/
│   ├── prompt.py
│   ├── diagram.py
│   ├── conversation.py
│   └── common.py
├── prompts/
│   ├── enhancement.py    ← system prompt template
│   ├── generation/       ← per-type generation prompts
│   └── refinement.py     ← refinement system prompt
└── core/
    ├── config.py
    ├── errors.py
    └── openai_client.py
```

**Dependency rules:**
- Frontend talks **only** to backend APIs (never to OpenAI directly)
- Backend services are **independent** (PromptEnhancer does not know about DiagramGenerator)
- Providers depend only on the abstract `DiagramProvider` interface
- Routes depend on services, services depend on providers/schemas
- No service should import another service's internal logic

---

## Data Flow Diagrams

### Text → Diagram Flow

```
User types prompt
  → PromptInput component
  → promptApi.enhance({ raw_prompt, diagram_type })
  → POST /api/prompts/enhance
  → PromptEnhancerService calls OpenAI
  → Returns EnhancementResult
  → Frontend shows EnhancedPreview
  → diagramApi.generate({ enhanced_prompt, conversation_id })
  → POST /api/diagrams/generate
  → DiagramGeneratorService
  → ProviderRegistry.get("mermaid")
  → MermaidProvider calls OpenAI with diagram prompt
  → Returns DiagramResult
  → Frontend renders DiagramPreview
  → User sees diagram + title + explanation
```

### Voice → Diagram Flow

```
User clicks mic
  → VoiceInput starts Web Speech API
  → Transcript appears in editable textarea
  → User edits / confirms
  → Confirmed transcript sent as text prompt
  → Follows exact same flow as Text → Diagram from this point
```

### Follow-up Refinement Flow

```
User sends follow-up message
  → ConversationHistory component
  → diagramApi.refine({ conversation_id, diagram_id, followup_prompt })
  → POST /api/diagrams/refine
  → RefinementService:
      1. Calls PromptEnhancer on follow-up (in context)
      2. Loads current diagram + conversation history
      3. Calls MermaidProvider.refine()
      4. Provider calls OpenAI with diagram + follow-up
      5. Returns updated DiagramResult
  → VersionService creates new version (n+1)
  → Frontend updates DiagramPreview
  → VersionHistory shows new version
  → User can switch versions
```

### Export Flow

```
User clicks Export button (Mermaid / JSON / Prompt / Explanation)
  → ExportPanel component
  → diagramApi.export({ diagram_id, format })
  → POST /api/diagrams/export
  → ExportService formats content
  → Returns { format, content, filename }
  → Frontend copies to clipboard
  → Toast notification confirms
```

---

## Failure Handling

| Failure | Layer | Detection | Action |
|---------|-------|-----------|--------|
| **Invalid input** | Frontend | Client validation | Inline error, prevent submit |
| **Schema validation error** | API | Pydantic | 422 with field-level errors |
| **AI timeout (>15s)** | Backend | Timeout wrapper | Retry once, then 503 |
| **AI returns invalid JSON** | Backend | JSON parse fail | Send repair prompt, retry once |
| **AI returns invalid Mermaid** | Backend | Regex/parser | Send repair prompt, retry once |
| **Provider unavailable** | Backend | Connection error | 503, suggest retry |
| **Conversation not found** | Backend | KeyError | 404, suggest new conversation |
| **Mermaid render failure** | Frontend | Mermaid.js error | Show code block fallback + error message |
| **Browser Speech API unsupported** | Frontend | Feature detection | Hide/disable mic button |
| **Context too long** | Backend | Token count | Summarize context, then proceed |

**Error response contract (all APIs):**
```json
{
  "error": {
    "code": "GENERATION_FAILED",
    "message": "We couldn't generate a diagram from that input.",
    "suggestion": "Try being more specific about components and relationships.",
    "retry_allowed": true
  }
}
```

---

## Extensibility Plan

| Extension | How | Effort |
|-----------|-----|--------|
| **Eraser provider** | Implement `DiagramProvider` interface, create `EraserProvider`, register in `ProviderRegistry` | Medium |
| **React Flow provider** | Implement `DiagramProvider` returning graph JSON, add React Flow renderer in frontend | Medium |
| **Database persistence** | Replace in-memory services with SQLAlchemy + PostgreSQL/SQLite, keep same interfaces | Low |
| **Authentication** | Add OAuth middleware, `user_id` to conversation models, auth-required decorators | Medium |
| **Project/workspace support** | Add `Project` entity, nest conversations under projects | Medium |
| **Image export (PNG/SVG)** | Add `image` format to ExportService, use Mermaid CLI or browser canvas | Low |
| **Design token import** | Add parser for Figma/token JSON, pre-populate diagram prompt with token data | Medium |
| **New diagram type** | Add prompt template in `prompts/generation/`, update classifier logic | Low |
| **Multiple AI models** | Add model selector to config, pass model name to OpenAI client | Low |

**Key design principle:** Every extension goes through an existing interface or adds a new interface. Never modifies existing working code.
