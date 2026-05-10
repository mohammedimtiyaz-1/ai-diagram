# LinkedIn Project Description

## Project Name
**AI Design System Diagram Assistant**

## Project Overview
A portfolio-grade fullstack SaaS application that transforms design system ideas into structured, AI-generated diagrams. Users can describe their design system in plain text, use voice input, or provide a GitHub repository URL. The AI enhances the prompt, generates a Mermaid diagram, and enables conversational refinement with version tracking.

## Live Demo
- **Frontend:** https://ai-design-system-diagram.vercel.app
- **Backend API:** https://ai-diagram-fds0.onrender.com

## Problem Solved
Design system architects and developers often struggle to visualize complex design system architectures manually. This tool automates the process of creating, refining, and maintaining design system diagrams through natural language interaction.

## Key Features

### 🎯 AI-Powered Generation
- **Prompt Enhancement**: Raw user prompts are enhanced by GPT-4o into structured diagram-generation prompts
- **Intelligent Diagram Generation**: Produces Mermaid diagrams with proper syntax and structure
- **Codebase Analysis**: Analyzes GitHub repositories to generate architecture diagrams from actual code
- **Evidence-Based Analysis**: Uses GPT-4o to detect architecture patterns, tech stacks, and module boundaries

### 💬 Conversational Refinement
- **Intent Classification**: Understands user intent (ADD_ELEMENT, REMOVE_ELEMENT, PATCH_CHANGE, STYLE_CHANGE, EXPLAIN_ONLY, REGENERATE)
- **Version Tracking**: All diagram versions are preserved with change history
- **Natural Language Refinement**: Users can refine diagrams through conversational follow-up prompts
- **Smart Fallback**: Preserves diagram structure even when AI refinement fails

### 🎨 User Experience
- **Voice Input**: Web Speech API integration for hands-free diagram creation
- **Real-time Validation**: Client-side form validation with inline error messages
- **Loading Indicators**: Context-aware loading states for different operations
- **Export Functionality**: Export diagrams as Mermaid, JSON, or plain text explanations
- **Visual Customization**: Diagram style toolbar for visual customization

### 🔧 Technical Excellence
- **Resilient AI Integration**: Retry logic, fallback mechanisms, and timeout handling
- **Rate Limiting**: API rate limiting to prevent abuse
- **Error Handling**: Comprehensive error parsing for Pydantic validation
- **CORS Configuration**: Production-ready CORS setup for cross-origin requests

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand (client), TanStack Query (server)
- **Diagram Rendering**: Mermaid.js, D3.js
- **Icons**: Lucide React
- **Voice**: Web Speech API

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Validation**: Pydantic v2
- **Async Runtime**: asyncio with httpx for async HTTP requests
- **Testing**: pytest
- **Linting**: ruff

### AI/ML
- **Models**: OpenAI GPT-4o (primary), GPT-4o-mini (fast operations)
- **Structured Output**: JSON mode for reliable parsing
- **Prompt Engineering**: Custom system prompts for each AI operation
- **Model Selection**: Different models for different use cases (analysis vs generation)

### Infrastructure
- **Frontend Hosting**: Vercel (auto-deploy via GitHub Actions)
- **Backend Hosting**: Render (auto-deploy via GitHub Actions)
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Environment Management**: Environment variables for configuration

### Architecture Patterns
- **Provider Pattern**: Pluggable diagram provider architecture (currently Mermaid, extensible to PlantUML, Draw.io)
- **Service Layer**: Separation of concerns with dedicated services (prompt enhancement, diagram generation, refinement, codebase analysis)
- **Repository Pattern**: In-memory conversation and version services
- **Error Handling**: Custom error classes with proper HTTP status codes

## AI Capabilities

### Prompt Enhancement
- Detects design-system intent from raw user input
- Identifies diagram type (flowchart, sequence diagram, class diagram)
- Generates structured prompts with clear instructions
- Uses GPT-4o-mini for fast, cost-effective enhancement

