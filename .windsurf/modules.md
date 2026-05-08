# AI Design System Diagram Assistant — Feature Modules

Modules organized by **user-facing capability**, not technical implementation.

---

## Frontend Modules

### Module 1: Landing Page

**User Goal**: Understand the product and start immediately.

**Inputs**: None (entry point)
**Outputs**: User navigates to workspace

**MVP Scope**: ✅ In

**Capabilities**:
- Explain product value in one sentence
- Show design-system diagram examples
- Provide 3-5 clickable example prompts
- CTA to workspace
- Responsive layout (desktop-first)

---

### Module 2: Design System Workspace

**User Goal**: Main working area for generating and refining diagrams.

**Inputs**: User interaction
**Outputs**: Diagram + conversation state

**MVP Scope**: ✅ In

**Layout**:
- Split layout: left panel (chat/prompt) + right panel (diagram preview)
- Collapsible panels for flexibility
- Persistent conversation state

---

### Module 3: Prompt Input

**User Goal**: Describe a design-system idea for AI processing.

**Inputs**: Plain text (10-2000 characters) + diagram type selection
**Outputs**: Validated input sent to prompt enhancement

**MVP Scope**: ✅ In

**Capabilities**:
- Textarea with character count
- Diagram type selector (Auto / Architecture / Hierarchy / Token / Workflow)
- Submit button (disabled when invalid)
- Example prompts populate input on click
- Loading state on submit

---

### Module 4: Voice Input

**User Goal**: Describe design-system ideas verbally.

**Inputs**: Audio from browser microphone
**Outputs**: Editable transcript

**MVP Scope**: ✅ In

**Capabilities**:
- Mic button with recording state indicator
- Browser permission handling
- Transcript displayed in editable textarea
- Confirm/cancel actions
- Graceful fallback if unsupported

---

### Module 5: Prompt Enhancement Preview

**User Goal**: See how AI improved the prompt before diagram generation.

**Inputs**: Raw prompt + enhanced prompt response
**Outputs**: Display of both prompts, copy action

**MVP Scope**: ✅ In

**Capabilities**:
- Show raw prompt (what user typed)
- Show enhanced prompt (what AI improved)
- Show extracted entities and assumptions
- Copy enhanced prompt button
- Optional: regenerate enhancement

---

### Module 6: Diagram Renderer

**User Goal**: View the generated design-system diagram.

**Inputs**: Mermaid source (or graph JSON)
**Outputs**: Rendered visual diagram

**MVP Scope**: ✅ In

**Capabilities**:
- Render Mermaid diagram in preview panel
- Show diagram title and explanation
- Show diagram metadata (type, provider, version)
- Handle invalid Mermaid gracefully (error state)
- Zoom/pan if diagram is large

---

### Module 7: Conversational Refinement Panel

**User Goal**: Iterate on the diagram through follow-up messages.

**Inputs**: Follow-up text from user
**Outputs**: Updated diagram version

**MVP Scope**: ✅ In

**Capabilities**:
- Follow-up message input (below conversation history)
- Display conversation messages (user + assistant)
- New diagram version rendered after refinement
- Context maintained across messages
- Clear "this modifies existing diagram" visual cue

---

### Module 8: Diagram Version History

**User Goal**: Navigate between diagram iterations.

**Inputs**: Diagram version list
**Outputs**: Selected version displayed

**MVP Scope**: ✅ In

**Capabilities**:
- List of versions (v1, v2, v3...)
- Current version highlighted
- Click to view any version
- Show change summary per version
- Restore previous version (optional stretch)

---

### Module 9: Export

**User Goal**: Use diagram output in other tools.

**Inputs**: Current diagram state
**Outputs**: Exported content (Mermaid, JSON, prompt, explanation)

**MVP Scope**: ✅ In

**Capabilities**:
- Export Mermaid syntax
- Export diagram JSON
- Copy enhanced prompt
- Copy diagram explanation
- One-click copy to clipboard
- Success toast on copy
- Future: PNG/SVG export

---

## Backend Modules

### Module B1: Prompt Enhancement API

**Purpose**: Enhance raw user input into diagram-generation-ready prompt.

