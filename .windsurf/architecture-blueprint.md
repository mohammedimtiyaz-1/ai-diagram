# AI Design System Diagram Assistant — Architecture Blueprint

## Product Summary

AI Design System Diagram Assistant lets users describe design system ideas OR provide a GitHub URL to transform rough ideas or existing codebases into polished, structured diagrams. The application uses a dual-flow AI-first pipeline:
- **Flow A (Prompt)**: Raw input → Enhanced prompt → Diagram generation.
- **Flow B (Codebase)**: GitHub URL → Repo analysis → Diagram generation.
Both flows support iterative chat-based refinement, version tracking, visual theme switching (without AI), and exports.

---

## Core User Journey

```
[LANDING] User selects mode: Design Prompt OR GitHub URL
           ↓
[INPUT] User enters text/voice OR provides GitHub URL
           ↓
[PROCESS] Flow A: AI Prompt Enhancement
          Flow B: GitHub Tree Analysis + AI Architecture Summary
           ↓
[GENERATE] System sends processed context to diagram provider
           ↓
[DISPLAY] Diagram renders with interactive tooltips (including repo paths for Flow B)
           ↓
[STYLE] User selects visual Node Theme (instantly applied via CSS/Mermaid)
           ↓
[CHAT] User sends follow-up for incremental refinement
           ↓
[EXPORT] User downloads .mmd or .json files
```

---

## System Context (Updated)

| Component | Responsibility | MVP Choice |
|-----------|-------------|------------|
| **Frontend** | UI, mode handling, Mermaid rendering, themes | Next.js App Router |
| **Backend** | API, GitHub integration, AI orchestration | FastAPI |
| **GitHub Integration** | Recursive tree extraction and file selection | GitHub API (httpx) |
| **AI Provider** | Enhancement, Analysis, Generation, Refinement | OpenAI GPT-4o |
| **Diagram Provider** | Generate Mermaid from analysis/prompt | MermaidProvider |
| **Storage** | Persistent conversation + version history | File-backed JSON store |

---

## Application Layers (Updated)

### 1. Presentation Layer (Frontend)
- **Input Mode Selector**: Toggle between "Design Prompt" and "GitHub URL".
- **GitHub Input**: URL input, diagram type selector, node theme selector.
- **Mermaid Renderer**: Enhanced with **Node Themes** (Technical, Soft, etc.) mapping.
- **Hover Tooltips**: Enhanced with **related_files** links for codebase diagrams.

### 3. API Layer (Backend)
- `POST /api/codebase/analyze`: Analyze repo tree and return summary.
- `POST /api/codebase/generate-diagram`: Generate diagram from analysis results.
- `PATCH /api/diagrams/{id}/style`: Update visual settings and node theme.

### 4. AI Workflow Layer (Backend)
- **Codebase Analyzer**: AI call to summarize tech stack and architecture from file tree.
- **Codebase Enhancer**: AI call to convert analysis into a specific diagram prompt.

### 5. Persistence Layer (File-backed JSON)
- Conversations and versions saved as JSON files in `apps/api/data/`.
- Ensures state survives server restarts.

---

## Module Dependency Map (Updated)

```
Backend (FastAPI)
├── api/routes/
│   ├── codebase.py       ← GitHubService + CodebaseAnalyzer
├── services/
│   ├── github_service.py ← httpx (GitHub API)
│   ├── codebase_service.py ← AI client + Tree filtering
│   ├── theme_service.py  ← Mapping themes to Mermaid styles
```

---

## Data Flow Diagrams (Updated)

### Codebase → Diagram Flow
1. User enters GitHub URL + Type + Theme.
2. Frontend sends to `POST /api/codebase/analyze`.
3. Backend:
    - `GitHubService` fetches tree + `package.json`.
    - `CodebaseAnalyzer` (AI) creates summary + stack list.
4. Backend sends to `POST /api/codebase/generate-diagram`.
5. Backend:
    - `CodebaseEnhancer` (AI) creates structured diagram prompt.
    - `MermaidProvider` generates source with `related_files` metadata.
6. Frontend renders diagram with theme and tooltips.

---

## Node Themes Strategy
Themes are applied by appending a `classDef` block to the Mermaid source and mapping node `type` to class names. This happens in the `MermaidRenderer` on the client, or can be persisted via `PATCH /style`.

**Themes**: Default, Minimal, Soft, Technical, Colorful, Dark, Enterprise.

---

## Failure Handling (Updated)
- **GitHub Rate Limit**: Return 429; frontend shows retry timer or guidance.
- **Private Repo**: Return 404; frontend suggests checking URL or permissions.
- **Analysis Fail**: AI fails to summarize; retry once with reduced tree context.
