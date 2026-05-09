# Module Composition

## How All Modules Work Together

This document defines the composition of frontend modules, backend modules, and the contracts between them.

---

## Frontend Composition

### Components (Hierarchy)

```
WorkspaceShell (split layout: left 40% / right 60%)
├── ChatPanel (left column)
│   ├── InputModeToggle (Prompt vs GitHub)
│   ├── [Flow A]: PromptInput
│   │   ├── Textarea
│   │   ├── DiagramTypeSelector
│   │   └── SubmitButton
│   ├── [Flow B]: GitHubInput
│   │   ├── URLInput (GitHub validation)
│   │   ├── CodebaseTypeSelector (Architecture | Folder Structure | API Flow)
│   │   ├── ThemeSelector (Technical | Soft | etc.)
│   │   └── AnalyzeButton
│   ├── VoiceInput
│   ├── EnhancedPromptPreview
│   └── ConversationHistory
│
└── DiagramPanel (right column)
    ├── DiagramPreview
    │   ├── MermaidRenderer (Instant Node Themes mapping)
    │   ├── DiagramTitle
    │   └── DiagramExplanation
    ├── DiagramStyleToolbar (Bottom Ribbon)
    │   ├── FontSelector
    │   ├── ThemeSelector (instantly updates Renderer)
    │   └── ScaleControls
    ├── VersionHistory
    └── ExportPanel (MMD | JSON | Prompt | Explanation)
```

### State Stores (Zustand)

```
useWorkspaceStore
├── inputMode: 'prompt' | 'codebase'
├── setInputMode

useDiagramStore
├── currentDiagram
├── nodeTheme: string
├── setNodeTheme (updates CSS/Mermaid classDefs)
```

### API Clients (TanStack Query)

```
codebaseApi
├── analyze(repoUrl, type) → AnalysisResult
└── generate(analysisId, type, theme) → DiagramResult
```

---

## Backend Composition

### Package/Module Structure

```
app/
├── api/routes/
│   ├── codebase.py         # POST /api/codebase/{analyze,generate}
├── services/
│   ├── github_service.py   # Tree extraction + filtering
│   ├── codebase_service.py # AI Analyzer + Enhancer
│   ├── theme_service.py    # Mermaid style/theme mapping
```

---

## Request Lifecycles (Updated)

### Codebase Analysis Lifecycle (Flow B)

1. User enters GitHub URL + Type.
2. Frontend: POST `/api/codebase/analyze`.
3. Backend: `GitHubService` fetches repo tree + `package.json`.
4. Backend: `CodebaseAnalyzer` (AI) creates architecture summary.
5. Backend: Returns `AnalysisResult`.
6. Frontend: User reviews summary, clicks "Generate Diagram".
7. Frontend: POST `/api/codebase/generate-diagram`.
8. Backend: `CodebaseEnhancer` (AI) creates diagram prompt.
9. Backend: `MermaidProvider` generates source with file path metadata.
10. Frontend: Renders diagram with theme and interactive tooltips.

---

## Node Theme Lifecycle

1. User selects "Technical" in `StyleToolbar`.
2. Frontend: `useDiagramStore.setNodeTheme('technical')`.
3. `MermaidRenderer`: Receives new theme state.
4. `MermaidRenderer`: Re-assembles Mermaid source: `Existing Source` + `Theme classDefs`.
5. UI: Re-renders diagram instantly (no network call).
