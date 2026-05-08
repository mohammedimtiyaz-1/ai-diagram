# Coding Rules: AI Design System Diagram Assistant

## Product Focus

- The project is **design-system focused**, not a generic diagram tool.
- All prompts and diagrams must be optimized for design-system architecture.
- Every feature must support the core flow: **raw input → enhanced prompt → diagram generation → refinement**.
- Prompt enhancement is a **first-class feature**, not optional pre-processing.
- Never send raw user prompt directly to diagram provider without enhancement (unless user explicitly opts out).

## Architecture Rules

- Diagram generation provider must remain **pluggable** via provider abstraction.
- Do not tightly couple the app to Eraser, Mermaid, or any single provider.
- Use provider interface to support Eraser, Mermaid, React Flow, or future engines.
- Conversation refinement must preserve diagram context across messages.
- Keep frontend and backend cleanly decoupled via API contracts.
- Keep all AI outputs **reviewable and debuggable**.
- Store enhanced prompt and final diagram state for traceability.

## Scope Rules

- Keep the project small and portfolio-focused.
- Do not over-engineer. MVP should remain small.
- Prioritize clean architecture over feature quantity.
- Define clean module boundaries so new diagram types, providers, prompt templates, and export options can be added later.
- Principle: **Small MVP, scalable design.**

## Code Standards

- Use TypeScript strictly on frontend.
- Use Pydantic models strictly on backend.
- AI responses must return structured JSON, not free-form text.
- All generated diagram data must be validated before rendering.
- Keep UI polished, modern, and simple.
- Use reusable components.
- Avoid hardcoded business logic inside UI components.
- Add meaningful error handling at every boundary.
- Add loading states and empty states for all async operations.
- Add tests for important logic (prompt enhancement, schema validation, provider adapter).
- Document all major decisions.

## UX Rules

- Prioritize polished UX and clean architecture.
- Chat-style interface for input and refinement.
- Show enhanced prompt before generation (transparency).
- Diagram preview should be clear and readable.
- Version history should be accessible but not overwhelming.
- Responsive layout, desktop-first (≥1024px).
