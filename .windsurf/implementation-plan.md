# Implementation Plan: AI Design System Diagram Assistant

---

## Milestone 1: Context and Planning

**Owner**: Project Manager
**Status**: In Progress

**Tasks**:
- [x] Define updated product requirements
- [x] Define architecture
- [x] Define modules and workflows
- [x] Create task board
- [ ] Resolve open questions

**Acceptance Criteria**:
- All `.windsurf/` and `docs/` files reflect new direction
- Open questions resolved before implementation

---

## Milestone 2: Project Setup

**Owner**: Architect + Developers
**Dependencies**: Milestone 1

**Tasks**:
- Create monorepo structure (`/frontend`, `/backend`)
- Setup Next.js App Router project
- Setup FastAPI project
- Setup environment variables (`.env.example`)
- Setup linting/formatting (ESLint, Prettier, Ruff)
- Create Makefile or scripts for local dev
- Create basic README

**Acceptance Criteria**:
- `make dev` (or equivalent) starts both frontend and backend
- Both services respond to health checks
- CI-ready project structure

---

## Milestone 3: Backend Schemas and Provider Abstraction

**Owner**: Backend Developer + Architect
**Dependencies**: Milestone 2

**Tasks**:
- Define Pydantic models (Conversation, DiagramVersion, Message, etc.)
- Define DiagramProvider abstract interface
- Implement MermaidProvider stub (returns mock Mermaid)
- Create request/response schemas for all endpoints
- Setup validation layer

**Acceptance Criteria**:
- All Pydantic models pass validation tests
- Provider interface is defined and documented
- Mock MermaidProvider returns valid mock response

---

## Milestone 4: Prompt Enhancement API

**Owner**: AI Workflow Engineer + Backend Developer
**Dependencies**: Milestone 3

**Tasks**:
- Create prompt enhancement service
- Create design-system prompt template
- Implement `/api/prompts/enhance` endpoint
- Add entity extraction logic
- Add diagram type classification
- Add assumption flagging
- Write tests for enhancement quality

**Acceptance Criteria**:
- Raw prompt → enhanced prompt with entities, type, structure
- Enhancement works for all 5 example inputs from PRD
- Invalid/short inputs return helpful errors

---

## Milestone 5: Mermaid Diagram Provider (MVP)

**Owner**: AI Workflow Engineer + Backend Developer
**Dependencies**: Milestone 4

**Tasks**:
- Implement MermaidProvider (calls OpenAI, returns Mermaid syntax)
- Create Mermaid generation prompt template
- Implement `/api/diagrams/generate` endpoint
- Add Mermaid syntax validation
- Add retry on failure
- Return diagram with explanation

**Acceptance Criteria**:
- Enhanced prompt → valid Mermaid diagram
- Mermaid renders correctly in standard Mermaid tools
- At least 3 design-system diagram types generated successfully
- Retry works on AI failure

---

## Milestone 6: Next.js Workspace UI

**Owner**: Frontend Developer
**Dependencies**: Milestone 2

**Tasks**:
- Create app layout (landing + workspace)
- Build landing page (hero, examples, CTA)
- Build workspace split layout (chat left, diagram right)
- Build chat input panel (textarea, type selector, submit)
- Add example prompts interaction
- Build loading/error/empty states
- Connect to backend APIs

**Acceptance Criteria**:
- Landing page explains product clearly
- Workspace renders with split layout
- Input form validates and submits
- Loading state shown during API calls
- Error state shown on failure

---

## Milestone 7: Diagram Rendering

**Owner**: Frontend Developer
**Dependencies**: Milestone 5, Milestone 6

**Tasks**:
- Integrate Mermaid.js renderer
- Display diagram from API response
- Show diagram title and explanation
- Add enhanced prompt preview (raw vs enhanced)
- Add zoom/pan controls if needed
- Handle rendering errors gracefully

**Acceptance Criteria**:
- Generated Mermaid renders in UI
- Title and explanation displayed
- Enhanced prompt visible and copyable
- Invalid Mermaid shows error, not crash

---

## Milestone 8: Conversational Refinement

**Owner**: AI Workflow Engineer + Backend + Frontend
**Dependencies**: Milestone 7

**Tasks**:
- Implement conversation context service (in-memory)
- Implement `/api/diagrams/refine` endpoint
- Create refinement prompt template
- Build follow-up input in frontend
- Show conversation history
- Track and display diagram versions
- Allow version comparison (basic)

**Acceptance Criteria**:
- Follow-up modifies existing diagram
- Context preserved across messages
- Version history shows all iterations
- At least 3 refinement scenarios work correctly

---

## Milestone 9: Voice Input

**Owner**: Frontend Developer
**Dependencies**: Milestone 6

**Tasks**:
- Implement Web Speech API integration
- Build mic button with recording state
- Build transcript preview/edit UI
- Connect confirmed transcript to generation flow
- Handle unsupported browser gracefully

**Acceptance Criteria**:
- Voice records and transcribes in Chrome/Edge
- Transcript editable before submission
- Unsupported browsers see graceful fallback
- Transcript flows through normal generation pipeline

---

## Milestone 10: Export and Version History

**Owner**: Frontend + Backend Developer
**Dependencies**: Milestone 8

**Tasks**:
- Implement export endpoint (Mermaid, JSON, prompt, explanation)
- Build export panel in UI
- Add copy-to-clipboard actions
- Build version history sidebar
- Allow restoring previous version

**Acceptance Criteria**:
- All export formats work correctly
- Copy gives visual feedback
- Version history lists all diagram versions
- Restore replaces current diagram with selected version

---

## Milestone 11: Testing and Polish

**Owner**: QA Engineer + All Developers
**Dependencies**: Milestones 5-10

**Tasks**:
- Backend unit tests (schemas, enhancement, generation, refinement)
- Frontend component tests (input, renderer, export)
- AI output quality tests (5 demo scenarios)
- Manual QA checklist execution
- UI polish (spacing, responsiveness, transitions)
- Error message review
- Performance check (<10s generation)

**Acceptance Criteria**:
- All critical paths have tests
- Demo scenarios pass at ≥80% accuracy
- No crashes on edge cases
- UI looks portfolio-ready

---

## Milestone 12: Documentation and Portfolio

**Owner**: Documentation Engineer
**Dependencies**: Milestone 11

**Tasks**:
- Complete README (setup, usage, architecture overview)
- Write portfolio case study (problem, approach, result)
- Document AI workflow with diagrams
- Document provider extension strategy
- Add screenshots/demo GIF
- Final review of all docs

**Acceptance Criteria**:
- README enables someone to run the project in <5 minutes
- Case study is presentation-ready
- Architecture and AI workflow documented visually
- All docs reflect final state
