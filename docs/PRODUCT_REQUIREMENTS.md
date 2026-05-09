# Product Requirements Document: AI Design System Diagram Assistant

## 1. Problem Statement

### The Problem

Design system teams — frontend engineers, UI architects, and design operations professionals — spend significant time communicating architecture decisions visually. They need diagrams showing component hierarchies, token pipelines, theme structures, and design-to-code workflows. Creating these diagrams is:

1. **Time-consuming**: Drawing design-system architecture diagrams manually takes 30-60 minutes
2. **Iterative**: Design systems evolve constantly; diagrams become outdated
3. **Hard to start**: Most people have a rough idea but struggle to structure it visually
4. **Tool-heavy**: Traditional tools require learning complex UIs for one-off diagrams
5. **Disconnected from thinking**: The gap between "I know how this should work" and "here's a clear visual" is large
6. **Code-to-Visual Gap**: Understanding the actual architecture of an existing codebase is difficult without manual reverse-engineering.

### What This Product Solves

AI Design System Diagram Assistant lets users describe their design system ideas in plain English (or voice) OR provide a GitHub codebase URL. It analyzes the context (raw input or repository structure), enhances it into a structured diagram prompt, generates a professional diagram, and then allows iterative refinement through conversation.

### Why This Matters as a Portfolio Project

Demonstrates:
- **AI orchestration**: Prompt enhancement + generation + refinement pipeline
- **Codebase Analysis**: Real-world integration with GitHub API and repository analysis
- **Product thinking**: Niche focus on design-system domain with practical "Code to Diagram" utility
- **Full-stack architecture**: Next.js + FastAPI + AI integration
- **UX design**: Multi-modal input (text, voice, repo URL) with iterative refinement
- **Software architecture**: Provider abstraction, clean module boundaries, extensibility
- **Domain expertise**: Understanding of design systems, tokens, components, themes, and codebase structures

---

## 2. Target Users

### Primary: Frontend & Design System Engineers
**Profile**: Engineers building, maintaining, or scaling design systems
**Goals**:
- Visualize component architecture and token pipelines
- **Document existing repositories automatically**
- Visualize component hierarchies from actual source code
- Iterate on architecture as the system evolves

**Pain points**:
- Hard to communicate design system structure visually
- Diagrams become outdated as tokens and components evolve
- Starting from scratch when planning new design system layers
- Manual effort to diagram existing complex codebases

### Secondary: UI Architects & Technical Leads
**Profile**: Senior engineers making architectural decisions for UI platforms
**Goals**:
- Plan scalable component hierarchies before implementation
- **Audit existing codebase architecture**
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

---

## 3. Core User Journey

### Flow A: Prompt to Design Diagram
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

### Flow B: Codebase to Diagram
```
1. User enters a public GitHub repository URL
2. User selects desired diagram type (Architecture, Component Hierarchy, etc.)
3. System fetches repository tree and analyzes key files (package.json, tsconfig, etc.)
4. AI generates a comprehensive codebase analysis and architecture summary
5. System generates a high-quality diagram representing the actual codebase
6. Diagram is displayed with tooltips linking to actual related files
7. User can refine the diagram or switch themes/types conversationally
```

---

## 4. MVP Feature List

### In Scope (MVP)

| Feature | Description | User Value |
|---------|-------------|------------|
| Text input | Type design-system description | Core entry point |
| **GitHub Mode** | Enter public GitHub URL for codebase analysis | Automated documentation |
| **Codebase Analysis** | AI analyzes repo structure, stack, and dependencies | Accurate visuals |
| **Diagram Type Selector** | Dropdown for Architecture, Folder Structure, Component Dependency, etc. | Tailored visualization |
| Prompt enhancement | AI rewrites raw input into structured diagram prompt | Better diagrams |
| Enhanced prompt preview | Show what AI understood before generation | Trust and control |
| Diagram generation (Mermaid) | Generate Mermaid diagram via pluggable provider | Visual output |
| Diagram display | Render Mermaid in UI with title/explanation | See the result |
| **Incremental Refinement** | Follow-up messages modify existing diagram without full redraw | Faster iteration |
| **Node Hover Tooltips** | Show metadata popovers with role and **related files** | Contextual information |
| **Diagram Style Toolbar** | Ribbon to customize font, size, and **Node Theme** | Visual personalization |
| Diagram version history | Track versions within conversation | Undo/compare |
| Voice input | Browser speech-to-text for hands-free input | Accessibility |
| Export (MMD, JSON) | Copy diagram in multiple formats | Reusability |

### Out of Scope (Post-MVP / Non-Goals)

| Feature | Rationale |
|---------|-----------|
| Private repositories | Requires complex OAuth and security; MVP focus on public repos |
| Deep static analysis | Full AST parsing for every language is heavy; AI + tree is enough for MVP |
| Vector database / RAG | Overkill for basic codebase visualization; useful for deep code search |
| Real-time repo sync | Complexity of webhooks; out of scope for visualization tool |
| Multi-repo analysis | Focus on single repo per diagram for simplicity |

---

## 5. User Stories

### Input & Mode Stories

**US-INP-01: Input Mode Toggle**
> As a user, I can switch between "Design Prompt" and "GitHub URL" modes so I can choose my input source.

**US-INP-04: GitHub URL Input**
> As an engineer, I can provide a public GitHub URL so that the system can visualize my actual codebase architecture.

**Acceptance Criteria**:
- Validates GitHub URL format
- Handles public repos only
- Shows clear error for rate limits or private repos

**US-INP-05: Diagram Type Selection**
> As a user, I can select from a predefined list of diagram types (Architecture, API Flow, etc.) to get the most relevant view.

### Codebase Analysis Stories

**US-CODE-01: Repository Tree Analysis**
> As a user, I want the system to understand my folder structure and package dependencies automatically.

**US-CODE-02: Stack & Technology Detection**
> As a user, I want the system to detect that I'm using Next.js, Tailwind, and FastAPI so the diagram is context-aware.

### Generation & Display Stories

**US-GEN-01: Diagram Generation**
> As a user, after my prompt/repo is analyzed, I receive a professional diagram.

**Acceptance Criteria**:
- Every node includes tooltip metadata (title, description, role, **related files**)
- Related files point to actual paths in the codebase

**US-GEN-04: Node Themes**
> As a user, I can change the "Node Theme" (Technical, Soft, Dark, etc.) to match my presentation style.

---

## 6. Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System must accept text or GitHub URL input | P0 |
| FR-11 | System must fetch and filter public GitHub repository trees | P0 |
| FR-12 | System must identify "important files" (package.json, main entry points) | P0 |
| FR-13 | System must support specific diagram types (Architecture, Folder Structure, API Flow, etc.) | P0 |
| FR-14 | System must support visual Node Themes (Technical, Minimal, Colorful, etc.) | P0 |
| FR-15 | Tooltips must include "related_files" for codebase diagrams | P0 |
| FR-05 | System must support incremental refinement for both Design and Codebase flows | P0 |

---

## 7. Success Criteria

| Criterion | Target |
|-----------|--------|
| GitHub analysis time | < 5 seconds |
| Total time (URL → Diagram) | < 20 seconds |
| Stack detection accuracy | ≥ 90% |
| Refinement stability | ≥ 95% |
| Export validity | 100% |

---

## 11. Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-05-08 | 0.3.0 | Added Incremental Refinement, Node Tooltips, and Style Toolbar requirements |
| 2026-05-08 | 0.4.0 | Added **Codebase to Diagram** (Flow B) requirements, GitHub integration, Diagram Types, and Node Themes. |
