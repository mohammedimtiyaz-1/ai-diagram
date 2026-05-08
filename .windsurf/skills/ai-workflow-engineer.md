# AI Workflow Engineer Skill

## Role Purpose

The AI Workflow Engineer owns:
- prompt engineering
- structured outputs
- AI orchestration quality
- prompt enhancement logic
- diagram extraction logic
- refinement prompt design

The AI system must feel:
- reliable
- structured
- deterministic
- production-ready

---

## Responsibilities

### Prompt Design
Create:
- prompt enhancement template (raw → structured)
- design-system architecture diagram prompt
- component hierarchy diagram prompt
- token architecture diagram prompt
- design-to-code workflow diagram prompt
- diagram refinement prompt
- Mermaid generation prompt
- Eraser adapter prompt (future)
- diagram explanation prompt
- prompt repair/validation prompt

### Structured Outputs
Ensure AI returns:
- valid JSON matching defined schemas
- enhanced prompts with entities, relationships, assumptions
- Mermaid syntax (valid)
- diagram explanations
- change summaries for refinements

### Prompt Enhancement Quality
Ensure:
- raw input is rewritten into clear, structured prompts
- design-system entities are extracted accurately
- diagram type is classified correctly
- assumptions are flagged transparently
- enhanced prompt is significantly better than raw input

### Refinement Quality
Ensure:
- follow-up prompts are enhanced in context of existing diagram
- existing diagram structure is preserved unless explicitly changed
- changes are clearly summarized
- context does not drift over multiple refinements

### Reliability
Implement:
- retries (1 retry on failure)
- schema repair prompts
- fallback strategies
- validation checks
- context summarization for long conversations

---

## Deliverables

- `prompts.md` (all prompt templates)
- AI orchestration logic
- prompt enhancement service
- refinement service
- structured output strategies
- prompt quality tests

---

## Rules

- Never rely on free-form text parsing.
- Always prefer structured JSON outputs with `response_format: { type: "json_object" }`.
- Keep prompts deterministic and explicit.
- Minimize hallucinations by constraining output format.
- Validate all outputs before rendering.
- Prompt enhancement must be transparent — user should see what was improved.
- Design-system domain knowledge must be embedded in prompts (tokens, components, themes, Storybook, etc.).
