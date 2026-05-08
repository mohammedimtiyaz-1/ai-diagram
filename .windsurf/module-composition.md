# Module Composition

## How All Modules Work Together

This document defines the composition of frontend modules, backend modules, and the contracts between them.

---

## Frontend Composition

### Pages

| Route | Module | Depends On |
|-------|--------|-----------|
| `/` | `LandingPage` | `LandingHero`, `ExamplePrompts`, `FeatureCards`, `CTAButton` |
| `/workspace` | `WorkspacePage` | `WorkspaceShell` |

### Components (Hierarchy)

```
WorkspaceShell (split layout: left 40% / right 60%)
├── ChatPanel (left column)
│   ├── PromptInput
│   │   ├── Textarea
│   │   ├── DiagramTypeSelector (auto | architecture | hierarchy | token | workflow)
│   │   ├── SubmitButton
│   │   └── ExamplePrompts (clickable chips)
│   ├── VoiceInput
│   │   ├── MicButton
│   │   ├── RecordingIndicator
│   │   └── TranscriptEditor (editable textarea + confirm/cancel)
│   ├── EnhancedPromptPreview (collapsible, shown after enhancement)
│   │   ├── RawPromptDisplay
│   │   ├── EnhancedPromptDisplay
│   │   ├── EntitiesList
│   │   ├── AssumptionsList
│   │   └── CopyButton
│   └── ConversationHistory
│       ├── UserMessageBubble
│       ├── AssistantEnhancementBubble (shows enhanced prompt)
│       ├── AssistantDiagramBubble (shows title + explanation)
│       └── FollowUpInput (textarea + send, appears after first diagram)
│
└── DiagramPanel (right column)
    ├── DiagramPreview
    │   ├── MermaidRenderer (client-side only, dynamic import)
    │   ├── DiagramTitle
    │   └── DiagramExplanation
    ├── DiagramToolbar
    │   ├── ZoomControls (optional)
    │   └── FitToViewButton (optional)
    ├── VersionHistory (collapsible sidebar)
    │   ├── VersionListItem (version number, timestamp, changes summary)
    │   └── VersionSwitchButton
    └── ExportPanel
        ├── CopyMermaidButton
        ├── CopyJSONButton
        ├── CopyPromptButton
        ├── CopyExplanationButton
        └── ToastNotification
```

### State Stores

```
useWorkspaceStore (Zustand)
├── activePanel: 'chat' | 'diagram'
├── layoutMode: 'split' | 'chat-focus' | 'diagram-focus'
├── isMobile: boolean
└── setActivePanel, setLayoutMode

useConversationStore (Zustand)
├── conversationId: string | null
├── messages: Message[]
├── isEnhancing: boolean
├── isGenerating: boolean
├── isRefining: boolean
├── error: string | null
├── addMessage(message)
├── setLoading(state)
└── setError(error)

useDiagramStore (Zustand)
├── currentDiagram: DiagramVersion | null
├── diagramVersions: DiagramVersion[]
├── enhancedPrompt: EnhancementResult | null
├── setCurrentDiagram(diagram)
├── addVersion(version)
├── setEnhancedPrompt(result)
└── switchVersion(versionId)
```

### API Clients (TanStack Query)

```
promptApi
├── enhance(rawPrompt, diagramType) → EnhancementResult
└── (TanStack Query: mutation with loading/error states)

diagramApi
├── generate(enhancedPrompt, conversationId?) → DiagramResult
├── refine(conversationId, diagramId, followup) → DiagramResult
├── export(diagramId, format) → ExportResult
└── getVersions(conversationId) → VersionListResult

voiceApi
└── (no backend call — uses browser SpeechRecognition API directly)
```

---

## Backend Composition

### Package/Module Structure

