# Skills: AI Design System Diagram Assistant

This document defines the virtual team roles, responsibilities, expectations, workflows, ownership boundaries, and quality standards for the AI Design System Diagram Assistant project.

The purpose of these skill definitions is to ensure:
- proper architectural thinking
- production-level engineering quality
- controlled scope
- high-quality documentation
- maintainable implementation
- portfolio-grade execution

The project should feel like a polished startup MVP, not an experimental prototype.

---

# Core Project Principles

All roles must follow these principles:

- Keep the scope intentionally small.
- Prioritize polish over feature count.
- Prefer maintainability over cleverness.
- Build reusable and modular systems.
- Every feature must support the core workflow:
  raw input → prompt enhancement → diagram generation → conversational refinement → export.
- Maintain clean documentation continuously.
- Never introduce unnecessary complexity.
- Use modern engineering best practices.
- Ensure portfolio-grade quality.

---

# 1. Product Manager Skill

## Role Purpose

The Product Manager owns:
- scope clarity
- roadmap planning
- feature prioritization
- milestone management
- project coordination
- progress tracking

This role ensures the project remains:
- realistic
- focused
- buildable
- portfolio-friendly

---

## Responsibilities

### Scope Management
- Prevent feature creep.
- Keep MVP small and achievable.
- Reject unnecessary features.
- Prioritize core workflows only.
- Enforce design-system domain focus (not generic diagram tool).

### Requirement Management
- Define feature requirements clearly.
- Create actionable implementation tasks.
- Ensure all tasks have acceptance criteria.
- Convert vague ideas into concrete engineering tasks.
- Own prompt enhancement and conversational refinement as core differentiators.

### Planning
- Maintain:
  - task-board.md
  - progress-tracker.md
  - implementation-plan.md
- Define milestones and sprint goals.
- Track dependencies between tasks.
- Coordinate provider abstraction and pluggable architecture planning.

### Coordination
- Coordinate work between:
  - frontend
  - backend
  - AI workflow
  - QA
  - documentation
  - CI/CD

### Product Quality
- Ensure UX remains intuitive.
- Ensure project feels production-grade.
- Ensure flows remain simple and understandable.
- Ensure prompt enhancement transparency is a first-class UX concern.

---

## Deliverables

- Project roadmap
- Milestone planning
- Task breakdowns
- Acceptance criteria
- Scope decisions
- Progress tracking

---

## Product Manager Rules

- Do not allow over-engineering.
- Do not introduce unnecessary infrastructure.
- Do not add features without clear user value.
- Prioritize usability and demoability.
- Always optimize for portfolio quality.
- Prompt enhancement must not be treated as optional — it is the core differentiator.
- Conversational refinement is a P0 feature, not a stretch goal.

---

# 2. Software Architect Skill

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

- architecture.md
- API contracts
- module structure
- shared interfaces (DiagramProvider)
- technical decisions
- engineering guidelines

---

## Architect Rules

- Avoid premature optimization.
- Avoid deeply coupled modules.
- Avoid logic duplication.
- Avoid business logic inside UI components.
- Prefer simple abstractions.
- Keep architecture startup-MVP friendly.
- Provider abstraction must be real, not theoretical — implement with MermaidProvider first.
- Never send raw user prompt directly to diagram provider without enhancement (unless user opts out).

---

# 3. Frontend Developer Skill

## Role Purpose

The Frontend Developer owns:
- user experience
- component implementation
- responsiveness
- frontend interactions
- visual polish

The frontend should feel:
- modern
- fast
- intuitive
- SaaS-quality

---

## Responsibilities

### UI Development
Build:
- landing page (hero, examples, CTA)
- workspace split layout (chat panel + diagram panel)
- prompt input panel (textarea, type selector, submit)
- voice input module (mic button, transcript preview)
- enhanced prompt preview component
- Mermaid diagram renderer
- conversation history panel
- follow-up refinement input
- diagram version history sidebar
- export panel (Mermaid, JSON, prompt, explanation)
- loading states
- error states
- empty states

### Mermaid.js Integration
Implement:
- dynamic import with SSR disabled
- diagram rendering from API response
- error handling for invalid Mermaid
- zoom/pan if needed
- title and explanation display

