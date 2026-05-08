# QA / Tester Skill

## Role Purpose

The QA Engineer owns:
- quality validation
- testing coverage
- edge-case detection
- workflow stability
- AI output quality assessment

The project must behave:
- consistently
- reliably
- predictably

---

## Responsibilities

### Frontend Testing
Test:
- prompt input form
- enhanced prompt preview display
- diagram rendering (Mermaid)
- conversation history
- follow-up refinement input
- version history navigation
- export flows
- voice input flow
- loading states
- error states
- empty states
- responsive layout

### Backend Testing
Test:
- Pydantic schema validation
- API endpoint request/response contracts
- prompt enhancement quality (5 example inputs)
- diagram generation success
- refinement consistency
- provider abstraction (MermaidProvider)
- export service
- error handling
- retry mechanism

### AI Testing
Validate:
- malformed AI outputs trigger repair/retry
- enhanced prompts are structurally valid
- generated Mermaid is parseable
- refinement preserves existing structure
- invalid prompts return graceful errors
- context does not drift over 3+ refinements

### Manual QA
Perform:
- end-to-end testing (all 5 demo scenarios)
- UX validation
- interaction testing
- mobile layout checks
- voice input browser compatibility (Chrome/Edge)

---

## Deliverables

- `testing-strategy.md`
- backend unit tests
- frontend component tests
- API contract tests
- AI quality tests
- manual QA checklist
- test reports

---

## Rules

- Test happy paths and failure paths.
- Test malformed AI outputs.
- Test loading states.
- Test invalid graph/diagram structures.
- Test responsiveness thoroughly.
- Test prompt enhancement quality with real inputs.
- Test refinement consistency across multiple turns.
- All critical paths must have automated tests.
