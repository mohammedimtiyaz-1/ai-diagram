# Tech Stack Decisions

## Frontend

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **Next.js 14+ App Router** | Chosen | File-based routing, SSR/SSG support, React Server Components reduce client JS, built-in API routes available if needed. Standard for modern React apps. |
| **TypeScript** | Chosen | Strict mode enforced. Eliminates runtime type errors, enables IDE autocomplete, self-documenting code. Non-negotiable for portfolio-grade quality. |
| **Tailwind CSS** | Chosen | Utility-first, rapid UI development, consistent design system, no CSS file bloat. Works perfectly with shadcn/ui. |
| **shadcn/ui** | Chosen | Copy-paste component primitives (not a dependency). Radix-based accessibility, fully customizable, no lock-in. Perfect for building custom UI without fighting a component library. |
| **Mermaid renderer** | Chosen (MVP) | Client-side diagram rendering with `mermaid.render()`. No server dependency, supports all needed diagram types (flowchart, sequence, etc.), text-based source is version-control friendly. |
| **Zustand** | Chosen | Minimal client state management. No boilerplate, no providers, TypeScript-friendly. Handles conversation state, diagram versions, UI mode. |
| **TanStack Query** | Chosen | Server state management (API calls). Caching, deduping, background refetching, loading/error states built-in. Replaces useEffect + fetch patterns. |
| **React Hook Form + Zod** | Chosen | Form validation with TypeScript inference. Zod schemas shared between frontend and backend (can copy Pydantic → Zod). Clean DX, minimal re-renders. |
| **Browser SpeechRecognition API** | Chosen (MVP) | No backend STT needed. Chrome/Edge native support. Transcript editable before submit. Fallback: hide button on unsupported browsers. |

**Frontend excluded:**
- React Flow (too complex for MVP; Mermaid covers rendering needs)
- Redux (overkill; Zustand sufficient)
- SWR (TanStack Query supersedes)
- Framer Motion (nice-to-have polish; add in Phase 8 if time)

---

## Backend

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **FastAPI** | Chosen | Python async framework, automatic OpenAPI docs, Pydantic integration, high performance. Python ecosystem is strongest for AI/ML work. |
| **Python 3.11+** | Chosen | Modern syntax (match, async improvements), better error messages, longer support. AI libraries (OpenAI SDK) target 3.10+. |
| **Pydantic v2** | Chosen | Schema validation, serialization, settings management. v2 is significantly faster than v1. Shared mental model with Zod on frontend. |
| **Uvicorn** | Chosen | ASGI server for FastAPI. Industry standard, supports HTTP/2, works with async endpoints. |
| **httpx** | Chosen | Async HTTP client for calling OpenAI API. Better than `requests` for async code, supports timeouts, retries, connection pooling. |
| **pytest** | Chosen | Python testing standard. Fixtures, parametrization, async support via `pytest-asyncio`. |
| **ruff** | Chosen | Ultra-fast Python linter and formatter (replaces flake8 + black). Single tool, consistent style. |

**Backend excluded (MVP):**
- SQLAlchemy (no database in MVP)
- Celery/Redis (no background jobs needed)
- Alembic (no migrations without DB)
- gunicorn (uvicorn sufficient for dev/demo)

---

## AI

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **OpenAI GPT-4o** | Chosen (MVP) | Best-in-class for structured JSON output, fast, cost-effective. `response_format: { type: "json_object" }` guarantees valid JSON. Strong at following detailed prompts. |
| **OpenAI-compatible abstraction** | Chosen | Backend services accept model name/config. Easy to swap to Claude, local models, or Azure OpenAI without changing service logic. |
| **Prompt enhancement service** | Chosen (mandatory) | Core differentiator. Separate service layer ensures raw prompts are never sent directly to diagram generation. Enables transparent AI UX. |
| **Mermaid generation via AI** | Chosen | AI generates Mermaid syntax from structured prompts. Alternative (static templates) is too rigid for design-system variety. |
| **Strict JSON mode** | Chosen | `response_format: { type: "json_object" }` on every AI call. Eliminates parsing failures from markdown-wrapped JSON. |
| **Prompt versioning in docs** | Chosen | All prompt templates live in `prompts/` directory, versioned in git. Enables A/B testing, rollback, audit trail. |

**AI excluded (MVP):**
- LangChain / LlamaIndex (unnecessary abstraction; direct OpenAI SDK is simpler and more controllable)
- Fine-tuning (GPT-4o is sufficient zero-shot with good prompts)
- Vector database (no RAG needed; all context is conversation-local)

---

## Diagram Rendering

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **Mermaid-first MVP** | Chosen | Browser-renderable via `mermaid.js`, no server image generation needed, text-based source is editable and version-control friendly, supports flowcharts/sequence/graph diagrams natively. |
| **Provider abstraction** | Chosen | `DiagramProvider` interface allows future Eraser/React Flow providers without frontend changes. Frontend receives normalized `DiagramResult` regardless of provider. |
| **Eraser provider** | Future | Will be implemented as second provider using same interface. Requires Eraser API access. Not MVP. |
| **React Flow** | Future option | Could be a provider that returns graph JSON (nodes/edges) instead of Mermaid text. Frontend would render with React Flow library. More interactive but more complex. Not MVP. |

