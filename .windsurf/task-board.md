# Task Board: AI Design System Diagram Assistant

Organized by status. Tasks derived from updated requirements.

---

## Done

### Phase 1 — Project Setup ✅
### Phase 2 — Backend Core ✅
### Phase 3 — Frontend Workspace Shell ✅
### Phase 4 — AI Prompt Enhancement ✅
### Phase 5 — AI Refinement & Tooltips ✅

---

## Backlog

### Phase 6 — Codebase to Diagram (NEW)

#### **UI / Frontend**
- [x] Define visual styles for themes: Technical, Soft, Colorful, Dark, Enterprise
- [x] Implement Theme Selector in the Style Toolbar
- [x] Update `MermaidRenderer` to apply themes via `classDef` and CSS
- [x] Add transition animations for theme switching
- [x] Implement visual feedback for 'related_files' tooltips
- [x] Final UI/UX polish pass (spacing, typography, loading states)

#### **Backend / API**
- [x] Create GitHub Service for repo tree extraction
- [x] Implement repo tree filtering and key file selection
- [x] Create Codebase Analyzer AI service (summary + tech stack)
- [x] Create Codebase Diagram Prompt Enhancer
- [x] Implement `POST /api/codebase/analyze` endpoint
- [x] Implement `POST /api/codebase/generate-diagram` endpoint
- [x] Update DiagramNode schema to include `related_files`
- [x] Build GitHub URL Input UI in the frontend
- [x] Add mode-switch logic (Prompt vs Codebase)
- [x] Integrate interactive tooltips for repo paths

#### **AI / Prompts**
- [ ] AI-CODE-001: Create Codebase Architecture Analyzer prompt
- [ ] AI-CODE-002: Create Codebase Diagram Prompt Enhancer template
- [ ] AI-CODE-003: Create Codebase-to-Mermaid generator prompt
- [ ] AI-CODE-004: Create Codebase Refinement prompt template
- [ ] AI-CODE-005: Create Codebase Safety/Redaction filter prompt

### Phase 7 — Export, Polish & Final Documentation

- [ ] EXP-002: Implement `.mmd` download (raw Mermaid source)
- [ ] EXP-003: Implement `.json` download (full structured data)
- [ ] UI-POLISH: Final UI/UX pass for portfolio readiness
- [ ] DOC-001: Update README with Codebase-to-Diagram instructions
- [ ] DOC-002: Create Portfolio Case Study (v2 with codebase features)
- [ ] TEST-006: End-to-end testing of GitHub Flow (3 public repos)
- [ ] TEST-007: Node Theme visual validation

---

## In Progress

- [~] ARCH-010: Update architectural documentation for Codebase to Diagram feature

---

## Blocked

_None_

---

## Task Statistics

- **Backlog**: 25 tasks
- **In Progress**: 1
- **Blocked**: 0
- **Done**: 60+

---

## Priority Order (Next Steps)

1. **Input Mode UI**: Switch between Prompt and GitHub input.
2. **GitHub API Integration**: Fetch repo tree and identify key files.
3. **Codebase AI Workflow**: Analysis → Prompt Enhancement → Generation.
4. **Node Themes**: Visual-only customization for Mermaid.
5. **Exports & Final Polish**: MMD/JSON downloads and documentation.
