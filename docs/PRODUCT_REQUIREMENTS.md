# Product Requirements Document: AI Design System Diagram Assistant

## 1. Problem Statement

### The Problem

Design system teams — frontend engineers, UI architects, and design operations professionals — spend significant time communicating architecture decisions visually. They need diagrams showing component hierarchies, token pipelines, theme structures, and design-to-code workflows. Creating these diagrams is:

1. **Time-consuming**: Drawing design-system architecture diagrams manually takes 30-60 minutes
2. **Iterative**: Design systems evolve constantly; diagrams become outdated
3. **Hard to start**: Most people have a rough idea but struggle to structure it visually
4. **Tool-heavy**: Traditional tools require learning complex UIs for one-off diagrams
5. **Disconnected from thinking**: The gap between "I know how this should work" and "here's a clear visual" is large

### What This Product Solves

AI Design System Diagram Assistant lets users describe their design system ideas in plain English (or voice), enhances their raw thinking into a structured diagram prompt, generates a professional diagram, and then allows iterative refinement through conversation.

### Why This Matters as a Portfolio Project

Demonstrates:
- **AI orchestration**: Prompt enhancement + generation + refinement pipeline
- **Product thinking**: Niche focus on design-system domain (not generic)
- **Full-stack architecture**: Next.js + FastAPI + AI integration
- **UX design**: Chat-based interface with transparent AI and iterative refinement
- **Software architecture**: Provider abstraction, clean module boundaries, extensibility
- **Domain expertise**: Understanding of design systems, tokens, components, themes

---

## 2. Target Users

### Primary: Frontend & Design System Engineers
**Profile**: Engineers building, maintaining, or scaling design systems
**Goals**:
- Visualize component architecture and token pipelines
- Document design system structure for team alignment
- Iterate on architecture as the system evolves

**Pain points**:
- Hard to communicate design system structure visually
- Diagrams become outdated as tokens and components evolve
- Starting from scratch when planning new design system layers

### Secondary: UI Architects & Technical Leads
**Profile**: Senior engineers making architectural decisions for UI platforms
**Goals**:
- Plan scalable component hierarchies before implementation
- Communicate architecture decisions to team
- Document design-to-code workflows

**Pain points**:
- Architecture diagrams take too long to create
- Want version-control-friendly formats (Mermaid)
- Need to iterate quickly when presenting options

### Tertiary: Design Operations & Product Engineers
**Profile**: Teams managing design system governance, documentation, tooling
**Goals**:
- Map governance workflows (Figma → tokens → code → deployment)
- Document component dependencies for impact analysis
- Plan design system roadmap visually

**Pain points**:
- Cross-functional workflows are hard to diagram
- Need diagrams that non-engineers can understand
- Want to update diagrams conversationally, not redraw

---

## 3. Core User Journey

```
1. User enters text or voice input about a design system idea
2. System analyzes and enhances the raw prompt (AI)
3. User optionally reviews the enhanced prompt
4. System generates a design-system-focused diagram
5. Diagram is displayed in the UI
6. User can continue chatting to refine the diagram
7. System maintains context and creates new diagram versions
8. User exports the final diagram (Mermaid, JSON, or prompt)
```

---

## 4. MVP Feature List

### In Scope (MVP)

| Feature | Description | User Value |
|---------|-------------|------------|
| Text input | Type design-system description | Core entry point |
| Prompt enhancement | AI rewrites raw input into structured diagram prompt | Better diagrams; transparency |
| Enhanced prompt preview | Show what AI understood before generation | Trust and control |
| Diagram generation (Mermaid) | Generate Mermaid diagram via pluggable provider | Visual output |
| Diagram display | Render Mermaid in UI with title/explanation | See the result |
| **Incremental Refinement** | Follow-up messages modify existing diagram without full redraw | Faster iteration; stability |
| **Node Hover Tooltips** | Show metadata popovers on node hover | Contextual information |
| **Diagram Style Toolbar** | Ribbon to customize font and color without AI call | Visual personalization |
| Diagram version history | Track versions within conversation | Undo/compare |
| Voice input | Browser speech-to-text for hands-free input | Accessibility |
| Export (Mermaid, JSON, prompt) | Copy diagram in multiple formats | Reusability |
| Example prompts | Design-system-specific examples | Guidance |
| Loading/error/empty states | Feedback at every step | Professional UX |
| Landing page | Product explanation + CTA | Entry point |

