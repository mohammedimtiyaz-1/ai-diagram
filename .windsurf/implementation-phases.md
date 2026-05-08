# Implementation Phases

## Overview

10 phases from architecture finalization to production-ready documentation. Each phase has a single goal, specific tasks, clear exit criteria, and estimated effort. Phases are sequential where noted, parallel where possible.

**Total estimated effort: 35-50 hours**

---

## Phase 0 — Architecture Finalization

**Goal:** Finalize all technical documentation before writing code.

**Status:** In Progress

**Tasks:**
- [ ] Review all existing `.windsurf/` and `docs/` files for consistency
- [ ] Finalize tech stack (`tech-stack-decisions.md`)
- [ ] Complete application blueprint (`architecture-blueprint.md`)
- [ ] Define module composition (`module-composition.md`)
- [ ] Define implementation phases (`implementation-phases.md`)
- [ ] Create phase tracker (`phase-tracker.md`)
- [ ] Review MVP boundaries — confirm what is in/out
- [ ] Confirm provider abstraction design
- [ ] Confirm Mermaid-first strategy
- [ ] Confirm future Eraser adapter strategy
- [ ] Resolve open questions from `progress-tracker.md`

**Exit Criteria:**
- All 5 new architecture documents are complete and consistent
- Tech stack is frozen for MVP
- MVP scope is clearly bounded
- No outstanding architectural questions
- Ready to begin Phase 1

**Estimated Effort:** 2-3 hours (mostly documentation)

---

## Phase 1 — Project Setup

**Goal:** Create the project skeleton. Both frontend and backend run locally.

**Status:** Not Started
**Depends On:** Phase 0

**Tasks:**
- [ ] Create monorepo root with `frontend/` and `backend/` directories
- [ ] Initialize Next.js 14+ App Router in `frontend/`
  - TypeScript, Tailwind CSS, shadcn/ui
  - Strict TypeScript config
  - ESLint + Prettier config
- [ ] Initialize FastAPI project in `backend/`
  - Python 3.11+, Pydantic v2
  - Uvicorn, httpx
  - Ruff config
  - pytest + pytest-asyncio
- [ ] Create `.env.example` with all required variables
- [ ] Create `Makefile` with `dev`, `install`, `test`, `lint`, `format` targets
- [ ] Create basic `README.md` with setup instructions
- [ ] Add `.gitignore` for both frontend and backend
- [ ] Verify `make dev` starts both services
- [ ] Verify frontend renders at `localhost:3000`
- [ ] Verify backend health endpoint at `localhost:8000/health`

**Exit Criteria:**
- `make dev` starts both frontend and backend in one command
- Frontend shows default Next.js page
- Backend `GET /health` returns `{"status": "healthy"}`
- No lint/type errors in either project
- README explains how to run the project

**Estimated Effort:** 2-3 hours

---

## Phase 2 — Backend Core (Mock APIs)

**Goal:** Build API contracts with mock responses. Frontend can integrate immediately.

**Status:** Not Started
**Depends On:** Phase 1

**Tasks:**
- [ ] Define Pydantic schemas (`schemas/prompt.py`, `schemas/diagram.py`, `schemas/conversation.py`)
  - EnhanceRequest, EnhancementResult
  - GenerateRequest, DiagramResult, DiagramVersion
  - RefineRequest
  - ExportRequest, ExportResult
  - ErrorResponse
- [ ] Create `DiagramProvider` abstract base class (`providers/base.py`)
- [ ] Create `MermaidProvider` stub (`providers/mermaid.py`) — returns hardcoded Mermaid
- [ ] Create `ProviderRegistry` (`providers/registry.py`) — factory pattern
- [ ] Implement `POST /api/prompts/enhance` — returns mock EnhancementResult
- [ ] Implement `POST /api/diagrams/generate` — returns mock DiagramResult
- [ ] Implement `POST /api/diagrams/refine` — returns mock DiagramResult
- [ ] Implement `POST /api/diagrams/export` — returns mock ExportResult
- [ ] Implement `GET /api/conversations/{id}/versions` — returns mock version list
- [ ] Add CORS middleware for frontend origin
- [ ] Write schema validation tests
- [ ] Write endpoint contract tests (request/response shapes)

