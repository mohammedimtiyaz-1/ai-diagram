# Technical Design: AI Design System Diagram Assistant

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                     │
│                                                              │
│  Landing Page → Workspace (Chat Panel + Diagram Panel)      │
│                                                              │
│  - Text/Voice Input                                          │
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
│   ├── PromptInput.tsx        # Text input + type selector
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
interface WorkspaceState {
  conversationId: string | null;
  messages: Message[];
  currentDiagram: DiagramVersion | null;
  diagramVersions: DiagramVersion[];
  enhancedPrompt: EnhancementResult | null;
  isEnhancing: boolean;
  isGenerating: boolean;
  isRefining: boolean;
  error: string | null;
}
```

---

## 3. Backend Architecture

### Framework & Stack
- **Python 3.11+**
- **FastAPI**
- **Pydantic v2** for validation
- **OpenAI Python SDK** (GPT-4o)
- **uvicorn** for ASGI server

### Project Structure
```
backend/
├── app/
│   ├── main.py                # FastAPI app initialization
│   ├── api/
│   │   ├── router.py         # Route registration
│   │   ├── prompts.py        # /api/prompts/* endpoints
│   │   ├── diagrams.py       # /api/diagrams/* endpoints
│   │   └── health.py         # /health endpoint
│   ├── services/
│   │   ├── enhancement.py    # Prompt enhancement logic
│   │   ├── generation.py     # Diagram generation orchestration
│   │   ├── refinement.py     # Follow-up refinement logic
│   │   ├── conversation.py   # Context management
│   │   ├── versioning.py     # Diagram version tracking
│   │   └── export.py         # Export formatting
│   ├── providers/
│   │   ├── base.py           # Abstract DiagramProvider
│   │   ├── mermaid.py        # MermaidProvider implementation
│   │   └── registry.py       # Provider registry
│   ├── schemas/
│   │   ├── requests.py       # API request models
│   │   ├── responses.py      # API response models
│   │   ├── diagram.py        # Diagram/Version models
│   │   └── conversation.py   # Conversation/Message models
│   ├── prompts/
│   │   ├── enhancement.py    # Enhancement prompt templates
│   │   ├── generation.py     # Generation prompt templates
│   │   └── refinement.py     # Refinement prompt templates
│   └── config.py             # Settings and environment
├── tests/
├── pyproject.toml
└── .env.example
```

---

## 4. AI Workflow Architecture

### Pipeline Stages

```
1. Input Normalization
   - Trim whitespace, validate length
   - Detect source (text/voice)

2. Prompt Enhancement (AI Call #1)
   - Extract design-system entities
   - Identify relationships
   - Classify diagram type
   - Rewrite into structured prompt
   - Flag assumptions

3. Diagram Generation (AI Call #2)
   - Select provider (Mermaid for MVP)
   - Adapt enhanced prompt for provider
   - Call AI with diagram-specific template
   - Validate output schema
   - Validate Mermaid syntax

4. Error Recovery
   - If invalid → retry with repair prompt
   - If still invalid → return error

5. Refinement (AI Call on follow-up)
   - Load conversation context
   - Enhance follow-up in context
   - Generate updated diagram
   - Track as new version
```

### Token Budget Management
- Enhancement prompt: ~500 tokens input, ~800 tokens output
- Generation prompt: ~800 tokens input, ~1500 tokens output
- Refinement: ~1500 tokens input (includes existing diagram), ~1500 tokens output
- Total per turn: ~2000-3000 tokens
- Context window for conversation: summarize after 5 messages

---

## 5. Provider Abstraction

```python
from abc import ABC, abstractmethod

class DiagramProvider(ABC):
    @abstractmethod
    async def generate_diagram(
        self, enhanced_prompt: str, context: DiagramContext
    ) -> DiagramResult:
        ...

    @abstractmethod
    async def refine_diagram(
        self, existing_diagram: str, enhanced_followup: str, context: DiagramContext
    ) -> DiagramResult:
        ...

    @abstractmethod
    async def export_diagram(
        self, diagram_source: str, format: ExportFormat
    ) -> ExportResult:
        ...
```

### MVP: MermaidProvider
- Calls OpenAI with Mermaid-specific prompt
- Returns valid Mermaid syntax
- Validates syntax before returning

### Future: EraserProvider
- Adapts enhanced prompt to Eraser API format
- Calls Eraser AI endpoint
- Returns Eraser diagram embed or image URL

---

## 6. Data Models

### Conversation
```python
class Conversation(BaseModel):
    id: str
    messages: list[Message]
    current_diagram_id: str | None
    diagram_versions: list[str]  # diagram IDs
    created_at: datetime
    updated_at: datetime
```

### DiagramVersion
```python
class DiagramVersion(BaseModel):
    id: str
    conversation_id: str
    version: int
    raw_prompt: str
    enhanced_prompt: str
    diagram_source: str          # Mermaid syntax
    diagram_format: str          # "mermaid" | "graph-json"
    diagram_type: str            # architecture | hierarchy | token | workflow
    title: str
    explanation: str
    provider: str
    changes_summary: list[str]   # empty for v1
    metadata: dict
    created_at: datetime
```

### Message
```python
class Message(BaseModel):
    id: str
    role: str                    # user | assistant | system
    content: str
    message_type: str            # input | enhancement | diagram | refinement | error
    timestamp: datetime
```

---

## 7. Error Handling Strategy

| Layer | Error Type | Action |
|-------|-----------|--------|
| Frontend input | Validation | Show inline error, prevent submit |
| Backend input | Schema validation | Return 422 with field-level errors |
| AI call | Timeout/rate limit | Retry once, then return 503 |
| AI output | Invalid JSON | Parse repair prompt, retry |
| AI output | Invalid Mermaid | Validate, retry with repair prompt |
| AI output | Irrelevant content | Return error suggesting rephrase |
| Provider | Connection failure | Return 503 with retry suggestion |

### Error Response Schema
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

## 8. Security Considerations

- **API key management**: OpenAI key stored server-side only, never exposed to frontend
- **Input sanitization**: All user inputs validated and sanitized
- **Rate limiting**: Per-session rate limits to prevent abuse (future)
- **No PII storage**: No user accounts, no personal data stored
- **CORS**: Configured for frontend origin only
- **Error messages**: Never expose internal details, stack traces, or API keys

---

## 9. Deployment Notes

### Local Development
```bash
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev

# Or single command:
make dev
```

### Environment Variables
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Future Deployment
- Frontend: Vercel (Next.js native)
- Backend: Railway / Render / Fly.io
- No database needed for MVP

---

## 10. Extension Strategy

| What to Add | How |
|-------------|-----|
| New provider (e.g., Eraser) | Implement `DiagramProvider` interface, register in provider registry |
| New diagram type | Add type to classifier, add prompt template in `prompts/` |
| New export format | Add format handler in `ExportService` |
| Persistence | Swap in-memory stores for SQLite/PostgreSQL |
| Authentication | Add auth middleware, user model, session management |
| Real-time updates | Add WebSocket layer for streaming generation |