### Diagram Generation
- Generates syntactically correct Mermaid code
- Creates nodes, edges, and proper relationships
- Supports multiple diagram types (flowcharts, sequence diagrams, class diagrams)
- Uses GPT-4o-mini for generation with retry logic

### Refinement
- Classifies user intent (6 different intent types)
- Applies minimal edits to preserve existing structure
- Handles EXPLAIN_ONLY without AI calls for efficiency
- Parses nodes/edges from diagram source when not provided
- Uses GPT-4o-mini with fallback to preserve diagram structure

### Codebase Analysis
- Fetches GitHub repository file tree
- Identifies important files (manifests, configs, entry points)
- Fetches file contents in parallel for speed
- Detects architecture patterns (Monolith, Monorepo, Microservices, etc.)
- Identifies tech stack from manifests (package.json, pyproject.toml, etc.)
- Generates enhanced prompts for diagram generation
- Uses GPT-4o for deep, evidence-based analysis

## Screenshots

### Landing Page
[Add screenshot of landing page with project title, description, and CTA]

### Workspace - Text Input
[Add screenshot of workspace with text prompt input and diagram type selector]

### Workspace - Voice Input
[Add screenshot showing voice input in action with microphone button]

### Workspace - Codebase Analysis
[Add screenshot of GitHub URL input and codebase analysis results]

### Workspace - Diagram Generation
[Add screenshot of generated diagram in the preview panel]

### Workspace - Refinement
[Add screenshot of conversational refinement with version history]