**Exit Criteria:**
- All 5 API endpoints return correct JSON shapes
- Pydantic validates all request/response schemas
- Tests pass for schema validation
- Frontend can call all endpoints and get mock data
- Provider abstraction is real (MermaidProvider implements interface)

**Estimated Effort:** 4-5 hours

---

## Phase 3 — Frontend Workspace Shell

**Goal:** Build the UI structure. User can navigate landing → workspace → input → see mock responses.

**Status:** Not Started
**Depends On:** Phase 1 (can parallel with Phase 2)

**Tasks:**
- [ ] Create landing page (`/`)
  - Hero section with product title + tagline
  - 3-5 example prompts (design-system specific)
  - CTA button to workspace
- [ ] Create workspace page (`/workspace`)
  - Split-panel layout (left ~40%, right ~60%)
  - Responsive: stack on mobile, hide diagram on small screens
- [ ] Create `WorkspaceShell` component
- [ ] Create `ChatPanel` component
  - `PromptInput`: textarea, diagram type selector, submit button
  - `ExamplePrompts`: clickable chips that populate textarea
- [ ] Create `DiagramPanel` component
  - Empty state with illustration + guidance
  - Placeholder for diagram rendering
- [ ] Create Zustand stores (`useConversationStore`, `useDiagramStore`, `useWorkspaceStore`)
- [ ] Create API client functions (fetch wrappers for all endpoints)
- [ ] Wire PromptInput → POST /api/prompts/enhance → show mock enhanced prompt
- [ ] Wire enhanced prompt → POST /api/diagrams/generate → show mock diagram
- [ ] Add loading states (spinners, disabled inputs)
- [ ] Add error states (human-readable messages)
- [ ] Add basic styling with Tailwind + shadcn/ui

**Exit Criteria:**
- User can navigate from landing to workspace
- User can type prompt, submit, see mock enhanced prompt
- User can generate mock diagram
- Loading and error states work
- UI is responsive and styled

**Estimated Effort:** 4-6 hours

---

## Phase 4 — AI Prompt Enhancement

**Goal:** Implement real AI prompt enhancement. Raw prompts become structured, useful enhanced prompts.

**Status:** Not Started
**Depends On:** Phase 2

**Tasks:**
- [ ] Create OpenAI client singleton (`core/openai_client.py`)
- [ ] Create prompt enhancement template (`prompts/enhancement.py`)
  - System prompt for design-system intent extraction
  - Instructions for entity extraction, relationship mapping, type classification
  - JSON output schema specification
- [ ] Implement `PromptEnhancerService.enhance()`
  - Build prompt from template + user input
  - Call OpenAI with `response_format: { type: "json_object" }`
  - Parse JSON into EnhancementResult
  - Handle errors (timeout, invalid JSON)
- [ ] Implement retry logic (1 retry on failure)
- [ ] Implement repair prompt (send error details to AI for fix)
- [ ] Validate enhanced output quality against 5 example inputs
- [ ] Replace mock `POST /api/prompts/enhance` with real implementation
- [ ] Test with real OpenAI API calls
- [ ] Verify enhanced prompts are meaningfully better than raw input

**Exit Criteria:**
- 5 example inputs produce useful enhanced prompts
- Entities and relationships are extracted correctly
- Diagram type classification is accurate (≥80%)
- Errors are handled gracefully (retry + fallback)
- Frontend shows real enhanced prompt in preview

**Estimated Effort:** 3-4 hours

---

## Phase 5 — Mermaid Diagram Generation

**Goal:** Generate real Mermaid diagrams from enhanced prompts via AI.

**Status:** Not Started
**Depends On:** Phase 4

**Tasks:**
- [ ] Create diagram-type-specific prompt templates (`prompts/generation/`)
  - `architecture.py` — layered design system architecture
  - `hierarchy.py` — component hierarchy/tree
  - `token.py` — token pipeline/flow
  - `workflow.py` — design-to-code workflow
- [ ] Implement `MermaidProvider.generate_diagram()`
  - Select template based on diagram_type
  - Build full prompt (system + template + enhanced_prompt)
  - Call OpenAI with JSON output mode
  - Parse response: title, mermaid_source, explanation
  - Validate basic Mermaid syntax (has nodes, has connections)
- [ ] Implement retry + repair for invalid Mermaid
- [ ] Replace mock `POST /api/diagrams/generate` with real implementation
- [ ] Test generation with all 4 diagram types
- [ ] Verify Mermaid renders correctly in Mermaid.js live editor
- [ ] Verify diagrams are relevant to input (≥80% accuracy)