```
app/
├── main.py                     # FastAPI app, middleware, CORS, startup/shutdown
├── core/
│   ├── config.py              # Pydantic Settings, env var loading
│   ├── errors.py              # Custom exceptions, error response builder
│   ├── logging.py             # Structured logging config
│   └── openai_client.py       # Singleton OpenAI client, retry logic
│
├── api/
│   ├── router.py              # Include all sub-routers
│   ├── deps.py                # FastAPI dependencies (get_services, get_provider)
│   └── routes/
│       ├── health.py          # GET /health
│       ├── prompts.py         # POST /api/prompts/enhance
│       ├── diagrams.py        # POST /api/diagrams/{generate,refine,export}
│       └── conversations.py   # GET /api/conversations/{id}/versions
│
├── services/
│   ├── prompt_enhancer.py     # Calls OpenAI to enhance raw prompt
│   ├── diagram_generator.py   # Orchestrates provider + AI for generation
│   ├── refinement_service.py # Orchestrates context + provider + AI for refinement
│   ├── export_service.py      # Formats diagram for export
│   ├── conversation_service.py # In-memory conversation store
│   └── version_service.py     # In-memory version tracking
│
├── providers/
│   ├── base.py                # DiagramProvider abstract class
│   ├── mermaid_provider.py    # MermaidProvider (MVP)
│   ├── eraser_provider.py     # EraserProvider (stub for future)
│   └── registry.py            # Provider factory: get_provider(name) -> DiagramProvider
│
├── schemas/
│   ├── prompt.py              # EnhanceRequest, EnhancementResult
│   ├── diagram.py             # DiagramResult, DiagramVersion, ExportRequest
│   ├── conversation.py        # Conversation, Message, VersionList
│   └── common.py              # ErrorResponse, SuccessResponse
│
├── prompts/
│   ├── enhancement.py         # System prompt for prompt enhancement
│   ├── generation/
│   │   ├── architecture.py    # Design system architecture diagram prompt
│   │   ├── hierarchy.py       # Component hierarchy diagram prompt
│   │   ├── token.py           # Token architecture diagram prompt
│   │   └── workflow.py        # Design-to-code workflow prompt
│   ├── refinement.py          # System prompt for diagram refinement
│   └── repair.py              # Prompt for fixing invalid AI output
│
└── tests/
    ├── conftest.py            # pytest fixtures, mock OpenAI client
    ├── test_schemas.py        # Pydantic model validation
    ├── test_prompts_api.py    # /api/prompts/enhance endpoint
    ├── test_diagrams_api.py   # /api/diagrams/* endpoints
    ├── test_services.py       # Service layer unit tests
    └── test_providers.py      # Provider abstraction tests
```

---

## Request Lifecycle

### Prompt Enhancement Lifecycle

```
1. User types prompt + selects diagram type
2. Frontend: TanStack Query mutation → POST /api/prompts/enhance
3. Backend: FastAPI receives request → Pydantic validates EnhanceRequest
4. Backend: PromptEnhancerService.enhance(raw_prompt, diagram_type)
5. Service: Builds prompt from templates (system + user)
6. Service: Calls OpenAI with structured JSON output mode
7. Service: Parses JSON response → EnhancementResult
8. Service: Validates result matches schema
9. Backend: Returns EnhancementResult as JSON
10. Frontend: TanStack Query caches result, updates Zustand store
11. UI: EnhancedPromptPreview component renders enhanced prompt
```

### Diagram Generation Lifecycle

```
1. User confirms enhanced prompt (or auto-proceeds)
2. Frontend: TanStack Query mutation → POST /api/diagrams/generate
3. Backend: FastAPI validates GenerateRequest (includes enhanced_prompt)
4. Backend: ConversationService creates new conversation (if no conversation_id)
5. Backend: DiagramGeneratorService.generate(enhanced_prompt, provider="mermaid")
6. Service: ProviderRegistry.get("mermaid") → MermaidProvider instance
7. Service: Provider builds generation prompt (diagram-type-specific)
8. Service: Provider calls OpenAI with JSON output mode
9. Service: Provider parses response → { title, mermaid_source, explanation }
10. Service: Provider validates Mermaid syntax (basic check)
11. Service: Returns DiagramResult
12. Backend: VersionService.create_version(conversation_id, diagram)
13. Backend: Returns DiagramResult + conversation_id
14. Frontend: Updates diagramStore, renders DiagramPreview
```

### Diagram Refinement Lifecycle

