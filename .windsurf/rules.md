# Coding Rules: AI Design System Diagram Assistant

## Product Focus

- The project is **design-system focused**, not a generic diagram tool.
- All prompts and diagrams must be optimized for design-system architecture or codebase representation.
- Every feature must support the core flows: 
    - Flow A: **raw input → enhanced prompt → diagram generation → refinement**.
    - Flow B: **GitHub URL → codebase analysis → diagram generation → refinement**.
- **Incremental refinement** is mandatory: preserve existing nodes and edges unless explicitly requested to change.
- **Node metadata** (tooltips) must be generated for every node during the AI phase.
- **Diagram styling** via the toolbar must be decoupled from diagram topology and AI calls.
- Prompt enhancement and codebase analysis are **first-class features**.

## Codebase Analysis Rules (Flow B)

- **Privacy First**: Support public GitHub repositories only.
- **Efficiency**: Fetch repo tree recursively but limit total bytes fetched; do not clone full repos.
- **AI Context**: Prioritize reading key files (package.json, tsconfig, entry points) for architecture summaries.
- **Node Tooltips**: For codebase diagrams, nodes should include `related_files` metadata pointing to actual repo paths.

## Refinement & Theme Rules

- All follow-up requests must be classified for intent (PATCH, ADD, REMOVE, STYLE, REGENERATE).
- **Node Themes**: Visual themes (Technical, Soft, etc.) apply styling only; changing a theme should not regenerate diagram topology or trigger AI calls.
- STYLE_CHANGE requests from chat should be handled by updating visual state, not regenerating the full diagram.
- EXPLAIN_ONLY requests must not mutate the diagram.
- Full regeneration is a guardrail: only execute when explicitly specified (e.g., "start over" or "change diagram type").

## UX Rules

- Prioritize polished UX and clean architecture.
- **Input Mode Toggle**: Switch between "Design Prompt" and "GitHub URL" modes clearly.
- **Node tooltips** must provide contextual DS or codebase information on hover.
- **Style toolbar** (ribbon) must update preview state immediately without AI lag.
- Show analysis/enhancement progress before generation (transparency).
- Diagram preview should be clear and readable.
- Export as `.mmd` (Mermaid) and JSON.
- Responsive layout, desktop-first (≥1024px).
