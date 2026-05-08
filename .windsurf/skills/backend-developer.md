# Backend Developer Skill

## Role Purpose

The Backend Developer owns:
- API implementation
- AI orchestration
- validation
- data normalization
- backend reliability
- provider abstraction
- conversation context management

The backend should be:
- clean
- async-first
- predictable
- strongly validated

---

## Responsibilities

### API Development
Implement:
- prompt enhancement endpoint (`POST /api/prompts/enhance`)
- diagram generation endpoint (`POST /api/diagrams/generate`)
- diagram refinement endpoint (`POST /api/diagrams/refine`)
- export endpoint (`POST /api/diagrams/export`)
- conversation versions endpoint (`GET /api/conversations/{id}/versions`)
- health endpoint (`GET /health`)

### AI Orchestration
Implement:
- prompt enhancement service
- diagram generation orchestration
- refinement orchestration
- structured output handling
- retry mechanism (1 retry on failure)
- response normalization

### Provider Abstraction
Implement:
- `DiagramProvider` abstract base class
- `MermaidProvider` implementation (MVP)
- Provider registry/factory
- Provider-specific prompt adaptation
- Future: `EraserProvider` adapter

### Validation
Use:
- Pydantic v2 schemas
- typed responses
- strict contracts
- Mermaid syntax validation (basic)
- AI output JSON schema validation

### Conversation & Versioning
Implement:
- in-memory conversation context service
- message history tracking
- diagram version tracking
- context summarization for long conversations

### Error Handling
Handle:
- invalid AI responses
- malformed diagram data
- API failures
- timeout handling
- provider failures

---

## Deliverables

- FastAPI services
- AI orchestration layer
- provider abstraction
- validation schemas
- backend tests
- API documentation

---

## Rules

- Never trust raw AI responses.
- Validate all diagram structures before returning to frontend.
- Keep services modular (one service per domain concern).
- Avoid giant service files.
- Use async properly (FastAPI async endpoints).
- Keep API contracts stable.
- OpenAI API key must never be exposed to frontend.
- Always log errors internally; never leak internals to client error responses.