```
1. User sends follow-up message in chat
2. Frontend: TanStack Query mutation → POST /api/diagrams/refine
3. Backend: FastAPI validates RefineRequest
4. Backend: RefinementService.refine(conversation_id, diagram_id, followup)
5. Service: ConversationService loads conversation context
6. Service: PromptEnhancer enhances follow-up in context (optional)
7. Service: ProviderRegistry.get(provider) → MermaidProvider
8. Service: Provider.refine(existing_diagram, enhanced_followup, context)
9. Service: Provider calls OpenAI with diagram + follow-up context
10. Service: Returns updated DiagramResult with changes_summary
11. Backend: VersionService.create_version(conversation_id, new_diagram)
12. Backend: ConversationService.add_message(followup, response)
13. Backend: Returns DiagramResult
14. Frontend: Updates diagramStore, adds version, renders updated diagram
```

### Export Lifecycle

```
1. User clicks export button (Mermaid / JSON / Prompt / Explanation)
2. Frontend: TanStack Query mutation → POST /api/diagrams/export
3. Backend: ExportService.export(diagram_id, format)
4. Service: Loads diagram from VersionService
5. Service: Formats content based on format:
   - "mermaid": returns diagram_source
   - "json": returns full DiagramResult as JSON
   - "prompt": returns enhanced_prompt
   - "explanation": returns explanation
6. Backend: Returns { format, content, filename }
7. Frontend: Copies content to clipboard
8. Frontend: Shows toast notification
```

---

## Contracts Between Modules

### Frontend ↔ Backend Contract

**Rule: Frontend talks only to backend APIs. Never to OpenAI directly.**

| Direction | Contract | Technology |
|-----------|----------|------------|
| Frontend → Backend | HTTP REST JSON | TanStack Query + fetch |
| Backend → Frontend | JSON responses | FastAPI + Pydantic |
| Error format | Unified ErrorResponse | `{ error: { code, message, suggestion, retry_allowed } }` |
| Auth | None (MVP) | CORS only |
| Rate limiting | None (MVP) | Client-side debounce on submit |

### Backend Internal Contracts

**Rule: Services are independent. Routes depend on services. Services depend on providers/schemas. No circular dependencies.**

| Layer | Depends On | Does Not Depend On |
|-------|-----------|-------------------|
| Routes | Services | Providers, OpenAI client |
| Services | Providers, Schemas, Core config | Routes, other Services (loosely coupled) |
| Providers | OpenAI client, Schemas | Services, Routes |
| Schemas | Nothing (pure data) | Anything |
| Core | Nothing (infrastructure) | Anything |

### Provider Contract

**Rule: All providers implement `DiagramProvider` interface. Frontend never knows which provider is used.**

```python
class DiagramProvider(ABC):
    @abstractmethod
    async def generate_diagram(
        self,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext
    ) -> DiagramResult: ...

    @abstractmethod
    async def refine_diagram(
        self,
        existing_diagram: str,
        enhanced_followup: str,
        context: DiagramContext
    ) -> DiagramResult: ...

    @abstractmethod
    async def export_diagram(
        self,
        diagram_source: str,
        format: ExportFormat
    ) -> ExportResult: ...
```

**Normalized `DiagramResult` (regardless of provider):**
```json
{
  "diagram_id": "uuid",
  "title": "string",
  "diagram_type": "architecture | hierarchy | token | workflow",
  "provider": "mermaid | eraser",
  "diagram_source": "string (Mermaid syntax or graph JSON)",
  "diagram_format": "mermaid | graph-json | eraser",
  "explanation": "string",
  "changes_summary": ["string"],
  "metadata": { "node_count": 8, "edge_count": 7 }
}
```

### AI Output Contract

**Rule: All AI calls return JSON matching a Pydantic schema. Never free-form text.**

| AI Call | Expected JSON Schema | Validation |
|---------|---------------------|------------|
| Prompt enhancement | `EnhancementResult` | Pydantic parse |
| Diagram generation | `DiagramResult` | Pydantic parse + Mermaid validation |
| Diagram refinement | `DiagramResult` | Pydantic parse + Mermaid validation |
| Context summarization | `ConversationSummary` | Pydantic parse |

### State Flow Contract

**Rule: Frontend state transitions are predictable and user-visible.**

