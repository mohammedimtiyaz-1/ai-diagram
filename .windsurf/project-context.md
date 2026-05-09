# AI Design System Diagram Assistant — Project Context

## What is This?

A portfolio-grade AI SaaS application that helps frontend engineers, UI architects, and design system teams transform rough design-system ideas OR existing codebases into clear architecture diagrams. The application uses AI to **enhance user prompts** or **analyze GitHub repositories** before generating diagrams, then allows **iterative chat-based refinement** of the generated output.

**Target feel**: Small startup MVP — polished enough to demo, scalable enough to extend.

---

## Core Flows

### Flow A: Prompt to Diagram
```
User input (text/voice)
  → AI prompt enhancement & metadata enrichment (tooltips)
  → Diagram generation (topology + metadata)
  → Display in UI with hover tooltips
  → Visual customization via style toolbar (no AI)
  → Conversational refinement (incremental patching)
  → Export
```

### Flow B: Codebase to Diagram (NEW)
```
GitHub Repository URL
  → Repository tree extraction & key file analysis
  → AI architecture summary & diagram prompt generation
  → Diagram generation with 'related_files' metadata
  → Visual customization via themes (no AI)
  → Conversational refinement (incremental patching)
```

---

## Example Interactions

### Text Input → Enhanced → Diagram
**User types**: "Create a design system architecture for a React and Next.js app with tokens, components, themes, and documentation."
**System enhances**: Adds entities, metadata (tooltips), relationships, and structure hints.
**System generates**: Mermaid architecture diagram. Hovering over "Component Library" shows "The central repository for reusable UI components...".

### GitHub URL → Analysis → Diagram
**User enters**: `https://github.com/example/design-system`
**System analyzes**: Detects React, Next.js, and Tailwind; identifies components/ and tokens/ folders.
**System generates**: "Architecture Diagram" showing the actual folder structure and dependencies, with tooltips pointing to relevant source files.

---

## What Makes This Different

| Feature | Why It Matters |
|---------|---------------|
| **Codebase-to-Diagram** | Automatic documentation of existing repositories — massive time saver |
| **Prompt enhancement** | Raw ideas are improved before generation — better diagrams |
| **Incremental Refinement** | Stable iteration: preserve existing nodes/edges unless changed |
| **Node Tooltips** | Contextual DS knowledge or codebase paths embedded in diagrams |
| **Node Themes** | Rapid visual customization without AI latency or topology breakage |

---

## Diagram Types

| Type | Use Case |
|------|----------|
| Design System Architecture | Overall system layers and integrations |
| Folder Structure Diagram | (Codebase) High-level map of repository layout |
| Component Hierarchy | (Design/Codebase) Atomic/composite/page component structure |
| API Flow Diagram | (Codebase) Request/response flow through services |
| Token Architecture | Primitive → Semantic → Component token pipeline |

---

## Key Principles

1. **Small MVP, scalable design** — don't overbuild, but keep module boundaries clean
2. **Analysis before Generation** — always analyze context (prompt or code) first
3. **Provider-agnostic** — diagram generation layer is pluggable
4. **Transparent AI** — show analysis results and enhanced prompts
5. **Design-system domain focus** — not a generic diagram tool
