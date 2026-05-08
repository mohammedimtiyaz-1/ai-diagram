# AI Design System Diagram Assistant

A portfolio-grade fullstack SaaS application that transforms design system ideas into structured, AI-generated diagrams.

## What It Does

Describe your design system in plain text or voice. The AI enhances your raw prompt into a structured diagram-generation prompt, produces a Mermaid diagram, and lets you refine it conversationally. All diagram versions are tracked, and everything can be exported.

**Current Phase:** Phase 1 — Project Setup (Complete)

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

## What's Not Implemented Yet

### Phase 2 — Backend Core (Next)

- API schemas (Pydantic models)
- Mock endpoints for prompt enhancement and diagram generation
- Provider abstraction interface
- MermaidProvider stub

### Phase 3 — Frontend Workspace Shell

- Real chat panel components
- Prompt input with diagram type selector
- API client integration
- Enhanced prompt preview
- Loading and error states

### Phase 4–9

- AI prompt enhancement (OpenAI integration)
- Mermaid diagram generation
- Conversational refinement
- Voice input (browser SpeechRecognition)
- Export actions
- Version history
- Testing & documentation polish

## Development Commands

| Command | Description |
|---------|-------------|
| `cd apps/web && npm run dev` | Start frontend dev server |
| `cd apps/api && uvicorn app.main:app --reload --port 8000` | Start backend dev server |
| `cd apps/web && npm run lint` | Run frontend linter |
| `cd apps/web && npm run type-check` | Run frontend type check |
| `cd apps/api && pytest` | Run backend tests |
| `cd apps/api && ruff check .` | Run backend linter |

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
