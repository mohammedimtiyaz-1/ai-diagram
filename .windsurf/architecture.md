# Architecture: AI Design System Diagram Assistant

## System Overview

```
User Input (text/voice)
  → Input Normalization
  → Design-System Intent Extraction
  → Prompt Enhancement (AI)
  → Diagram Type Classification
  → Provider-Specific Prompt Adaptation
  → Diagram Provider (Mermaid / Eraser / Structured Graph)
  → Generated Diagram
  → Frontend Renderer
  → User Follow-up Chat
  → Context-Aware Refinement (AI)
  → New Diagram Version
```

---

## Frontend Architecture

### Pages
- **Landing Page** — product explanation, examples, CTA
- **Workspace Page** — main working area (chat + diagram)

### Components
- **Chat Input Panel** — text input, submit, example prompts
- **Voice Input Module** — mic recording, transcript preview/edit
- **Enhanced Prompt Preview** — show raw vs enhanced prompt, copy actions
- **Diagram Preview Panel** — Mermaid/React Flow renderer, title, explanation
- **Conversational Refinement Panel** — follow-up messages, conversation history
- **Diagram Version History** — version list, restore, compare
- **Export Actions** — Mermaid, JSON, prompt, explanation copy
- **Settings/Provider Selector** — choose diagram provider (future)

### State Management
- Conversation state (messages, diagram versions)
- Current diagram state (source, format, metadata)
- UI state (loading, errors, active panel)

### Tech Stack
- Next.js App Router
- TypeScript
- Tailwind CSS
- shadcn/ui
- Mermaid.js (MVP renderer)
- React Flow (alternative/future renderer)
- Zustand or TanStack Query

---

## Backend Architecture

### API Layer
- Health check endpoint
- Prompt enhancement endpoint
- Diagram generation endpoint
- Diagram refinement endpoint
- Voice transcription endpoint
- Export endpoint

### Services
- **Prompt Enhancement Service** — rewrites raw input into diagram-optimized prompt
- **Diagram Generation Service** — orchestrates provider calls
- **Diagram Provider Abstraction** — pluggable interface for providers
- **Conversation Context Service** — manages message history and diagram context
- **Diagram Version Service** — tracks diagram versions within conversation
- **Export Service** — converts diagram to requested format

### Provider Interface

```python
class DiagramProvider(ABC):
    async def generate_diagram(self, enhanced_prompt: str, context: DiagramContext) -> DiagramResult
    async def refine_diagram(self, existing_diagram: str, enhanced_followup: str, context: DiagramContext) -> DiagramResult
    async def export_diagram(self, diagram: str, format: ExportFormat) -> ExportResult
```

### Providers
- **MermaidProvider** (MVP) — generates Mermaid syntax
- **StructuredGraphProvider** — generates JSON graph for React Flow
- **EraserProvider** (future) — adapter for Eraser AI API

### Tech Stack
- Python 3.11+
- FastAPI
- Pydantic v2
- OpenAI API (GPT-4o structured output)
- Optional: SQLite for diagram persistence
- Optional: Redis for session context (post-MVP)

---

## AI Architecture

### Agents/Services
- **Raw Prompt Analyzer** — extracts design-system intent and entities
- **Design-System Prompt Enhancer** — rewrites for clarity and diagram generation
- **Diagram Type Classifier** — selects best diagram type for the input
- **Provider Prompt Builder** — adapts enhanced prompt for specific provider format
- **Refinement Prompt Builder** — merges follow-up with existing context
- **Context Summarizer** — compresses long conversations to fit token limits

### Prompt Enhancement Output
Enhanced prompt includes:
- Diagram goal
- Relevant design-system entities
- Relationships between entities
- Diagram type recommendation
- Expected structure/layout hints
- Visual clarity instructions
- Inferred assumptions (flagged)

---

## Data Flow (Detailed)

### Initial Generation
```
1. User types/speaks input
2. Frontend validates input (min length, not empty)
3. POST /api/prompts/enhance → AI enhances prompt
4. Frontend shows enhanced prompt preview
5. POST /api/diagrams/generate → provider generates diagram
6. Frontend renders diagram (Mermaid/React Flow)
7. Conversation state initialized
```

### Conversational Refinement
```
1. User sends follow-up message
2. POST /api/diagrams/refine (with conversation_id, current diagram)
3. AI enhances follow-up in context of existing diagram
4. Provider generates updated diagram
5. Frontend renders new version
6. Version history updated
```

---

## Data Models

### Conversation
- conversation_id
- messages[] (role, content, timestamp)
- current_diagram_id
- diagram_versions[]
- created_at

### DiagramVersion
- diagram_id
- version_number
- raw_prompt
- enhanced_prompt
- diagram_source (Mermaid string / graph JSON)
- diagram_format
- diagram_type
- explanation
- provider
- metadata
- created_at

### Message
- role (user | assistant | system)
- content
- type (input | enhanced_prompt | diagram | refinement | error)
- timestamp

---

## Extension Points

| Extension | How to Add |
|-----------|-----------|
| New diagram provider | Implement `DiagramProvider` interface |
| New diagram type | Add type to classifier, add prompt template |
| New export format | Add format to `ExportService` |
| Persistent storage | Swap in-memory store for SQLite/PostgreSQL |
| Real-time collaboration | Add WebSocket layer on top of conversation service |