### State Management
Manage:
- workspace state (Zustand)
- conversation messages
- current diagram version
- diagram version history
- enhanced prompt display state
- loading states (enhancing, generating, refining)
- error state
- export state

### UX
Ensure:
- responsive design (desktop-first ≥1024px)
- keyboard usability
- clean spacing
- smooth interactions
- intuitive layout
- transparent AI experience (user sees enhanced prompt)

### Performance
Optimize:
- React rendering
- Mermaid re-rendering on diagram updates
- unnecessary rerenders
- large conversation history performance

---

## Deliverables

- reusable components
- polished UI
- responsive pages
- diagram renderer
- export features
- chat interface
- version history UI

---

## Frontend Developer Rules

- Do not hardcode data.
- Do not mix API logic into UI components (use custom hooks or service layer).
- Use reusable components.
- Use strict TypeScript typing.
- Keep components small and focused.
- Maintain clean folder structure.
- Mermaid rendering must be client-side only (dynamic import).
- Never expose API keys or backend internals to the frontend.

---

# 4. Backend Developer Skill

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

## Backend Developer Rules

- Never trust raw AI responses.
- Validate all diagram structures before returning to frontend.
- Keep services modular (one service per domain concern).
- Avoid giant service files.
- Use async properly (FastAPI async endpoints).
- Keep API contracts stable.
- OpenAI API key must never be exposed to frontend.
- Always log errors internally; never leak internals to client error responses.

---

# 5. AI Workflow Engineer Skill

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

- prompts.md (all prompt templates)
- AI orchestration logic
- prompt enhancement service
- refinement service
- structured output strategies
- prompt quality tests

---

## AI Engineer Rules

- Never rely on free-form text parsing.
- Always prefer structured JSON outputs with `response_format: { type: "json_object" }`.
- Keep prompts deterministic and explicit.
- Minimize hallucinations by constraining output format.
- Validate all outputs before rendering.
- Prompt enhancement must be transparent — user should see what was improved.
- Design-system domain knowledge must be embedded in prompts (tokens, components, themes, Storybook, etc.).

---

# 6. QA / Tester Skill

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

- testing-strategy.md
- backend unit tests
- frontend component tests
- API contract tests
- AI quality tests
- manual QA checklist
- test reports

---

## QA Rules

- Test happy paths and failure paths.
- Test malformed AI outputs.
- Test loading states.
- Test invalid graph/diagram structures.
- Test responsiveness thoroughly.
- Test prompt enhancement quality with real inputs.
- Test refinement consistency across multiple turns.
- All critical paths must have automated tests.

---

# 7. Documentation Engineer Skill

## Role Purpose

The Documentation Engineer owns:
- project clarity
- onboarding quality
- portfolio presentation
- developer understanding
- AI workflow explanation

Documentation should feel:
- professional
- concise
- maintainable
- startup-grade

---

## Responsibilities

### Documentation
Maintain:
- README.md (setup, usage, architecture overview)
- TECHNICAL_DESIGN.md (system overview, architecture decisions)
- API_CONTRACTS.md (endpoint documentation)
- AI_WORKFLOW_DESIGN.md (prompt pipeline, enhancement, refinement)
- prompts.md (all AI prompt templates)
- portfolio case study

### Portfolio Positioning
Explain:
- technical decisions
- AI workflow design (prompt enhancement + refinement)
- provider abstraction strategy
- architecture choices
- engineering tradeoffs
- why design-system focus was chosen

### Developer Experience
Ensure:
- setup is easy (`make dev` or equivalent)
- commands are documented
- environment variables are explained
- architecture is understandable from docs alone

### AI Workflow Documentation
Document:
- how prompt enhancement works
- how refinement maintains context
- how provider abstraction enables future providers
- how diagram types are classified
- how errors are recovered

---

## Deliverables

- README.md
- TECHNICAL_DESIGN.md
- API_CONTRACTS.md
- AI_WORKFLOW_DESIGN.md
- portfolio case study
- architecture decision records (ADRs)

---

## Documentation Rules

- Keep docs updated continuously.
- Prefer diagrams and examples.
- Explain WHY decisions were made.
- Keep onboarding friction low.
- Document the AI workflow clearly — this is a key differentiator.
- Document provider abstraction so future contributors can add new providers.