**Endpoint**: `POST /api/prompts/enhance`
**MVP Scope**: ✅ In

**Capabilities**:
- Analyze raw input for design-system intent
- Extract entities and relationships
- Classify diagram type
- Generate enhanced prompt
- Flag assumptions made
- Return structured enhancement response

---

### Module B2: Diagram Generation API

**Purpose**: Generate diagram from enhanced prompt via provider.

**Endpoint**: `POST /api/diagrams/generate`
**MVP Scope**: ✅ In

**Capabilities**:
- Accept enhanced prompt + context
- Route to selected provider (Mermaid MVP)
- Validate diagram output
- Retry once on failure
- Return diagram with metadata and explanation
- Initialize conversation context

---

### Module B3: Diagram Refinement API

**Purpose**: Modify existing diagram based on follow-up instructions.

**Endpoint**: `POST /api/diagrams/refine`
**MVP Scope**: ✅ In

**Capabilities**:
- Accept follow-up + existing diagram context
- Enhance follow-up in context
- Generate updated diagram
- Increment version
- Return changes summary
- Maintain conversation state

---

### Module B4: Diagram Provider Adapter

**Purpose**: Abstraction layer for pluggable diagram generation.

**MVP Scope**: ✅ In

**Providers**:
- MermaidProvider (MVP) — generates Mermaid syntax via OpenAI
- StructuredGraphProvider (future) — JSON graph for React Flow
- EraserProvider (future) — Eraser AI API adapter

**Interface**:
- `generate_diagram(enhanced_prompt, context) → DiagramResult`
- `refine_diagram(existing, followup, context) → DiagramResult`
- `export_diagram(diagram, format) → ExportResult`

---

### Module B5: Conversation Context Service

**Purpose**: Manage message history and diagram context within a session.

**MVP Scope**: ✅ In (in-memory)

**Capabilities**:
- Store messages per conversation
- Track current diagram state
- Summarize context if conversation grows long
- Provide context to refinement calls

---

### Module B6: Diagram Versioning Service

**Purpose**: Track diagram iterations within a conversation.

**MVP Scope**: ✅ In (in-memory)

**Capabilities**:
- Store diagram versions
- Return version list
- Retrieve specific version
- Track changes between versions

---

### Module B7: Export Service

**Purpose**: Format diagram data for export.

**Endpoint**: `POST /api/diagrams/export`
**MVP Scope**: ✅ In

**Capabilities**:
- Return Mermaid source
- Return graph JSON
- Return enhanced prompt
- Return explanation text
- Future: PNG/SVG rendering

---

### Module B8: Validation Schema Layer

**Purpose**: Validate all inputs and AI outputs.

**MVP Scope**: ✅ In

**Capabilities**:
- Pydantic models for all request/response types
- Validate AI JSON responses against schema
- Validate Mermaid syntax (basic parsing)
- Reject malformed data before it reaches frontend

---

## Module Dependency Map

```
Landing Page
    ↓
Workspace ──────────────────────────────────────
  │                                              │
  ├── Prompt Input ← → Voice Input              │
  │       ↓                                      │
  │   [Backend: Prompt Enhancement API]          │
  │       ↓                                      │
  ├── Prompt Enhancement Preview                 │
  │       ↓                                      │
  │   [Backend: Diagram Generation API]          │
  │       ↓                                      │
  ├── Diagram Renderer ← → Version History      │
  │       ↓                                      │
  ├── Conversational Refinement Panel            │
  │       ↓                                      │
  │   [Backend: Diagram Refinement API]          │
  │       ↓                                      │
  └── Export                                     │
─────────────────────────────────────────────────
```

---

## Post-MVP Modules

| Module | Reason Deferred |
|--------|-----------------|
| User Authentication | Adds complexity; no persistent storage needed for portfolio |
| Persistent Diagram Library | Requires DB + auth; in-memory sufficient for demo |
| Provider Settings UI | Single provider for MVP; selector useful later |
| Collaborative Editing | Major infrastructure; single-user first |
| Custom Themes/Styling | Default theme sufficient for portfolio |
