# Implementation Plan: AI Design System Diagram Assistant

---

## Milestone 1: Context and Planning ✅
## Milestone 2: Project Setup ✅
## Milestone 3: Backend Schemas and Provider Abstraction ✅
## Milestone 4: Prompt Enhancement API ✅
## Milestone 5: Mermaid Diagram Provider (MVP) ✅
## Milestone 6: Next.js Workspace UI ✅
## Milestone 7: Diagram Rendering ✅
## Milestone 8: Conversational Refinement ✅
## Milestone 9: Voice Input ✅
## Milestone 10: Export and Version History ✅
## Milestone 11: Testing and Polish ✅

---

## Milestone 13: Codebase to Diagram (NEW)

**Owner**: Backend Developer + AI Workflow Engineer
**Dependencies**: Milestone 11

**Tasks**:
- [ ] Create GitHub Service for repo tree extraction
- [ ] Implement repo tree filtering and key file selection
- [ ] Create Codebase Analyzer AI service (summary + tech stack)
- [ ] Create Codebase Diagram Prompt Enhancer
- [ ] Implement `POST /api/codebase/analyze` endpoint
- [ ] Implement `POST /api/codebase/generate-diagram` endpoint
- [ ] Update DiagramNode schema to include `related_files`
- [ ] Build GitHub URL Input UI in the frontend
- [ ] Add mode-switch logic (Prompt vs Codebase)
- [ ] Integrate interactive tooltips for repo paths

**Acceptance Criteria**:
- Public GitHub URL → Architecture Diagram in <20s
- Tech stack detected correctly for React/Next.js/FastAPI projects
- Tooltips show actual file paths from the repository
- Incremental refinement works for codebase-based diagrams

---

## Milestone 14: Node Themes & Visual Polish (NEW)

**Owner**: Frontend Developer
**Dependencies**: Milestone 7

**Tasks**:
- [ ] Define visual styles for themes: Technical, Soft, Colorful, Dark, Enterprise
- [ ] Implement Theme Selector in the Style Toolbar
- [ ] Update `MermaidRenderer` to apply themes via `classDef` and CSS
- [ ] Add transition animations for theme switching
- [ ] Implement visual feedback for 'related_files' tooltips (e.g. icon indicators)
- [ ] Final UI/UX polish pass (spacing, typography, loading states)

**Acceptance Criteria**:
- Theme switching is instantaneous (no AI call)
- Themes accurately reflect requested aesthetics
- UI feels "premium" and "alive" with micro-animations

---

## Milestone 12: Documentation and Portfolio (Updated)

**Owner**: Documentation Engineer
**Dependencies**: Milestone 14

**Tasks**:
- [ ] Complete README with Codebase Flow instructions
- [ ] Write portfolio case study (including Flow B and Themes)
- [ ] Document the dual-flow AI architecture
- [ ] Add high-quality screenshots and demo videos
- [ ] Final review of all docs for consistency
