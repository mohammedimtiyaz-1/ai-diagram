# Architecture: AI Design System Diagram Assistant

## System Overview

```
User Input (text/voice OR GitHub URL)
  → Mode Selection (Prompt vs Codebase)
  → [Case Codebase]: 
      → GitHub API extraction (tree + key files)
      → AI Codebase Analysis (summary + detect stack)
  → [Case Prompt]:
      → Design-System Intent Extraction
      → Prompt Enhancement (AI)
  → Diagram Type Classification
  → Diagram Provider (Mermaid / Structured Graph)
  → Generated Diagram (Topology + Metadata + related_files)
  → Frontend Renderer (with Hover Tooltips)
  → Conversational Refinement (AI - Incremental Patching)
```

---

## Frontend Architecture

### Components
- **Input Mode Selector** — toggle between Design Prompt and GitHub URL
- **GitHub Input Component** — URL validation, type/theme selectors
- **Diagram Preview Panel** — rendering, hover tooltip integration
- **Node Tooltip** — context metadata + **related files** links
- **Diagram Style Toolbar** — ribbon for typography and **Node Theme** customization
- **Version History** — track iterative changes and summaries

### State Management
- `TopologyState`: JSON representation of current nodes/edges
- `MetadataState`: Map of node IDs to tooltip data (includes `related_files`)
- `StyleState`: Global visual settings (font, colors) and **Node Theme**
- `ConversationState`: Messages and versions
- `AnalysisState`: (For Codebase) Stored architecture summary and stack info

---

## Backend Architecture

### Services
- **Codebase Analyzer** — (AI) summarizes repo architecture and extracts modules
- **Intent Classifier** — (AI) classifies user request for strategy selection
- **Prompt Enhancer** — (AI) expands prompt + generates node metadata
- **Diagram Generator** — (AI) generates/patches Mermaid source
- **GitHub Service** — fetches repo tree and filters important files
- **Versioning Service** — creates immutable versions of topology + metadata + style

---

## Data Flow (Detailed)

### Codebase Analysis (Flow B)
```
1. User provides GitHub URL
2. Backend:
   - GitHub Service: Fetch tree + package.json
   - Codebase Analyzer: AI summarizes tech stack and architecture
3. Diagram Generator: AI generates Mermaid diagram with tooltips pointing to repo files
4. Frontend: Render diagram with 'related_files' metadata in tooltips
```

### Visual Theme Update
```
1. User selects "Technical" theme in toolbar
2. Frontend: Update StyleState (theme: 'technical')
3. MermaidRenderer: Apply theme-specific classDefs/styles to existing source
4. Result: Immediate visual change without AI or backend call
```

---

## Data Models (Updated)

### DiagramNode
- id, label, type
- metadata: { tooltip_title, description, role, connections_summary, **related_files[]** }
- style: { bg_color, font_color }

### DiagramStyle
- font_family, font_size, font_color
- node_background_color, diagram_background_color
- **node_theme** (default, minimal, soft, technical, colorful, dark, enterprise)

### CodebaseMetadata
- repo_name, repo_url
- detected_stack[], important_files[]
- architecture_summary, project_type

---

## Extension Points

| Extension | How to Add |
|-----------|-----------|
| New codebase provider | Add provider to `GitHubService` (e.g. GitLab, Bitbucket) |
| New diagram provider | Implement `DiagramProvider` interface |
| New node theme | Add theme styles to `MermaidRenderer` mapping |
| Persistent storage | Swap in-memory store for SQLite/PostgreSQL |
