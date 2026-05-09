# API Contracts: AI Design System Diagram Assistant

Base URL: `http://localhost:8000`

---

## GET /health

**Purpose**: Health check for the backend service.

**Response** `200 OK`:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## POST /api/prompts/enhance

**Purpose**: Enhance a raw user prompt into a structured diagram-generation prompt.
**Timeout**: 10 seconds.

**Request Body**:
```json
{
  "raw_prompt": "string (10-2000 chars, required)",
  "diagram_type": "auto | design-system-architecture | component-hierarchy | token-architecture | design-to-code-workflow",
  "source": "text | voice"
}
```

**Response** `200 OK`:
```json
{
  "enhanced_prompt": "string",
  "diagram_goal": "string",
  "detected_diagram_type": "design-system-architecture | component-hierarchy | token-architecture | design-to-code-workflow",
  "entities": ["string"],
  "relationships": [
    {
      "from": "string",
      "to": "string",
      "type": "string (depends-on | contains | feeds-into | exports-to | extends)"
    }
  ],
  "structure_hints": "string (e.g., 'top-down layered architecture')",
  "assumptions": ["string"],
  "recommended_provider": "mermaid | eraser | structured-graph"
}
```

---

## POST /api/codebase/analyze (NEW)

**Purpose**: Analyze a public GitHub repository and suggest an architecture diagram.
- **Refinement Flow**: Context-aware diagram updates.
- **Strict Timeouts**: Both Enhance and Refine APIs have a strict 10-second timeout to ensure snappy user experience.

**Request Body**:
```json
{
  "repo_url": "string (valid public GitHub URL, required)",
  "diagram_type": "auto | architecture | folder-structure | component-dependency | api-flow | sequence | data-flow | design-system | state-management | auth-flow",
  "node_theme": "default | minimal | soft | technical | colorful | dark | enterprise"
}
```

**Response** `200 OK`:
```json
{
  "analysis_id": "string (uuid)",
  "repo_name": "string",
  "detected_stack": ["React", "Next.js", "Tailwind"],
  "important_files": ["package.json", "src/app/page.tsx"],
  "project_summary": "string",
  "architecture_summary": "string",
  "recommended_diagram_type": "architecture",
  "enhanced_prompt": "string (structured prompt for diagram generator)",
  "warnings": ["string"]
}
```

---

## POST /api/codebase/generate-diagram (NEW)

**Purpose**: Generate a diagram from a codebase analysis.

**Request Body**:
```json
{
  "repo_url": "string",
  "analysis_id": "string | null",
  "diagram_type": "string",
  "node_theme": "string",
  "provider": "mermaid | structured-graph",
  "conversation_id": "string | null"
}
```

**Response** `200 OK`:
```json
{
  "diagram_id": "string (uuid)",
  "conversation_id": "string (uuid)",
  "base_diagram_id": "string (uuid)",
  "version": 1,
  "source_type": "codebase",
  "repo_url": "string",
  "title": "string",
  "diagram_type": "string",
  "provider": "mermaid",
  "diagram_source": "string",
  "diagram_format": "mermaid",
  "nodes": [
    {
      "id": "node1",
      "label": "App Router",
      "type": "module",
      "metadata": {
        "tooltip_title": "App Router",
        "tooltip_description": "Next.js 13+ App Router structure",
        "role": "Routing",
        "importance": "high",
        "connections_summary": "Manages page navigation",
        "related_files": ["src/app/layout.tsx", "src/app/page.tsx"]
      },
      "style": {}
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "node1",
      "target": "node2",
      "label": "interaction",
      "metadata": {
        "tooltip_title": "Relationship Title",
        "tooltip_description": "Contextual interaction explanation",
        "relationship_type": "dependency | data-flow | sequence | ownership | generic",
        "source_to_target_summary": "Summary of the link",
        "importance": "high | medium | low"
      },
      "style": {}
    }
  ],
  "style": {
    "node_theme": "technical"
  },
  "explanation": "string",
  "codebase_summary": "string",
  "metadata": {
    "detected_stack": ["Next.js"],
    "important_files": ["..."],
    "analysis_warnings": []
  }
}
```

---

## POST /api/diagrams/generate

**Purpose**: Generate a diagram from an enhanced prompt using the selected provider.

**Request Body**:
```json
{
  "raw_prompt": "string (original user input)",
  "enhanced_prompt": "string (from /api/prompts/enhance)",
  "diagram_type": "design-system-architecture | component-hierarchy | token-architecture | design-to-code-workflow",
  "provider": "mermaid | eraser | structured-graph",
  "conversation_id": "string | null (null for first generation)"
}
```

**Response** `200 OK`:
*(Schema identical to /api/codebase/generate-diagram, but source_type is "prompt")*

---

## POST /api/diagrams/refine

**Purpose**: Modify an existing diagram based on follow-up instructions.
**Timeout**: 10 seconds.

**Request Body**:
```json
{
  "conversation_id": "string (required)",
  "diagram_id": "string (current diagram ID)",
  "followup_prompt": "string (10-1000 chars)",
  "current_diagram_source": "string (current Mermaid/graph)",
  "current_nodes": ["DiagramNode (optional, for topology preservation)"],
  "provider": "string"
}
```

**Response** `200 OK`:
*(Schema same as generation, with change_intent and changes_summary)*

---

## PATCH /api/diagrams/{diagram_id}/style

**Purpose**: Update visual styling of a diagram without calling AI or changing topology.

**Request Body**:
```json
{
  "style": {
    "font_family": "Inter | Arial | Roboto | System",
    "font_size": "small | medium | large",
    "font_color": "default | dark | muted",
    "node_background_color": "default | white | soft-blue | soft-gray | soft-purple",
    "node_theme": "default | minimal | soft | technical | colorful | dark | enterprise"
  }
}
```

---

## Common Error Codes (Added Codebase Specifics)

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `GITHUB_REPO_NOT_FOUND` | 404 | Public GitHub repository not found |
| `GITHUB_RATE_LIMIT` | 429 | GitHub API rate limit hit |
| `CODE_ANALYSIS_FAILED` | 500 | AI could not analyze the repository tree |
| `INVALID_GITHUB_URL` | 400 | The provided URL is not a valid GitHub URL |