---

# 8. CI/CD Developer Skill

## Role Purpose

The CI/CD Developer owns:
- continuous integration pipeline
- continuous deployment setup
- GitHub Actions workflows
- code quality automation
- deployment infrastructure
- environment management

The CI/CD pipeline must be:
- automated
- reliable
- fast
- transparent

---

## Responsibilities

### GitHub Actions Workflows
Create:
- **Frontend CI**: lint, type-check, build, test on PR/push
- **Backend CI**: lint (ruff), type-check, test on PR/push
- **Integration CI**: end-to-end smoke tests
- **Deploy Preview**: Vercel preview for frontend PRs
- **Deploy Staging**: auto-deploy main branch to staging
- **Deploy Production**: manual or tag-based production deploy

### Code Quality Automation
Configure:
- ESLint + Prettier for frontend (enforced in CI)
- Ruff + Black for backend (enforced in CI)
- TypeScript strict mode checks
- Pydantic schema validation tests
- Test coverage reporting (optional)
- Dependency vulnerability scanning (Dependabot)

### Deployment Infrastructure
Setup:
- **Frontend**: Vercel deployment (Next.js native)
- **Backend**: Railway / Render / Fly.io deployment
- Environment variable management (Vercel env, backend env)
- Health check endpoint monitoring
- Deployment status notifications

### GitHub Repository Management
Configure:
- Branch protection rules (require PR, require checks)
- PR templates
- Issue templates
- Labels and milestones
- CODEOWNERS file (optional)
- Semantic versioning strategy (optional)

### Local Development Environment
Ensure:
- `make dev` starts both frontend and backend
- `make install` installs all dependencies
- `make test` runs all tests
- `make lint` runs all linters
- `make format` runs all formatters
- Docker Compose setup (optional, for future PostgreSQL/Redis)

---

## Deliverables

- `.github/workflows/` directory with all CI workflows
- `Makefile` or equivalent task runner
- `docker-compose.yml` (optional)
- Deployment documentation
- Environment setup guide
- Troubleshooting guide

---

## CI/CD Developer Rules

- Fail fast in CI — lint and type-check before tests.
- Never deploy with failing tests.
- Keep CI pipeline under 5 minutes for feedback loop.
- Use matrix builds for multiple Node/Python versions (optional).
- Secrets must be stored in GitHub Secrets, never in code.
- Deployment must be reproducible (same commit deploys the same artifacts).
- Health checks must pass before considering deployment successful.
- Rollback strategy must be documented (even if manual).

---

# Collaboration Workflow

All roles must collaborate through:
- implementation-plan.md
- task-board.md
- progress-tracker.md

Before starting new work:
1. Check dependencies.
2. Update task status.
3. Confirm acceptance criteria.
4. Review architecture impact.
5. Notify CI/CD if infrastructure changes are needed.

---

# Role Interaction Matrix

| When... | Involves |
|---------|----------|
| Adding a new diagram provider | Architect designs interface, Backend implements, AI Engineer creates prompt, QA tests, CI/CD updates pipelines |
| Changing API contract | Architect approves, Backend implements, Frontend updates, QA tests, Docs updates API_CONTRACTS.md |
| Adding a new diagram type | Product Manager approves scope, AI Engineer creates prompt, Backend updates classification, QA tests |
| UI redesign | Frontend leads, Architect reviews, Product Manager approves, QA tests responsive layout |
| Deploying to production | CI/CD leads, Backend verifies health, Frontend verifies build, QA runs smoke tests |
| AI prompt changes | AI Engineer leads, Backend integrates, QA tests output quality, Docs updates AI_WORKFLOW_DESIGN.md |

---

# Final Project Goal

Build a portfolio-grade AI SaaS application that demonstrates:

- modern Next.js App Router architecture
- FastAPI backend engineering
- AI workflow orchestration (prompt enhancement + conversational refinement)
- structured AI outputs (JSON schema enforcement)
- Mermaid diagram visualization
- SaaS-quality UX with transparent AI
- provider abstraction for extensibility
- production-level engineering discipline
- clean documentation
- automated CI/CD

The final project should feel:
- realistic
- polished
- technically mature
- startup-ready
- demo-friendly
- impressive in interviews and client discussions
