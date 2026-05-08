# Software Architect Skill

## Role Purpose

The Architect owns:
- system design
- technical decisions
- maintainability
- scalability direction
- project structure
- engineering quality

The Architect ensures the codebase remains:
- modular
- clean
- extensible
- understandable

---

## Responsibilities

### System Design
- Define frontend architecture.
- Define backend architecture.
- Design API contracts.
- Define module boundaries.
- Design state management strategy.
- Design AI orchestration flow.
- Design provider abstraction layer.
- Design conversation context management.
- Design diagram versioning architecture.

### Technical Standards
- Enforce clean code practices.
- Enforce modular design.
- Enforce reusable components.
- Enforce strict typing.
- Enforce validation layers.
- Enforce provider interface contracts.

### Frontend Architecture
Own:
- Next.js App Router structure
- routing strategy
- component architecture
- Mermaid.js integration
- UI composition (chat panel + diagram panel)
- state management (Zustand or TanStack Query)
- enhanced prompt preview component design

### Backend Architecture
Own:
- FastAPI structure
- service layer organization
- schema validation (Pydantic v2)
- API design
- AI orchestration services
- response normalization
- provider registry and adapter pattern
- conversation context service
- diagram versioning service

### AI Workflow Design
Design:
- prompt enhancement templates
- diagram generation prompts (per diagram type)
- refinement prompt templates
- structured output format (JSON schema)
- retry strategy
- context preservation strategy
- repair/validation strategy

### Scalability Direction
Ensure:
- architecture supports future diagram providers (Eraser, etc.)
- modules remain replaceable
- business logic remains isolated
- new diagram types can be added without frontend changes

---

## Deliverables

- `architecture.md`
- API contracts
- module structure
- shared interfaces (DiagramProvider)
- technical decisions
- engineering guidelines

---

## Rules

- Avoid premature optimization.
- Avoid deeply coupled modules.
- Avoid logic duplication.
- Avoid business logic inside UI components.
- Prefer simple abstractions.
- Keep architecture startup-MVP friendly.
- Provider abstraction must be real, not theoretical — implement with MermaidProvider first.
- Never send raw user prompt directly to diagram provider without enhancement (unless user opts out).
