# AI Design System Diagram Assistant

A portfolio-grade fullstack SaaS application that transforms design system ideas into structured, AI-generated diagrams.

## What It Does

Describe your design system in plain text or voice. The AI enhances your raw prompt into a structured diagram-generation prompt, produces a Mermaid diagram, and lets you refine it conversationally. All diagram versions are tracked, and everything can be exported.

**Current Phase:** Phase 9 — Testing & Documentation (Final Phase)

## Architecture

```
Frontend (Next.js 14+ App Router)
  ├── Landing Page (/)
  └── Workspace Page (/workspace)
       ├── Chat / Prompt Panel (left)
       └── Diagram Preview Panel (right)

Backend (FastAPI)
  ├── /health
  ├── /api/prompts/enhance  (Phase 4)
  ├── /api/diagrams/generate  (Phase 5)
  ├── /api/diagrams/refine  (Phase 6)
  └── /api/diagrams/export  (Phase 8)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14+, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.11+, Pydantic v2 |
| AI | OpenAI GPT-4o (structured JSON output) |
| Diagram | Mermaid.js (MVP), pluggable provider architecture |
| State | Zustand (client), TanStack Query (server) |

## Local Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+

### Frontend

```bash
cd apps/web
cp .env.example .env
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Backend

```bash
cd apps/api
cp .env.example .env
# Install dependencies (choose one)
# Option A: with uv
uv pip install -e ".[dev]"
# Option B: with pip
pip install -e ".[dev]"

# Run server
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`.

### Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok","service":"ai-design-system-diagram-assistant-api"}
```

## What's Implemented

### Phase 0 — Architecture Finalization (Complete)
- [x] All documentation finalized (PRD, technical design, API contracts)
- [x] Architecture blueprint and tech stack decisions
- [x] Module composition defined
- [x] Implementation phases planned

### Phase 1 — Project Setup (Complete)
- [x] Next.js frontend with TypeScript and Tailwind CSS
- [x] Landing page (`/`) with project title, description, and CTA
- [x] Workspace placeholder page (`/workspace`) with split-panel layout
- [x] FastAPI backend with CORS middleware
- [x] Health check endpoint (`GET /health`)
- [x] Environment configuration (`.env.example` files)
- [x] Pydantic settings for backend config
- [x] Custom error classes for backend
- [x] Backend test for health endpoint
- [x] Project structure matching architecture docs

### Phase 2 — Backend Core (Complete)
- [x] API schemas (Pydantic models for prompts, diagrams, conversations)
- [x] Provider abstraction interface
- [x] MermaidProvider stub with mock generation
- [x] Mock endpoints for prompt enhancement and diagram generation
- [x] In-memory conversation and version services
- [x] Export service with multiple formats
- [x] 12 backend tests passing

### Phase 3 — Frontend Workspace Shell (Complete)
- [x] Real chat panel components (PromptInput, ConversationHistory)
- [x] Prompt input with diagram type selector and example prompts
- [x] API client integration with typed fetch wrappers
- [x] Zustand store for workspace state
- [x] Enhanced prompt preview in conversation history
- [x] DiagramPreview component with Mermaid rendering
- [x] FollowUpInput component for refinement
- [x] VersionHistory component showing diagram versions
- [x] Loading and error states
- [x] Landing page updated with example prompts

### Phase 4 — AI Prompt Enhancement (Complete)
- [x] OpenAI client singleton with sync/async methods
- [x] Prompt enhancement template with system prompt for design-system intent
- [x] Real PromptEnhancerService using GPT-4o with JSON response format
- [x] Retry logic (1 retry on failure)
- [x] Fallback enhancement for resilience
- [x] 5 enhancement service tests passing

### Phase 5 — Mermaid Diagram Generation (Complete)
- [x] Mermaid generation template with system prompt for Mermaid syntax
- [x] Real MermaidProvider.generate_diagram() using GPT-4o
- [x] Mermaid syntax validation
- [x] Retry logic and fallback for resilience
- [x] 6 Mermaid provider tests passing

### Phase 6 — Conversational Refinement (Complete)
- [x] Mermaid refinement template with system prompt
- [x] Real MermaidProvider.refine_diagram() using GPT-4o
- [x] Retry logic and fallback for resilience
- [x] 2 refinement tests passing

### Phase 7 — Voice Input (Complete)
- [x] Web Speech API integration
- [x] VoiceInput component with microphone button
- [x] Speech-to-text transcription
- [x] Integration with PromptInput component
- [x] Visual feedback (recording state with Mic/MicOff icons)

### Phase 8 — Export & Polish (Complete)
- [x] ExportPanel component with Mermaid, JSON, and Explanation export options
- [x] Download functionality using Blob API
- [x] Loading states for export operations
- [x] Integration with DiagramPreview component

## What's Not Implemented Yet

### Phase 9 — Testing & Documentation (In Progress)
- [x] Backend tests (24/24 passing)
- [x] Fix failing API tests for AI behavior
- [x] Update README with complete setup instructions
- [ ] Add API documentation
- [ ] Add frontend testing

## Development Commands

| Command | Description |
|---------|-------------|
| `cd apps/web && npm run dev` | Start frontend dev server |
| `cd apps/api && uvicorn app.main:app --reload --port 8000` | Start backend dev server |
| `cd apps/web && npm run lint` | Run frontend linter |
| `cd apps/web && npm run type-check` | Run frontend type check |
| `cd apps/api && pytest` | Run backend tests |
| `cd apps/api && ruff check .` | Run backend linter |

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full deployment instructions.

**Quick overview:**
- **Frontend** → Vercel (auto-deployed via GitHub Actions)
- **Backend** → Render (auto-deployed via GitHub Actions + deploy hook)
- **CI/CD** → GitHub Actions (`.github/workflows/ci.yml`, `deploy-frontend.yml`, `deploy-backend.yml`)

## Project Structure

```
/
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── app/
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── layout.tsx      # Root layout
│   │   │   ├── workspace/
│   │   │   │   └── page.tsx    # Workspace page
│   │   │   └── globals.css
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── stores/
│   │   ├── .env.example
│   │   ├── package.json
│   │   ├── next.config.ts
│   │   ├── tailwind.config.ts
│   │   └── tsconfig.json
│   │
│   └── api/                    # FastAPI backend
│       ├── app/
│       │   ├── main.py
│       │   ├── api/
│       │   │   └── routes/
│       │   │       └── health.py
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   └── errors.py
│       │   ├── schemas/
│       │   ├── services/
│       │   ├── providers/
│       │   └── prompts/
│       ├── tests/
│       │   └── test_health.py
│       ├── pyproject.toml
│       └── .env.example
│
├── docs/                       # Documentation
│   ├── PRODUCT_REQUIREMENTS.md
│   ├── TECHNICAL_DESIGN.md
│   ├── API_CONTRACTS.md
│   ├── AI_WORKFLOW_DESIGN.md
│   └── DEVELOPMENT_PLAN.md
│
├── .windsurf/                  # Windsurf context files
│   ├── architecture-blueprint.md
│   ├── tech-stack-decisions.md
│   ├── module-composition.md
│   ├── implementation-phases.md
│   ├── phase-tracker.md
│   ├── progress-tracker.md
│   ├── task-board.md
│   ├── rules.md
│   └── skills/
│
└── README.md                   # This file
```

## License

MIT — Portfolio project.
