# AI Design System Diagram Assistant

A portfolio-grade fullstack SaaS application that transforms design system ideas into structured, AI-generated diagrams.

## What It Does

Describe your design system in plain text or voice, or provide a GitHub repository URL. The AI enhances your raw prompt into a structured diagram-generation prompt, produces a Mermaid diagram, and lets you refine it conversationally. All diagram versions are tracked, and everything can be exported.

**Current Phase:** Complete — All Phases Delivered

## Live Demo

- **Frontend:** https://ai-design-system-diagram.vercel.app
- **Backend API:** https://ai-diagram-fds0.onrender.com

## Architecture

```
Frontend (Next.js 14+ App Router)
  ├── Landing Page (/)
  └── Workspace Page (/workspace)
       ├── Chat / Prompt Panel (left)
       └── Diagram Preview Panel (right)

Backend (FastAPI)
  ├── /health
  ├── /api/prompts/enhance
  ├── /api/diagrams/generate
  ├── /api/diagrams/refine
  ├── /api/diagrams/export
  ├── /api/codebase/analyze
  └── /api/codebase/generate-diagram
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
- [x] Intent classification (ADD_ELEMENT, REMOVE_ELEMENT, PATCH_CHANGE, STYLE_CHANGE, EXPLAIN_ONLY, REGENERATE)
- [x] EXPLAIN_ONLY intent handling without AI calls
- [x] Retry logic and fallback for resilience
- [x] Node/edge parsing from diagram source when not provided
- [x] Version history metadata persistence for nodes/edges
- [x] 2 refinement tests passing

### Phase 7 — Codebase Analysis (Complete)
- [x] GitHub repository URL input component
- [x] GitHub service for fetching repository data
- [x] File tree parsing and important file detection
- [x] Parallel file content fetching with httpx
- [x] Evidence-based codebase analysis using GPT-4o
- [x] Architecture pattern detection (Monolith, Monorepo, Microservices, etc.)
- [x] Tech stack detection from manifests
- [x] Module boundary identification
- [x] Enhanced prompt generation from codebase analysis
- [x] Codebase diagram generation endpoint
- [x] 4 codebase analysis tests passing

### Phase 8 — Voice Input (Complete)
- [x] Web Speech API integration
- [x] VoiceInput component with microphone button
- [x] Speech-to-text transcription
- [x] Integration with PromptInput component
- [x] Visual feedback (recording state with Mic/MicOff icons)

### Phase 9 — Export & Polish (Complete)
- [x] ExportPanel component with Mermaid, JSON, and Explanation export options
- [x] Download functionality using Blob API
- [x] Loading states for export operations
- [x] Integration with DiagramPreview component
- [x] DiagramStyleToolbar for visual customization
- [x] Client-side form validation with inline error messages
- [x] Chat loading indicator with context-aware messages
- [x] CORS configuration for production domains
- [x] API error parsing for Pydantic validation arrays

## What's Not Implemented Yet

### Future Enhancements (Optional)
- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Add frontend testing (Playwright/Vitest)
- [ ] Add more diagram providers (PlantUML, Draw.io)
- [ ] Add real-time collaboration features
- [ ] Add diagram sharing and public links

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

### Live URLs
- **Frontend:** https://ai-design-system-diagram.vercel.app
- **Backend API:** https://ai-diagram-fds0.onrender.com

### Deployment Platforms
- **Frontend** → Vercel (auto-deployed via GitHub Actions)
- **Backend** → Render (auto-deployed via GitHub Actions + deploy hook)
- **CI/CD** → GitHub Actions (`.github/workflows/ci.yml`, `deploy-frontend.yml`, `deploy-backend.yml`)

### Environment Variables

**Frontend (Vercel):**
- `NEXT_PUBLIC_API_BASE_URL` - Backend API URL (set in Vercel dashboard)

**Backend (Render):**
- `OPENAI_API_KEY` - OpenAI API key for AI operations
- `CORS_ORIGINS` - Comma-separated list of allowed frontend origins (e.g., `http://localhost:3000,https://ai-design-system-diagram.vercel.app`)
- `ENHANCE_MODEL` - AI model for prompt enhancement (default: `gpt-4o-mini`)
- `REFINE_MODEL` - AI model for refinement (default: `gpt-4o-mini`)
- `ANALYZE_MODEL` - AI model for codebase analysis (default: `gpt-4o`)
- `GENERATION_MODEL` - AI model for diagram generation (default: `gpt-4o-mini`)
- `ENHANCE_TIMEOUT_SECONDS` - Timeout for prompt enhancement (default: 30)
- `REFINE_TIMEOUT_SECONDS` - Timeout for refinement (default: 45)
- `ANALYZE_TIMEOUT_SECONDS` - Timeout for codebase analysis (default: 60)
- `ENHANCE_RATE_LIMIT` - Rate limit for enhance API (default: 10 req/min)
- `REFINE_RATE_LIMIT` - Rate limit for refine API (default: 8 req/min)
- `ANALYZE_RATE_LIMIT` - Rate limit for analyze API (default: 5 req/min)

### Manual Deployment

**To Vercel:**
1. Go to https://vercel.com/dashboard
2. Find your `ai-design-system-diagram` project
3. Click **Deployments** → **Redeploy**

**To Render:**
1. Go to https://dashboard.render.com
2. Find your `ai-diagram-api` service
3. Click **Manual Deploy** → **Deploy latest commit**

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