### Out of Scope (Post-MVP / Non-Goals)

| Feature | Rationale |
|---------|-----------|
| Full Figma replacement | Not a design tool; generates diagrams only |
| Full Eraser clone | Use Eraser as future provider, not replicate it |
| Complex collaborative whiteboard | Single-user sufficient for portfolio |
| Enterprise auth (SSO, RBAC) | No persistent user data needed |
| Real-time multiplayer | Major infrastructure; out of scope |
| Full design token management | Not a token tool; visualizes token architecture |
| PNG/SVG export | Future enhancement; Mermaid sufficient for MVP |
| Database persistence | In-memory sufficient; localStorage optional |
| Mobile-native app | Desktop-first for diagram work |
| Custom diagram themes (per-node) | Only global style toolbar for MVP |
| Multiple AI model selection | Single model per task (gpt-4o-mini for speed) |

---

## 5. User Stories

### Input & Enhancement Stories

**US-INP-01: Text Input**
> As a design system engineer, I can type a rough description of my design system idea so I can get it visualized.

**Acceptance Criteria**:
- Input accepts 10-2000 characters
- Diagram type selector (Auto/Architecture/Hierarchy/Token/Workflow)
- Submit triggers prompt enhancement → generation pipeline
- Example prompts available to click

**US-INP-02: Voice Input**
> As a user, I can describe my design system idea verbally for hands-free input.

**Acceptance Criteria**:
- Mic button starts/stops recording
- Browser permission handled gracefully
- Transcript shown in editable textarea
- Confirm sends transcript to enhancement pipeline

**US-INP-03: Prompt Enhancement Preview**
> As a user, I can see how the AI enhanced my prompt so I understand what will be generated.

**Acceptance Criteria**:
- Raw prompt shown alongside enhanced version
- Extracted entities and assumptions visible
- Copy enhanced prompt button available
- Generation proceeds after enhancement

### Generation & Display Stories

**US-GEN-01: Diagram Generation**
> As a user, after my prompt is enhanced, I receive a design-system diagram.

**Acceptance Criteria**:
- Diagram generates within 10 seconds
- Mermaid diagram rendered in preview panel
- Title and explanation displayed
- Every node includes tooltip metadata (title, description, role)

**US-GEN-02: Node Hover Tooltips**
> As a user, I can hover over any node in the diagram to see more details about it.

**Acceptance Criteria**:
- Clean tooltip appears on hover
- Content is context-specific to the node and architecture
- Tooltip is preserved across refinement unless node is removed

**US-GEN-03: Diagram Style Toolbar**
> As a user, I can customize the visual style of the diagram using a toolbar.

**Acceptance Criteria**:
- Toolbar available at the bottom of the diagram area
- Controls for: font family, size, color, node background, diagram background
- Changes apply immediately without AI call
- Topology (nodes/edges) is NOT affected by style changes

### Refinement Stories

**US-REF-01: Incremental Refinement**
> As a user, I can send follow-up messages to modify the existing diagram incrementally.

**Acceptance Criteria**:
- System classifies intent (PATCH, ADD, REMOVE, STYLE, etc.)
- Existing nodes and edges are preserved by default
- Only requested changes are applied
- Tooltip metadata is preserved for existing nodes
- New version created with changes summary

**US-REF-02: Version History**
> As a user, I can see all diagram versions and switch between them.

**Acceptance Criteria**:
- Version list visible (v1, v2, v3...)
- Current version highlighted
- Click shows that version's diagram and style
- Change summary shown per version

### Export Stories

**US-EXP-01: Mermaid Export**
> As a user, I can copy the diagram as Mermaid syntax for use in documentation.

**Acceptance Criteria**:
- Valid Mermaid syntax generated
- One-click copy to clipboard
- Visual confirmation on copy

**US-EXP-02: JSON Export**
> As a user, I can export the full diagram data as JSON.

