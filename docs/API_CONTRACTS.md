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

**Error** `422 Unprocessable Entity`:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input must be between 10 and 2000 characters.",
    "field": "raw_prompt"
  }
}
```

**Error** `500 Internal Server Error`:
```json
{
  "error": {
    "code": "ENHANCEMENT_FAILED",
    "message": "Unable to enhance this prompt. Please try rephrasing.",
    "suggestion": "Be more specific about design system components and relationships.",
    "retry_allowed": true
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
```json
{
  "diagram_id": "string (uuid)",
  "conversation_id": "string (uuid)",
  "base_diagram_id": "string (uuid)",
  "version": 1,
  "title": "string",
  "diagram_type": "string",
  "provider": "string",
  "diagram_source": "string (Mermaid syntax)",
  "diagram_format": "mermaid",
  "nodes": [
    {
      "id": "A",
      "label": "Design Tokens",
      "type": "token",
      "metadata": {
        "tooltip_title": "Design Tokens",
        "tooltip_description": "Reusable values like colors and spacing.",
        "role": "Foundation",
        "importance": "high",
        "connections_summary": "Feeds into components"
      },
      "style": {
        "background_color": null,
        "font_color": null
      }
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "A",
      "target": "B",
      "label": "uses"
    }
  ],
  "style": {
    "font_family": "Inter",
    "font_size": "medium",
    "font_color": "default",
    "node_background_color": "default",
    "diagram_background_color": "default"
  },
  "explanation": "string",
  "metadata": {
    "node_count": 8,
    "edge_count": 7,
    "generated_at": "2026-05-08T14:00:00Z"
  }
}
```

**Error** `500 Internal Server Error`:
```json
{
  "error": {
    "code": "GENERATION_FAILED",
    "message": "Could not generate a valid diagram after retrying.",
    "suggestion": "Try simplifying your description or selecting a specific diagram type.",
    "retry_allowed": true
  }
}
```

---

## POST /api/diagrams/refine

**Purpose**: Modify an existing diagram based on follow-up instructions.

**Request Body**:
```json
{
  "conversation_id": "string (required)",
  "diagram_id": "string (current diagram ID)",
  "followup_prompt": "string (10-1000 chars)",
  "current_diagram_source": "string (current Mermaid/graph)",
  "provider": "string"
}
```

**Response** `200 OK`:
```json
{
  "diagram_id": "string (new uuid)",
  "conversation_id": "string",
  "base_diagram_id": "string",
  "parent_diagram_id": "string",
  "version": 2,
  "change_intent": "PATCH_CHANGE | ADD_ELEMENT | REMOVE_ELEMENT | STYLE_CHANGE | REGENERATE",
  "is_full_regeneration": false,
  "diagram_source": "string",
  "nodes": [],
  "edges": [],
  "style": {},
  "explanation": "string",
  "changes_summary": ["Added Storybook layer"],
  "metadata": {}
}
```

**Error** `404 Not Found`:
```json
{
  "error": {
    "code": "CONVERSATION_NOT_FOUND",
    "message": "Conversation not found. Please start a new diagram.",
    "retry_allowed": false
  }
}
```

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
    "diagram_background_color": "default | white | light-gray"
  }
}
```

**Response** `200 OK`:
```json
{
  "diagram_id": "string",
  "style": {
    "font_family": "Inter",
    "font_size": "medium",
    "font_color": "default",
    "node_background_color": "soft-blue",
    "diagram_background_color": "white"
  },
  "updated_at": "2026-05-08T14:10:00Z"
}
```

---

## GET /api/diagrams/{diagram_id}/nodes/{node_id}/tooltip

**Purpose**: (Optional) Fetch detailed tooltip metadata for a specific node.

**Response** `200 OK`:
```json
{
  "node_id": "string",
  "tooltip_title": "string",
  "tooltip_description": "string",
  "role": "string",
  "connections_summary": "string"
}
```

---

## POST /api/diagrams/export

**Purpose**: Export the current diagram in the requested format.

**Request Body**:
```json
{
  "conversation_id": "string",
  "diagram_id": "string",
  "format": "mermaid | json | enhanced-prompt | explanation"
}
```

**Response** `200 OK`:
```json
{
  "format": "mermaid",
  "content": "string (formatted content in requested format)",
  "filename_suggestion": "design-system-architecture.md"
}
```

---

## POST /api/voice/transcribe (Optional/Future)

**Purpose**: Server-side speech-to-text (if browser API insufficient).

**Note**: MVP uses browser Web Speech API. This endpoint is reserved for future backend STT.

**Request**: `multipart/form-data` with audio file
**Response**:
```json
{
  "transcript": "string",
  "confidence": 0.95,
  "language": "en"
}
```

---

## GET /api/conversations/{conversation_id}/versions

**Purpose**: Get all diagram versions for a conversation.

**Response** `200 OK`:
```json
{
  "conversation_id": "string",
  "versions": [
    {
      "diagram_id": "string",
      "version": 1,
      "title": "string",
      "diagram_type": "string",
      "changes_summary": [],
      "created_at": "2026-05-08T14:00:00Z"
    },
    {
      "diagram_id": "string",
      "version": 2,
      "title": "string",
      "diagram_type": "string",
      "changes_summary": ["Added testing layer"],
      "created_at": "2026-05-08T14:05:00Z"
    }
  ]
}
```

---

## Common Error Schema

All errors follow this structure:

```json
{
  "error": {
    "code": "string (machine-readable error code)",
    "message": "string (human-readable message for UI display)",
    "suggestion": "string | null (actionable suggestion for user)",
    "field": "string | null (specific field for validation errors)",
    "retry_allowed": "boolean"
  }
}
```

### Error Codes

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `VALIDATION_ERROR` | 422 | Input failed validation |
| `ENHANCEMENT_FAILED` | 500 | AI could not enhance the prompt |
| `GENERATION_FAILED` | 500 | AI could not generate a valid diagram |
| `REFINEMENT_FAILED` | 500 | AI could not refine the diagram |
| `CONVERSATION_NOT_FOUND` | 404 | Conversation ID does not exist |
| `PROVIDER_ERROR` | 503 | Diagram provider is unavailable |
| `RATE_LIMITED` | 429 | Too many requests |

---

## CORS Configuration

```python
origins = [
    "http://localhost:3000",  # Next.js dev
]
```

---

## Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | Optional | Client-generated request ID for tracing |
