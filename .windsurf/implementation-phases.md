# Implementation Phases

## Overview

11 phases from architecture finalization to production-ready documentation. Each phase has a single goal, specific tasks, clear exit criteria, and estimated effort.

**Total estimated effort: 45-65 hours**

---

## Phase 0 — Architecture Finalization ✅
## Phase 1 — Project Setup ✅
## Phase 2 — Backend Core ✅
## Phase 3 — Frontend Workspace Shell ✅
## Phase 4 — AI Prompt Enhancement ✅
## Phase 5 — Mermaid Diagram Generation ✅
## Phase 6 — Conversational Refinement ✅
## Phase 7 — Voice Input ✅
## Phase 8 — Export & Polish ✅
## Phase 9 — Testing & Documentation ✅

---

## Phase 10 — Codebase to Diagram (Flow B)

**Goal:** Allow users to generate diagrams from GitHub URLs via automated codebase analysis.

**Tasks:**
- [ ] **GitHub Integration**:
  - Implement `GitHubService` using `httpx`.
  - Fetch recursive file tree (limit depth to 3-5).
  - Filter out non-essential files (.git, node_modules, images, etc.).
  - Select "Important Files" (package.json, tsconfig.json, main entry points).
- [ ] **Codebase Analyzer (AI)**:
  - Create system prompt for architecture analysis.
  - Detect tech stack, major modules, and project type.
  - Generate architecture summary.
- [ ] **Codebase Enhancer (AI)**:
  - Convert analysis summary into structured diagram prompt.
  - Map nodes to actual file paths (`related_files`).
- [ ] **Backend APIs**:
  - Implement `POST /api/codebase/analyze`.
  - Implement `POST /api/codebase/generate-diagram`.
- [ ] **Frontend UI**:
  - Build `InputModeToggle` (Prompt vs GitHub).
  - Build `GitHubInput` with URL validation and type selectors.
  - Update `MermaidRenderer` to handle `related_files` in tooltips.

**Exit Criteria:**
- Public GitHub URL → Diagram in <20s.
- Tooltips link to repo paths.
- Refinement works for codebase-based diagrams.

**Estimated Effort:** 8-10 hours

---

## Phase 11 — Visual Themes & Premium Polish

**Goal:** Implement instant visual theme switching and premium micro-interactions.

**Tasks:**
- [ ] **Node Themes**:
  - Define theme styles: Technical, Soft, Colorful, Dark, Enterprise.
  - Implement instant theme switching via CSS/Mermaid `classDef`.
- [ ] **Style Toolbar (Ribbon)**:
  - Add theme selector to the toolbar.
  - Ensure theme persists across refinements.
- [ ] **Micro-animations**:
  - Add smooth transitions for diagram updates.
  - Add hover effects and animations for tooltips.
- [ ] **Export Improvements**:
  - Implement `.mmd` (Raw Mermaid) and `.json` (Full Data) file downloads.

**Exit Criteria:**
- Theme switching <100ms.
- UI feels premium and "alive".
- All export formats functional.

**Estimated Effort:** 4-6 hours