**Acceptance Criteria**:
- Includes diagram source, metadata, nodes (with tooltips), edges, and style
- Pretty-printed
- Copyable

**US-EXP-03: Enhanced Prompt Export**
> As a user, I can copy the enhanced prompt to reuse in other tools.

**Acceptance Criteria**:
- Enhanced prompt copyable separately
- Includes entities and structure hints

### Feedback Stories

**US-FB-01: Example Prompts**
> As a new user, I see design-system-specific examples so I know what to type.

**Acceptance Criteria**:
- 3-5 examples covering different diagram types
- Click populates input
- Examples are genuinely useful for design systems

**US-FB-02: Loading/Error/Empty States**
> As a user, I always know what the system is doing.

**Acceptance Criteria**:
- Loading spinner during enhancement and generation
- Human-readable error with suggestions on failure
- Empty state with guidance before first diagram

---

## 6. Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System must accept text input (10-2000 chars) related to design systems | P0 |
| FR-02 | System must enhance raw prompt into structured diagram-generation prompt | P0 |
| FR-03 | System must generate diagram + node metadata (tooltips) | P0 |
| FR-04 | System must render diagram and show tooltips on hover | P0 |
| FR-05 | System must support incremental refinement (PATCH_CHANGE, ADD_ELEMENT, etc.) | P0 |
| FR-06 | System must classify follow-up intent to determine refine strategy | P0 |
| FR-07 | System must provide a style toolbar for non-AI visual customization | P0 |
| FR-08 | Style changes must not trigger AI or mutate diagram topology | P0 |
| FR-09 | System must maintain context and version history across conversation | P0 |
| FR-10 | System must export diagram, style, and metadata in JSON/Mermaid | P0 |

---

## 7. Success Criteria

| Criterion | Target |
|-----------|--------|
| End-to-end time (input → rendered diagram) | < 12 seconds |
| Refinement stability (preserves unchanged elements) | ≥ 95% |
| Tooltip coverage (nodes with meaningful metadata) | 100% |
| Style reactivity (UI update on toolbar change) | < 100ms |
| Export validity (Mermaid renders correctly) | 100% |

---

## 8. Demo Scenarios

### Scenario 1: Base Diagram + Tooltips
**Steps**:
1. Input: "Create a design system architecture for a React app with tokens and components."
2. Verify: Diagram renders. Hover over "Tokens" to see tooltip "Design Tokens define reusable values...".

### Scenario 2: Incremental Refinement
**Steps**:
1. From Scenario 1, type: "Add a Storybook layer for documentation."
2. Verify: Existing nodes/edges preserved. New node "Storybook" added. New version v2 created.

### Scenario 3: Style Toolbar
**Steps**:
1. From Scenario 2, use toolbar to change "Font Family" to "Roboto" and "Node Background" to "Soft Blue".
2. Verify: UI updates immediately. No network request to AI. Topology remains identical.

---

## 9. Open Questions

| Question | Options | Status |
|----------|---------|--------|
| Should enhanced prompt require explicit approval before generation? | Auto-proceed / Require click / Toggle option | Open |
| MVP renderer: Mermaid.js only? | Mermaid only / Also React Flow | Open |
| Diagram history persistence | In-memory only / localStorage / SQLite | Open |
| Context management for long conversations | Truncate / AI summarize / Sliding window | Open |

---

## 10. Future Features (Post-MVP Roadmap)

1. **Eraser AI provider** — send enhanced prompts to Eraser for richer diagrams
2. **PNG/SVG export** — render diagram as image
3. **Diagram library** — save and revisit past diagrams (requires auth + DB)
4. **Team sharing** — share diagram links with others
5. **Custom prompt templates** — user-defined prompt patterns
6. **Multiple AI models** — choose GPT-4o, Claude, etc.
7. **Figma plugin** — generate diagrams directly inside Figma

---

## 11. Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-05-08 | 0.1.0 | Initial PRD draft (generic flow architect) |
| 2026-05-08 | 0.2.0 | Redefined: design-system focus, prompt enhancement, conversational refinement, provider abstraction |
| 2026-05-08 | 0.3.0 | Added Incremental Refinement, Node Tooltips, and Style Toolbar requirements |
