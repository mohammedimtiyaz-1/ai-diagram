# Phase Tracker

## Current Phase

Phase 4 — AI Prompt Enhancement

## Overall Status

In Progress

## Phase Progress

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Architecture Finalization | Complete | All docs finalized, stack frozen |
| 1 | Project Setup | Complete | Both frontend and backend running |
| 2 | Backend Core (Mock APIs) | Complete | All schemas, provider abstraction, mock endpoints, tests — 12/12 passing |
| 3 | Frontend Workspace Shell | Complete | Zustand store, API client, components, Mermaid rendering, build passes |
| 4 | AI Prompt Enhancement | Not Started | |
| 5 | Mermaid Diagram Generation | Not Started | |
| 6 | Conversational Refinement | Not Started | |
| 7 | Voice Input | Not Started | |
| 8 | Export & Polish | Not Started | |
| 9 | Testing & Documentation | Not Started | |

## Active Tasks

- [ ] Create OpenAI client singleton (`core/openai_client.py`)
- [ ] Create prompt enhancement template with system prompt and JSON schema
- [ ] Implement real `PromptEnhancerService.enhance()` with OpenAI GPT-4o
- [ ] Add retry logic (1 retry on failure)
- [ ] Validate enhanced output against 5 example inputs
- [ ] Update frontend to display real enhanced prompts

## Completed Tasks

- [x] Initial PRD created
- [x] Requirement redefined to design-system focus
- [x] All context files updated for new direction
- [x] Skills defined (including CI/CD Developer)
- [x] Architecture blueprint finalized
- [x] Tech stack decisions documented
- [x] Module composition defined
- [x] Implementation phases defined
- [x] Phase tracker created
- [x] Next.js frontend initialized (TypeScript, Tailwind, App Router)
- [x] FastAPI backend initialized (Pydantic, Uvicorn, CORS)
- [x] Landing page (`/`) created
- [x] Workspace placeholder (`/workspace`) created
- [x] Health endpoint (`GET /health`) working
- [x] Environment files (`.env.example`) created for both apps
- [x] Backend test for health endpoint
- [x] README updated with setup instructions
- [x] Frontend builds successfully
- [x] Backend health check passes
- [x] Pydantic schemas defined (prompt, diagram, conversation, common)
- [x] DiagramProvider abstract base class created (3 methods)
- [x] MermaidProvider stub implemented with mock Mermaid diagram
- [x] ProviderRegistry factory created
- [x] PromptEnhancerService mock (returns structured enhancement)
- [x] DiagramGeneratorService mock (orchestrates provider + versioning)
- [x] RefinementService mock (orchestrates refinement + new versions)
- [x] ExportService mock (Mermaid, JSON, enhanced-prompt, explanation)
- [x] ConversationService in-memory store
- [x] VersionService in-memory store
- [x] `POST /api/prompts/enhance` endpoint with mock response
- [x] `POST /api/diagrams/generate` endpoint with mock response
- [x] `POST /api/diagrams/refine` endpoint with mock response
- [x] `POST /api/diagrams/export` endpoint with mock response
- [x] `GET /api/conversations/{id}/versions` endpoint
- [x] All 5 API routes wired in main.py
- [x] 12 backend tests passing (schemas + endpoints)
- [x] Zustand installed, workspace store created (`stores/workspace.ts`)
- [x] API client module with typed fetch wrappers for all 5 endpoints (`lib/api.ts`)
- [x] PromptInput component with textarea, diagram type selector, example chips
- [x] ConversationHistory component with user/assistant styled messages
- [x] DiagramPreview component with dynamic Mermaid import + rendering
- [x] FollowUpInput component for refinement
- [x] VersionHistory component showing diagram versions
- [x] Workspace page wired: prompt → enhance API → show enhancement → generate API → render Mermaid
- [x] Refinement flow: follow-up input → refine API → render updated diagram
- [x] Loading states (spinner + status text in header)
- [x] Error states (red banner + message in conversation)
- [x] Landing page updated with example prompts
- [x] Frontend builds successfully with Mermaid client-side rendering

## Decisions Made

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-08 | Product is design-system focused | Clear niche; better portfolio signal than generic tool |
| 2026-05-08 | Prompt enhancement is a first-class feature | Better diagrams; differentiator; shows AI orchestration |
| 2026-05-08 | Diagram provider must be pluggable | Start with Mermaid; allow Eraser/others later |
| 2026-05-08 | Mermaid is MVP provider | Simplest to implement; renderable in browser; exportable |
| 2026-05-08 | Chat-based refinement required | Core UX differentiator; iterative = more useful |
| 2026-05-08 | In-memory context for MVP | No DB needed; sufficient for portfolio demo |
| 2026-05-08 | Voice uses browser Web Speech API | Avoids backend STT complexity |
| 2026-05-08 | Desktop-first responsive (≥1024px) | Diagram work is desktop-centric |
| 2026-05-08 | No authentication for MVP | Reduces complexity; no persistent user data needed |
| 2026-05-08 | Next.js App Router + FastAPI | Modern fullstack; Python for AI; React for UI |
| 2026-05-08 | Zustand + TanStack Query | Zustand for client state; TanStack Query for server state |
| 2026-05-08 | OpenAI GPT-4o | Best structured JSON output; fast; cost-effective |
| 2026-05-08 | Pydantic v2 + Zod | Shared validation mental model; TypeScript inference |

## Open Questions

| Question | Options | Status | Decision Needed By |
|----------|---------|--------|-------------------|
| Should enhanced prompt require manual approval before generation? | Auto-proceed (with preview in chat) | Decided | Shown in conversation history; user can see what was enhanced |
| Should localStorage save diagram history for MVP? | No (in-memory only) | Decided | No persistent storage needed for MVP |
| Which Mermaid renderer package should be used? | `mermaid` npm package directly | Decided | Dynamic import, client-side only, full control over rendering |
| Should refinement auto-enhance follow-up or send raw? | Enhance follow-up (better quality) / Send raw (faster) | Open | Before Phase 6 |
| Context window management: truncate or summarize? | Truncate old messages / AI summarize / Sliding window | Open | Before Phase 6 |

## Next Recommended Action

Start Phase 4 — AI Prompt Enhancement:
1. Create OpenAI client singleton
2. Create prompt enhancement template with system prompt for design-system intent extraction
3. Implement real `PromptEnhancerService.enhance()` using GPT-4o with `response_format: json_object`
4. Add retry and error handling
5. Validate with 5 example inputs

## Time Tracking

| Phase | Estimated | Actual | Variance |
|---|---|---|---|
| 0 | 2-3h | — | — |
| 1 | 2-3h | — | — |
| 2 | 4-5h | — | — |
| 3 | 4-6h | — | — |
| 4 | 3-4h | — | — |
| 5 | 4-5h | — | — |
| 6 | 5-7h | — | — |
| 7 | 2-3h | — | — |
| 8 | 4-6h | — | — |
| 9 | 4-6h | — | — |
| **Total** | **34-48h** | **—** | **—** |