```
[IDLE] ──submit──► [ENHANCING] ──success──► [ENHANCED]
                                              │
                                              ▼ confirm
                                        [GENERATING] ──success──► [READY]
                                                                     │
                                                                     │ follow-up
                                                                     ▼
                                                                [REFINING] ──success──► [READY]
                                                                                          │
                                                                                          │ new version
                                                                                          ▼
                                                                                     [VERSION_UPDATED]
```

Each state transition updates UI:
- `ENHANCING`: Show spinner on input, disable submit
- `ENHANCED`: Show enhanced prompt preview, enable generate
- `GENERATING`: Show skeleton in diagram panel
- `READY`: Render diagram, show conversation history, enable follow-up
- `REFINING`: Show inline spinner, disable follow-up input
- `VERSION_UPDATED`: Highlight new version in sidebar, show changes summary

---

## Cross-Cutting Concerns

### Error Handling

**Strategy: Every layer handles errors at its boundary.**

| Layer | Error Type | Handler |
|-------|-----------|---------|
| Frontend input | Validation | Zod + React Hook Form (inline) |
| Frontend API | HTTP error | TanStack Query error state → ErrorBoundary |
| Backend API | Schema validation | Pydantic → 422 response |
| Backend service | Business logic | Custom exceptions → error response builder |
| AI call | Timeout/invalid JSON | Retry once → repair prompt → final error |
| Provider | Invalid output | Validate → retry → error with suggestion |

### Loading States

**Strategy: Every async operation has a visible loading state.**

| Operation | Loading Indicator | Location |
|-----------|-------------------|----------|
| Prompt enhancement | Spinner on submit button | ChatPanel |
| Diagram generation | Skeleton/placeholder | DiagramPanel |
| Refinement | Inline spinner + disabled input | FollowUpInput |
| Version switch | Brief spinner | DiagramPanel |
| Export | Button changes to "Copied!" | ExportPanel |
| Voice recording | Pulsing mic icon | VoiceInput |

### Logging

**Strategy: Structured logging at service boundaries.**

```python
# Every service method logs:
{
    "event": "prompt_enhancement_started",
    "conversation_id": "...",
    "raw_prompt_length": 120,
    "diagram_type": "architecture"
}

# Every AI call logs:
{
    "event": "openai_request",
    "model": "gpt-4o",
    "prompt_tokens": 800,
    "completion_tokens": 1200
}

# Every error logs:
{
    "event": "generation_failed",
    "error_code": "INVALID_MERMAID",
    "retry_attempt": 1,
    "will_retry": true
}
```

---

## Module Interaction Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  ChatPanel   │  │ DiagramPanel │  │   Zustand Stores     │  │
│  │  (Prompt +   │  │ (Mermaid +   │  │  (Conversation +     │  │
│  │   History)   │  │  Version +   │  │   Diagram + UI)      │  │
│  │              │  │  Export)     │  │                      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────────┘  │
│         │                  │                                     │
│         └──────────────────┘                                     │
│                   │                                               │
│            TanStack Query                                         │
│                   │                                               │
└───────────────────┼───────────────────────────────────────────────┘
                    │ HTTP/REST JSON
┌───────────────────┼───────────────────────────────────────────────┐
│                   ▼                                               │
│              BACKEND (FastAPI)                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  API Layer                                                  │  │
│  │  /api/prompts/enhance  →  PromptEnhancerService            │  │
│  │  /api/diagrams/generate → DiagramGeneratorService          │  │
│  │  /api/diagrams/refine  →  RefinementService                │  │
│  │  /api/diagrams/export  →  ExportService                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                         │                                         │
│  ┌──────────────────────┼─────────────────────────────────────┐  │
│  │  Provider Layer      │                                     │  │
│  │  ┌───────────────────┴─────────────────────────────────┐  │  │
│  │  │  DiagramProvider (ABC)                              │  │  │
│  │  │  ├── MermaidProvider (MVP)  →  OpenAI + Mermaid     │  │  │
│  │  │  └── EraserProvider (future) →  Eraser API         │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                         │                                         │
│  ┌──────────────────────┴─────────────────────────────────────┐  │
│  │  Storage Layer (MVP: in-memory)                            │  │
│  │  ConversationService  +  VersionService                     │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                         │                                         │
│                   OpenAI API                                    │
└─────────────────────────────────────────────────────────────────┘
```