**Exit Criteria:**
- All 4 diagram types generate valid Mermaid
- Mermaid syntax is parseable and renderable
- Diagrams are relevant to design-system input
- Retry/repair handles invalid output
- Frontend renders real diagram in preview panel

**Estimated Effort:** 4-5 hours

---

## Phase 6 — Conversational Refinement

**Goal:** Allow users to chat with the diagram, refining it iteratively. Track versions.

**Status:** Not Started
**Depends On:** Phase 5

**Tasks:**
- [ ] Implement in-memory `ConversationService`
  - Create conversation
  - Get conversation by ID
  - Add messages
  - Get message history
- [ ] Implement in-memory `VersionService`
  - Create version (auto-increment)
  - Get version by ID
  - List versions for conversation
  - Get current version
- [ ] Create refinement prompt template (`prompts/refinement.py`)
  - Include current diagram source
  - Include conversation context
  - Instruction to preserve unchanged elements
  - Request changes_summary
- [ ] Implement `RefinementService.refine()`
  - Load conversation + current diagram
  - Enhance follow-up (optional, in context)
  - Call MermaidProvider.refine()
  - Create new version
  - Return updated diagram
- [ ] Implement context summarization for long conversations (>5 messages)
- [ ] Replace mock `POST /api/diagrams/refine` with real implementation
- [ ] Implement `GET /api/conversations/{id}/versions` with real data
- [ ] Frontend: Create `ConversationHistory` component
  - Display user + assistant messages
  - Show follow-up input below history
- [ ] Frontend: Create `FollowUpInput` component
  - Textarea + send button
  - Disabled during refinement
- [ ] Frontend: Create `VersionHistory` sidebar
  - List versions with numbers + timestamps
  - Show changes_summary per version
  - Click to switch version
- [ ] Frontend: Wire refinement flow end-to-end

**Exit Criteria:**
- User can send follow-up message
- System generates updated diagram
- New version is created and visible
- Original diagram structure is preserved unless explicitly changed
- Version switching works
- Context is maintained across multiple refinements

**Estimated Effort:** 5-7 hours

---

## Phase 7 — Voice Input

**Goal:** Add browser-based speech-to-text input.

**Status:** Not Started
**Depends On:** Phase 3 (can parallel with Phases 4-6)

**Tasks:**
- [ ] Create `VoiceInput` component
  - Mic button with visual recording state
  - Browser SpeechRecognition API integration
  - Feature detection (hide on unsupported browsers)
- [ ] Implement recording start/stop
  - `recognition.start()` on mic click
  - `recognition.stop()` on second click or auto-stop
  - Visual feedback (pulsing icon, timer)
- [ ] Implement transcript preview
  - Editable textarea with transcript
  - Confirm button → sends to enhancement flow
  - Cancel button → clears transcript
- [ ] Handle permission denied gracefully
  - Show message: "Microphone access required for voice input"
  - Fallback to text input
- [ ] Handle browser incompatibility
  - Safari/Firefox: hide mic button, show tooltip
- [ ] Wire voice input to same flow as text input
  - Confirmed transcript = raw_prompt
  - Follows exact same enhancement → generation pipeline

**Exit Criteria:**
- Mic button visible in Chrome/Edge
- Recording works, transcript appears
- Transcript is editable before confirm
- Confirmed transcript generates diagram via same flow as text
- Graceful fallback on unsupported browsers

**Estimated Effort:** 2-3 hours

---

## Phase 8 — Export & Polish

**Goal:** Make the project portfolio-ready. Export, UI polish, responsive design.

**Status:** Not Started
**Depends On:** Phase 5-6

**Tasks:**
- [ ] Implement `ExportService` (`services/export_service.py`)
  - Format Mermaid syntax
  - Format JSON (full diagram data)
  - Format enhanced prompt
  - Format explanation
- [ ] Implement `POST /api/diagrams/export` with real formatting
- [ ] Create `ExportPanel` component
  - 4 export buttons (Mermaid, JSON, Prompt, Explanation)
  - One-click copy to clipboard
  - Toast notification on copy
- [ ] Add empty state illustrations
  - Workspace before first diagram
  - Friendly, on-brand illustration
- [ ] Add loading skeletons
  - ChatPanel during enhancement
  - DiagramPanel during generation
