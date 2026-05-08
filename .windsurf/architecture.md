# Architecture: AI Design System Diagram Assistant

## System Overview

```
User Input (text/voice)
  → Input Normalization
  → Design-System Intent Extraction
  → Prompt Enhancement (AI)
  → Diagram Type Classification
  → Provider-Specific Prompt Adaptation
  → Diagram Provider (Mermaid / Eraser / Structured Graph)
  → Generated Diagram
  → Frontend Renderer
  → User Follow-up Chat
  → Context-Aware Refinement (AI)
  → New Diagram Version
```

---

## Frontend Architecture

### Pages
- **Landing Page** — product explanation, examples, CTA
- **Workspace Page** — main working area (chat + diagram)

| Feature | Description |
|---------|-------------|
| **Intent Classification** | Determines if request is NEW, PATCH, STYLE, or REGENERATE |
| **Metadata Enrichment** | Generates DS-specific tooltip info for every node |
| **Incremental Patching** | Preserves existing topology across refinements |
| **Visual Style State** | Decouples styling from AI logic |

---

## Frontend Architecture

### Components
- **Chat Input Panel** — text/voice input, intent handling
- **Diagram Preview Panel** — rendering, hover tooltip integration
- **Node Tooltip** — hover popover with context-specific metadata
- **Diagram Style Toolbar** — bottom ribbon for visual customizations
- **Version History** — track iterative changes and summaries

### State Management
- `TopologyState`: JSON representation of current nodes/edges
- `MetadataState`: Map of node IDs to tooltip data
- `StyleState`: Global visual settings (font, colors)
- `ConversationState`: Messages and versions

---

## Backend Architecture

### Services
- **Intent Classifier** — (AI) classifies user request for strategy selection
- **Prompt Enhancer** — (AI) expands prompt + generates node metadata
- **Diagram Generator** — (AI) generates/patches Mermaid source
- **Style Controller** — (No-AI) updates style state without topology mutation
- **Versioning Service** — creates immutable versions of topology + metadata + style

---

## Data Flow (Detailed)

### Incremental Refinement
```
1. User: "Add Storybook layer"
2. Intent Classifier: ADD_ELEMENT
3. Refinement Service:
   - Load vN Topology + Metadata
   - AI: Generate Mermaid patch + new node metadata
   - Update Topology + Metadata
4. Frontend: Rerender diagram + update tooltips
```

### Visual Style Update
```
1. User clicks "Blue Nodes" in toolbar (or types in chat)
2. Case Toolbar: Frontend updates StyleState immediately
3. Case Chat: Intent Classifier: STYLE_CHANGE
4. Style Controller: Updates StyleState (skip AI generation)
5. Frontend: Rerender with new styles
```

---

## Data Models

### DiagramNode
- id, label, type
- metadata: { tooltip_title, description, role, connections_summary }
- style: { bg_color, font_color }

### DiagramStyle
- font_family, font_size, font_color
- node_background_color, diagram_background_color

### DiagramVersion
- diagram_id, base_diagram_id, parent_diagram_id
- version, change_intent
- nodes[], edges[], style{}
- diagram_source (Mermaid)
- changes_summary[]

### Message
- role (user | assistant | system)
- content
- type (input | enhanced_prompt | diagram | refinement | error)
- timestamp

---

## Extension Points

| Extension | How to Add |
|-----------|-----------|
| New diagram provider | Implement `DiagramProvider` interface |
| New diagram type | Add type to classifier, add prompt template |
| New export format | Add format to `ExportService` |
| Persistent storage | Swap in-memory store for SQLite/PostgreSQL |
| Real-time collaboration | Add WebSocket layer on top of conversation service |
