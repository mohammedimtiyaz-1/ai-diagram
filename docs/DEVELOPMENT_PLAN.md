# Development Plan: AI Design System Diagram Assistant

## Guiding Principles

1. **Build small** — each milestone delivers a working increment
2. **Start with Mermaid** — simplest provider, renders in browser
3. **Prompt enhancement first** — the differentiator, build it early
4. **Chat refinement is core** — not a nice-to-have, implement before polish
5. **Codebase to Diagram** — the advanced "Pro" feature, implement after core refinement
6. **Voice after text** — text flow must be stable first
7. **Polish last** — UI polish happens after features work
8. **Document as portfolio** — README and case study are final deliverables

---

## Phase 1: Foundation (Milestones 1-2) ✅

### Milestone 1: Context & Planning ✅
### Milestone 2: Project Setup ✅

---

## Phase 2: Backend Core (Milestones 3-5) ✅

### Milestone 3: Schemas & Provider Abstraction ✅
### Milestone 4: Prompt Enhancement API ✅
### Milestone 5: Mermaid Provider MVP ✅

---

## Phase 3: Frontend Core (Milestone 6-7) ✅

### Milestone 6: Next.js Workspace UI ✅
### Milestone 7: Diagram Rendering & Enhancement Preview ✅

---

## Phase 4: AI Refinement & Style (Milestones 8-9) ✅

### Milestone 8: Node Tooltips & Metadata Enrichment ✅
### Milestone 9: Incremental Refinement & Version History ✅

---

## Phase 5: Voice & Style Toolbar (Milestones 10-11) ✅

### Milestone 10: Interactive Style Toolbar (Ribbon) ✅
### Milestone 11: Voice Input Integration ✅

---

## Phase 6: Codebase to Diagram (Milestones 12-14) 🆕

### Milestone 12: Codebase Input UI
**Owner**: Frontend Developer
**Estimated effort**: 3-4 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Input Mode Toggle | Switch between Prompt and GitHub modes | State updates correctly |
| GitHub URL Input | Validated input field for GitHub URLs | Rejects non-GitHub links |
| Diagram Type Selector | Dropdown with specific codebase types | Options from requirements |
| Node Theme Selector | Dropdown for visual themes | Options from requirements |
| Codebase Input Component | Integrated UI for Flow B | Replaces PromptInput when toggled |

**Risks**: UI becoming cluttered
**Mitigation**: Use tabs or a clean toggle; keep settings compact

### Milestone 13: Codebase Analysis Backend
**Owner**: Architect + Backend Developer
**Estimated effort**: 5-6 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| GitHub Parser | Extract owner/repo; validate public access | Correctly identifies repo |
| Tree Fetcher | Fetch recursive file tree via GitHub API | Tree returned with filtering |
| File Selector | Identify key files (package.json, tsconfig) | Entry points detected |
| Analyzer Service | AI call to summarize repo architecture | Returns stack + summary |
| Enhancer Service | Convert analysis to diagram prompt | Returns high-quality prompt |
| API Endpoints | `/api/codebase/analyze` & `/api/codebase/generate` | Both return valid schemas |

**Risks**: GitHub rate limits; repo too large
**Mitigation**: Proxied requests; recursive tree limit (3 levels); skip binary/large files

### Milestone 14: Codebase Diagram Generation
**Owner**: AI Workflow Engineer + Backend Developer
**Estimated effort**: 4-5 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Node Theme Logic | Implement classDef/style mapping in Mermaid | Themes apply correctly |
| Related Files Metadata | Map nodes to actual codebase paths | Tooltips show file paths |
| Codebase Refinement | Support follow-up chat for codebase diagrams | Incremental logic works |
| Tests | End-to-end codebase flow tests | 3 public repos test pass |

---

## Phase 7: Export & Final Polish (Milestones 15-16)

### Milestone 15: Persistence & Exports
**Owner**: Backend + Frontend Developer
**Estimated effort**: 3-4 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Backend Persistence | File-backed JSON store for conversations | Persists across restarts |
| Mermaid MMD Export | Download raw Mermaid file | `.mmd` download works |
| JSON Export | Download structured diagram data | `.json` download works |

### Milestone 16: Final QA & Portfolio
**Owner**: QA + All Developers
**Estimated effort**: 4-5 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Cross-browser testing | Chrome, Safari, Firefox | Responsive and functional |
| Performance audit | Optimize Mermaid rendering & API calls | UI feels snappy |
| Portfolio Docs | Update README, screenshots, and case study | Professional presentation |

---

## Total Estimated Effort (Updated)

| Phase | Estimated Hours |
|-------|-----------------|
| Phases 1-5 (Core) | ~30 hours (Done) |
| Phase 6 (Codebase) | 12-15 hours |
| Phase 7 (Polish) | 7-9 hours |
| **Total** | **49-54 hours** |

---

## Scope Control Rules (Updated)

1. **Public GitHub only** — no private repo support in MVP.
2. **Read-only analysis** — do not attempt to modify repo code.
3. **Selective reading** — limit total files read to avoid token overflow.
4. **Visual Themes first** — implement theme mapping via CSS/Mermaid before AI.
