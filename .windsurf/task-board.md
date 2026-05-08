# Task Board: AI Design System Diagram Assistant

Organized by status. Tasks derived from updated requirements.

---

## Done

### Phase 0 — Architecture Finalization

- [x] ARCH-001: Finalize application blueprint
- [x] ARCH-002: Finalize tech stack decisions
- [x] ARCH-003: Define module composition
- [x] ARCH-004: Define implementation phases
- [x] ARCH-005: Create phase tracker
- [x] ARCH-006: Review MVP boundaries
- [x] ARCH-007: Confirm provider abstraction
- [x] ARCH-008: Confirm Mermaid-first strategy
- [x] ARCH-009: Confirm future Eraser adapter strategy

### Phase 1 — Project Setup

- [x] SETUP-001: Create monorepo structure (`apps/web`, `apps/api`)
- [x] SETUP-002: Setup Next.js frontend (TypeScript, Tailwind, App Router)
- [x] SETUP-003: Setup FastAPI backend (Pydantic v2, Uvicorn, CORS, health endpoint)
- [x] SETUP-004: Environment configuration (`.env.example` files)
- [x] Landing page (`/`) with project title, description, CTA
- [x] Workspace placeholder (`/workspace`) with split-panel layout
- [x] Backend health test (pytest + TestClient)
- [x] README with setup instructions

### Phase 2 — Backend Core (Mock APIs)

- [x] SCHEMA-001: Define Pydantic models (prompt, diagram, conversation, common)
- [x] SCHEMA-002: Define DiagramProvider interface (ABC with 3 methods)
- [x] SCHEMA-003: Implement MermaidProvider stub with mock Mermaid
- [x] Create ProviderRegistry factory pattern
- [x] ENHANCE-001: Create mock prompt enhancement service
- [x] ENHANCE-003: Implement `POST /api/prompts/enhance` endpoint (mock)
- [x] GEN-004: Implement conversation context service (in-memory)
- [x] GEN-002: Implement `POST /api/diagrams/generate` endpoint (mock)
- [x] REFINE-002: Implement `POST /api/diagrams/refine` endpoint (mock)
- [x] REFINE-003: Implement diagram versioning service (in-memory)
- [x] Create ExportService and `POST /api/diagrams/export` endpoint
- [x] Implement `GET /api/conversations/{id}/versions` endpoint
- [x] Add schema validation tests
- [x] Add endpoint contract tests
- [x] Wire all routes in `app/main.py`

### Phase 3 — Frontend Workspace Shell

- [x] UI-001: Create app layout (landing + workspace routes)
- [x] UI-002: Build landing page with example prompts
- [x] UI-003: Build workspace split layout (40% / 60%)
- [x] UI-004: Build prompt input panel (textarea, type selector, examples)
- [x] UI-005: Enhanced prompt shown in conversation history
- [x] UI-006: Integrate Mermaid.js renderer (dynamic import)
- [x] UI-007: Build conversation history (user/assistant styled)
- [x] UI-008: Build follow-up refinement input
- [x] UI-009: Build version history sidebar
- [x] STATE-001: Loading states (spinner + status text)
- [x] STATE-002: Error states (red banner + message in chat)
- [x] STATE-003: Empty state (diagram panel placeholder)
- [x] EXP-001: Implement export endpoint (mock)
- [x] Install Zustand + TanStack Query
- [x] Create workspace store (Zustand)
- [x] Create API client with typed fetch wrappers
- [x] Wire all components to mock backend APIs
- [x] Frontend builds successfully

### Phase 4 — AI Prompt Enhancement

- [x] ENHANCE-001: Create OpenAI client singleton
- [x] ENHANCE-002: Create prompt enhancement template with system prompt
- [x] ENHANCE-003: Implement real PromptEnhancerService with GPT-4o
- [x] ENHANCE-004: Add retry logic (1 retry on failure)
- [x] ENHANCE-005: Add fallback enhancement for resilience
- [x] TEST-003: Create enhancement service tests (5 tests passing)
- [x] TEST-004: Create example validation test file

---

## Backlog

### Testing

- [ ] TEST-001: Backend schema validation tests
  - Owner skill: QA Engineer
  - Description: Test all Pydantic models with valid/invalid data
  - Acceptance criteria: 100% of models tested; invalid data rejected
  - Dependencies: SCHEMA-001

- [ ] TEST-002: Prompt enhancement quality tests
  - Owner skill: QA Engineer
  - Description: Test 5 example inputs produce sensible enhancements
  - Acceptance criteria: All 5 return valid schema; entities reasonable; type correct
  - Dependencies: ENHANCE-003

- [ ] TEST-003: Diagram generation tests
  - Owner skill: QA Engineer
  - Description: Test generation produces valid Mermaid for each diagram type
  - Acceptance criteria: Mermaid parseable; renders in mermaid.live; 80%+ accuracy
  - Dependencies: GEN-002

- [ ] TEST-004: Refinement consistency tests
  - Owner skill: QA Engineer
  - Description: Test that refinement preserves unchanged elements
  - Acceptance criteria: 3 refinement scenarios tested; original structure preserved
  - Dependencies: REFINE-002

- [ ] TEST-005: Manual QA checklist execution
  - Owner skill: QA Engineer
  - Description: Execute all manual QA scenarios from testing-strategy.md
  - Acceptance criteria: All demo scenarios pass; edge cases documented
  - Dependencies: All implementation tasks

### Documentation

- [ ] DOC-001: Complete README
  - Owner skill: Documentation Engineer
  - Description: Setup instructions, architecture overview, usage guide
  - Acceptance criteria: New contributor can run project in <5 minutes from README alone
  - Dependencies: All implementation complete

- [ ] DOC-002: Portfolio case study
  - Owner skill: Documentation Engineer
  - Description: Problem → approach → architecture → result writeup
  - Acceptance criteria: Suitable for portfolio site; includes screenshots; explains decisions
  - Dependencies: DOC-001

---

## In Progress

- [~] Context and planning files update (this task)

---

## Blocked

_None_

---

## Done

- [x] Initial PRD created (v0.1)
- [x] Initial project context files created
- [x] Requirement redefined to design-system focus

---

### Phase 5 — AI Refinement & Tooltips

- [x] GEN-005: Update prompt enrichment to include DS metadata (tooltips)
- [x] GEN-006: Implement intent classification (PATCH, STYLE, etc.)
- [x] GEN-007: Implement "Minimal Edit" Mermaid patching
- [x] UI-010: Implement Node Tooltip hover component
- [x] UI-011: Implement Diagram Style Toolbar (Ribbon)
- [x] STATE-004: Decouple StyleState from TopologyState
- [x] REFINE-004: Version-aware refinement (preserve topology)
- [x] UI-012: Integrated Voice Input (Web Speech API)
- [x] BACKEND-001: Persistent JSON storage for conversations and versions

---

## Task Statistics

- **Backlog**: 45 tasks
- **In Progress**: 1
- **Blocked**: 0
- **Done**: 52

---

## Priority Order (Start Here)

1. REFINEMENT & TOOLTIPS (New Phase 5)
2. SCHEMA UPDATE (Topology + Metadata + Style)
3. PROMPT UPDATES (Intent + Metadata)
4. UI UPDATES (Tooltip + Toolbar)
5. Export → Voice → Documentation