- [ ] Add error state illustrations + actionable messages
- [ ] Improve responsive design
  - Mobile: stack panels, collapsible chat
  - Tablet: adjust split ratio
  - Desktop: 40/60 split
- [ ] Add transitions and micro-interactions
  - Panel switch animations
  - Message appearance animations
  - Version change transitions
- [ ] Polish landing page
  - Professional hero design
  - Feature cards with icons
  - Example prompts with hover effects
- [ ] Add favicon, metadata, Open Graph tags

**Exit Criteria:**
- All 4 export formats work
- UI feels polished and professional
- Responsive on desktop, tablet, mobile
- Empty/loading/error states are delightful
- Landing page is portfolio-worthy

**Estimated Effort:** 4-6 hours

---

## Phase 9 — Testing & Documentation

**Goal:** Production-quality finish. Tests, README, portfolio case study.

**Status:** Not Started
**Depends On:** Phase 8

**Tasks:**
- [ ] Backend unit tests
  - Schema validation tests (all Pydantic models)
  - Service tests with mocked OpenAI client
  - Provider tests (MermaidProvider)
  - Endpoint tests (all 5 endpoints)
- [ ] Frontend component tests
  - PromptInput validation
  - EnhancedPromptPreview rendering
  - DiagramPreview rendering (mock Mermaid)
  - ExportPanel button interactions
- [ ] AI quality tests
  - 5 example inputs → enhancement quality check
  - 4 diagram types → generation quality check
  - 3 refinement scenarios → consistency check
- [ ] Manual QA checklist
  - All demo scenarios from PRD
  - Edge cases (empty input, very long input, invalid input)
  - Browser compatibility (Chrome, Edge, Safari, Firefox)
  - Responsive breakpoints
- [ ] Complete README.md
  - Problem statement
  - Architecture overview
  - Setup instructions (<5 min)
  - Tech stack
  - Screenshots/GIFs
  - API overview
  - Deployment notes
- [ ] Portfolio case study
  - Problem → Approach → Architecture → Result
  - Technical decisions explained
  - Screenshots
  - Link to live demo
- [ ] Final architecture docs update
  - Update `architecture.md` with final state
  - Update `API_CONTRACTS.md` with any changes
  - Update `AI_WORKFLOW_DESIGN.md` with final prompts

**Exit Criteria:**
- All critical paths have tests
- Manual QA checklist passes
- README enables setup in <5 minutes
- Portfolio case study is presentation-ready
- All docs reflect final implementation

**Estimated Effort:** 4-6 hours

---

## Phase Dependencies

```
Phase 0 (Architecture)
    │
    ▼
Phase 1 (Project Setup)
    │
    ├──► Phase 2 (Backend Core) ──┐
    │                              │
    └──► Phase 3 (Frontend Shell)─┘
                   │
                   ▼
            Phase 4 (AI Enhancement)
                   │
                   ▼
            Phase 5 (Mermaid Generation)
                   │
                   ▼
            Phase 6 (Refinement)
                   │
            Phase 7 (Voice) ────────┘ (can run parallel with 4-6)
                   │
                   ▼
            Phase 8 (Export & Polish)
                   │
                   ▼
            Phase 9 (Testing & Docs)
```

**Parallelization opportunities:**
- Phase 2 and Phase 3 can run in parallel after Phase 1
- Phase 7 (Voice) can run in parallel with Phases 4-6 after Phase 3

---

## Risk Mitigation by Phase

| Phase | Risk | Mitigation |
|-------|------|------------|
| 0 | Scope creep in architecture | Strict MVP boundary checklist |
| 1 | Setup issues (Node/Python versions) | Document exact versions, use package managers |
| 2 | Schema design errors | Test schemas with real example data immediately |
| 3 | Mermaid.js SSR issues | Dynamic import with `ssr: false` |
| 4 | AI enhancement quality poor | Test with 5 real examples before integration |
| 5 | Invalid Mermaid output | Build repair prompt, validate syntax before returning |
| 6 | Context drift in refinement | Always include current diagram source in prompt |
| 7 | Browser Speech API inconsistency | Feature detection, graceful fallback |
| 8 | Polish takes too long | Define "good enough" criteria, timebox |
| 9 | Tests reveal major bugs | Reserve buffer time, prioritize critical path tests |