**Why Mermaid first:**
1. Simpler to implement (text → render, no coordinate math)
2. No server-side image generation needed
3. Export is immediately useful (paste into GitHub, Notion, docs)
4. AI is good at generating Mermaid syntax with clear prompts
5. Can always add React Flow later as alternative provider

---

## Persistence

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **In-memory (Python dict)** | Chosen (MVP backend) | No setup, no migrations, instant. Acceptable for demo/portfolio where server restarts are rare. |
| **localStorage (optional)** | Chosen (MVP frontend) | Survives page refresh. Optional enhancement if time permits in Phase 8. Not required for core flow. |
| **SQLite** | Near future | Single-file, zero-config, Python standard library. Upgrade path when version history persistence becomes important. |
| **PostgreSQL** | Future | When auth + multi-user + durability required. SQLAlchemy models can target either SQLite or PostgreSQL. |

**Why no DB in MVP:**
1. Faster development (no schema design, no migrations)
2. No deployment complexity (no database service to provision)
3. Portfolio/demo use case doesn't require durability
4. Easy to add later via SQLAlchemy without changing service interfaces

---

## Testing

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **pytest** | Chosen (backend) | Standard Python testing. Async support, fixtures, parametrization. |
| **pytest-asyncio** | Chosen | Required for testing FastAPI async endpoints and services. |
| **Vitest** | Chosen (frontend) | Vite-native test runner. Fast, Jest-compatible API, TypeScript support built-in. |
| **React Testing Library** | Chosen | Testing components by user interaction (not implementation details). Accessible queries, async utilities. |
| **Playwright** | Future (E2E) | Full browser E2E testing. Expensive to run in CI, but powerful for critical paths. Add after MVP features are stable. |
| **MSW (Mock Service Worker)** | Chosen | Intercept and mock API requests in tests and development. Enables frontend development without running backend. |

---

## Deployment

| Technology | Decision | Rationale |
|------------|----------|-----------|
| **Frontend: Vercel** | Chosen | Next.js native hosting. Automatic previews on PRs, edge network, zero-config. Perfect for portfolio demos. |
| **Backend: Render or Fly.io** | Chosen | Free tier available, simple Docker/Procfile deploy, good for FastAPI ASGI apps. Render has longer free tier uptime; Fly.io has better global distribution. |
| **Environment variables** | Chosen | `OPENAI_API_KEY` stored in Vercel (frontend build env) and Render/Fly (backend runtime env). Never in code. |
| **GitHub Actions** | Chosen (CI) | Frontend lint/build on PR, backend lint/test on PR. Deploy on merge to main. |

**Deployment excluded:**
- Docker (not needed for simple FastAPI app on Render/Fly)
- Kubernetes (massive overkill for MVP)
- AWS/GCP/Azure (complexity not justified for portfolio)

---

## Explicit Non-Decisions for MVP

These are intentionally **not** included:

| Item | Why Excluded | When to Add |
|------|-------------|-------------|
| **Authentication** | No user accounts needed; stateless per-session | When diagram library/persistence required |
| **Billing / payments** | Portfolio project, not commercial SaaS | Never (or when pivoting to product) |
| **Team workspace / multiplayer** | Massive infrastructure (WebSockets, presence, conflicts) | Post-MVP with funding |
| **Figma integration** | Requires Figma API, plugin infrastructure, OAuth | As separate feature post-MVP |
| **Real Eraser integration** | Requires Eraser API access, may not be public | When API available |
| **Complex database schema** | In-memory sufficient for MVP | When persistence required |
| **Drag-drop diagram editing** | Mermaid is text-based; interactive editing would require React Flow provider | As React Flow provider |
| **Custom diagram themes/styling** | Default Mermaid theme sufficient | When branding/customization requested |
| **Mobile-native app** | Desktop-first for diagram work; responsive web sufficient | Never for this product |
| **Offline mode** | Online-only acceptable for AI-dependent app | When adding local AI model |
| **Real-time collaboration** | Single-user editing keeps scope manageable | Major infrastructure investment |

---

## Technology Version Targets

| Technology | Minimum Version | Target Version |
|------------|-----------------|----------------|
| Node.js | 18 LTS | 20 LTS |
| Next.js | 14 | 14+ |
| React | 18 | 18+ |
| TypeScript | 5.0 | 5.3+ |
| Tailwind CSS | 3.4 | 3.4+ |
| Python | 3.11 | 3.11+ |
| FastAPI | 0.110 | 0.110+ |
| Pydantic | 2.0 | 2.6+ |
| OpenAI SDK | 1.0 | 1.30+ |
| Mermaid.js | 10.0 | 10.8+ |