### Workspace - Export
[Add screenshot of export panel with Mermaid, JSON, and explanation options]

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
│   │   │   └── workspace/      # Workspace components
│   │   │       ├── PromptInput.tsx
│   │   │       ├── CodebaseInput.tsx
│   │   │       ├── ConversationHistory.tsx
│   │   │       ├── DiagramPreview.tsx
│   │   │       ├── FollowUpInput.tsx
│   │   │       ├── VoiceInput.tsx
│   │   │       ├── VersionHistory.tsx
│   │   │       └── ExportPanel.tsx
│   │   ├── lib/
│   │   │   └── api.ts          # API client
│   │   └── stores/
│   │       └── workspace.ts    # Zustand store
│   │
│   └── api/                    # FastAPI backend
│       ├── app/
│       │   ├── main.py         # FastAPI app
│       │   ├── api/
│       │   │   └── routes/
│       │   │       ├── health.py
│       │   │       ├── prompts.py
│       │   │       ├── diagrams.py
│       │   │       └── codebase.py
│       │   ├── core/
│       │   │   ├── config.py   # Settings
│       │   │   ├── errors.py   # Custom errors
│       │   │   ├── rate_limit.py
│       │   │   └── timeouts.py
│       │   ├── schemas/        # Pydantic models
│       │   ├── services/       # Business logic
│       │   │   ├── prompt_enhancer.py
│       │   │   ├── codebase_service.py
│       │   │   ├── refinement_service.py
│       │   │   ├── conversation_service.py
│       │   │   └── version_service.py
│       │   ├── providers/
│       │   │   ├── base.py     # Provider interface
│       │   │   └── mermaid_provider.py
│       │   └── prompts/        # AI prompts
│       │       ├── enhancement_prompt.py
│       │       ├── mermaid_prompt.py
│       │       ├── refinement_prompt.py
│       │       └── codebase_prompt.py
│       └── tests/              # Backend tests
```

## Implementation Phases

### Phase 0 — Architecture Finalization ✅
- Documentation finalized (PRD, technical design, API contracts)
- Architecture blueprint and tech stack decisions
- Module composition defined
- Implementation phases planned

### Phase 1 — Project Setup ✅
- Next.js frontend with TypeScript and Tailwind CSS
- Landing page and workspace placeholder
- FastAPI backend with CORS middleware
- Health check endpoint
- Environment configuration

### Phase 2 — Backend Core ✅
- API schemas (Pydantic models)
- Provider abstraction interface
- MermaidProvider stub
- Mock endpoints
- In-memory conversation and version services
- 12 backend tests passing

### Phase 3 — Frontend Workspace Shell ✅
- Real chat panel components
- API client integration
- Zustand store for workspace state
- DiagramPreview component with Mermaid rendering
- FollowUpInput component
- VersionHistory component
- Loading and error states

### Phase 4 — AI Prompt Enhancement ✅
- OpenAI client singleton
- Prompt enhancement template
- Real PromptEnhancerService using GPT-4o
- Retry logic and fallback
- 5 enhancement service tests passing

### Phase 5 — Mermaid Diagram Generation ✅
- Mermaid generation template
- Real MermaidProvider.generate_diagram()
- Mermaid syntax validation
- Retry logic and fallback
- 6 Mermaid provider tests passing

### Phase 6 — Conversational Refinement ✅
- Mermaid refinement template
- Real MermaidProvider.refine_diagram()
- Intent classification (6 intent types)
- EXPLAIN_ONLY handling without AI calls
- Node/edge parsing from diagram source
- Version history metadata persistence
- 2 refinement tests passing

### Phase 7 — Codebase Analysis ✅
- GitHub repository URL input
- GitHub service for fetching repository data
- File tree parsing and important file detection
- Parallel file content fetching
- Evidence-based codebase analysis using GPT-4o
- Architecture pattern detection
- Tech stack detection from manifests
- 4 codebase analysis tests passing

### Phase 8 — Voice Input ✅
- Web Speech API integration
- VoiceInput component with microphone button
- Speech-to-text transcription
- Integration with PromptInput component
- Visual feedback

### Phase 9 — Export & Polish ✅
- ExportPanel component
- Download functionality
- Loading states
- DiagramStyleToolbar
- Client-side form validation
- Chat loading indicator
- CORS configuration
- API error parsing

## Challenges & Solutions

### Challenge 1: Empty Nodes/Edges in Refinement
**Problem**: When refinement failed or used EXPLAIN_ONLY intent, the response returned empty nodes/edges arrays even though the diagram source contained valid Mermaid code.

**Solution**: 
- Enhanced Mermaid parser to extract nodes/edges from diagram source
- Added version history lookup for nodes/edges before parsing fallback
- Updated provider fallback to accept and use existing nodes/edges
- Added nodes/edges to version metadata for persistence

### Challenge 2: CORS Errors in Production
**Problem**: Frontend on Vercel couldn't call backend on Render due to CORS restrictions.

**Solution**: Added Vercel URL to CORS origins in backend configuration and Render environment variables.

### Challenge 3: API Validation Errors
**Problem**: Short inputs (e.g., "hi") caused API validation errors with unclear messages.

**Solution**: 
- Added client-side form validation with minimum length requirements
- Real-time visual feedback (red border/bg) when input is too short
- Inline error messages while typing
- Improved API error parsing for Pydantic validation arrays

### Challenge 4: Timeout Handling
**Problem**: AI operations could timeout, leaving users in an unclear state.

**Solution**: Implemented comprehensive timeout handling with:
- Configurable timeouts for different operations
- Custom timeout error classes
- Graceful error messages
- Cancel button for long-running operations

## Future Enhancements

- Add API documentation (Swagger/OpenAPI)
- Add frontend testing (Playwright/Vitest)
- Add more diagram providers (PlantUML, Draw.io)
- Add real-time collaboration features
- Add diagram sharing and public links
- Add more diagram types (ER diagrams, network diagrams)

## GitHub Repository
https://github.com/mohammedimtiyaz-1/ai-diagram

## Tags
#AI #MachineLearning #NextJS #FastAPI #TypeScript #Python #OpenAI #GPT4 #WebDevelopment #FullStack #DesignSystems #Mermaid #SaaS #Vercel #Render
