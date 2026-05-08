# AI Design System Diagram Assistant — Project Context

## What is This?

A portfolio-grade AI SaaS application that helps frontend engineers, UI architects, and design system teams transform rough design-system ideas into clear architecture diagrams. The application uses AI to **enhance user prompts** before generating diagrams, then allows **iterative chat-based refinement** of the generated output.

**Target feel**: Small startup MVP — polished enough to demo, scalable enough to extend.

---

## Core Flow

```
User input (text/voice)
  → AI prompt enhancement & metadata enrichment (tooltips)
  → Diagram generation (topology + metadata)
  → Display in UI with hover tooltips
  → Visual customization via style toolbar (no AI)
  → Conversational refinement (incremental patching)
  → Export
```

---

## Example Interactions

### Text Input → Enhanced → Diagram
**User types**: "Create a design system architecture for a React and Next.js app with tokens, components, themes, and documentation."
**System enhances**: Adds entities, metadata (tooltips), relationships, and structure hints.
**System generates**: Mermaid architecture diagram. Hovering over "Component Library" shows "The central repository for reusable UI components...".

### Conversational Refinement (Incremental)
**User follows up**: "Add a Storybook layer for documentation."
**System**: Classifies as `ADD_ELEMENT` → preserve existing nodes → append Storybook to Mermaid → update v2.

### Visual Customization (No AI)
**User clicks toolbar**: Changes "Node Background" to "Soft Gray".
**System**: Updates style state → preview re-renders immediately.

---

## What Makes This Different

| Feature | Why It Matters |
|---------|---------------|
| **Prompt enhancement** | Raw ideas are improved before generation — better diagrams |
| **Incremental Refinement** | Stable iteration: preserve existing nodes/edges unless changed |
| **Node Tooltips** | Contextual DS knowledge embedded in diagrams |
| **Style Toolbar** | Rapid visual customization without AI latency |
| **Transparent AI** | Shows enhanced prompt — user sees what AI understood |

---

## Target Users

| User | Goal |
|------|------|
| Frontend engineers | Visualize component architecture and dependencies |
| Design system engineers | Map token pipelines, governance, documentation |
| UI architects | Plan scalable component hierarchies |
| Product engineers | Understand design-to-code workflows |
| Technical leads | Communicate architecture decisions visually |
| Design operations teams | Document design system governance |

---

## Diagram Types

| Type | Use Case |
|------|----------|
| Design System Architecture | Overall system layers and integrations |
| Component Hierarchy | Atomic/composite/page component structure |
| Token Architecture | Primitive → Semantic → Component token pipeline |
| Design-to-Code Workflow | Figma → Tokens → Code → Storybook → App |
| Component Dependency Map | What depends on what |

---

## Key Principles

1. **Small MVP, scalable design** — don't overbuild, but keep module boundaries clean
2. **Prompt enhancement is first-class** — never send raw input directly to diagram provider
3. **Provider-agnostic** — diagram generation layer is pluggable
4. **Transparent AI** — show what was enhanced, what was assumed
5. **Design-system domain focus** — not a generic diagram tool

---

## Documentation Map

| Document | Location |
|----------|----------|
| Product Requirements | `docs/PRODUCT_REQUIREMENTS.md` |
| Technical Design | `docs/TECHNICAL_DESIGN.md` |
| API Contracts | `docs/API_CONTRACTS.md` |
| AI Workflow Design | `docs/AI_WORKFLOW_DESIGN.md` |
| Development Plan | `docs/DEVELOPMENT_PLAN.md` |
| Task Board | `.windsurf/task-board.md` |
| Progress Tracker | `.windsurf/progress-tracker.md` |
| Architecture | `.windsurf/architecture.md` |
| Prompts | `.windsurf/prompts.md` |
