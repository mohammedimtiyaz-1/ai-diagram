# Coding Rules: AI Design System Diagram Assistant

## Product Focus

- The project is **design-system focused**, not a generic diagram tool.
- All prompts and diagrams must be optimized for design-system architecture.
- Every feature must support the core flow: **raw input → enhanced prompt → diagram generation → refinement**.
- **Incremental refinement** is mandatory: preserve existing nodes and edges unless explicitly requested to change.
- **Node metadata** (tooltips) must be generated for every node during the AI phase.
- **Diagram styling** via the toolbar must be decoupled from diagram topology and AI calls.
- Prompt enhancement is a **first-class feature**, not optional pre-processing.

## Refinement Rules

- All follow-up requests must be classified for intent (PATCH, ADD, REMOVE, STYLE, REGENERATE).
- STYLE_CHANGE requests from chat should be handled by updating visual state, not regenerating the full diagram.
- EXPLAIN_ONLY requests must not mutate the diagram.
- Full regeneration is a guardrail: only execute when explicitly specified (e.g., "start over").

## UX Rules

- Prioritize polished UX and clean architecture.
- Chat-style interface for input and refinement.
- **Node tooltips** must provide contextualDS information on hover.
- **Style toolbar** (ribbon) must update preview state immediately without AI lag.
- Show enhanced prompt before generation (transparency).
- Diagram preview should be clear and readable.
- Version history should be accessible but not overwhelming.
- Responsive layout, desktop-first (≥1024px).
