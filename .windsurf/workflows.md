# Workflows: AI Design System Diagram Assistant

---

## Workflow 1: Text to Design System Diagram
*(Flow A: Design Prompt)*

1. User enters text in chat input panel
2. Frontend validates input (≥10 chars, ≤2000 chars)
3. Frontend sends raw prompt to `/api/prompts/enhance`
4. AI enhances prompt (adds entities, relationships, structure, clarity)
5. Frontend shows enhanced prompt preview
6. Frontend sends enhanced prompt to `/api/diagrams/generate`
7. Provider generates diagram (Mermaid syntax)
8. Frontend renders diagram in preview panel

---

## Workflow 8: Codebase to Diagram (NEW)
*(Flow B: GitHub URL)*

1. User switches input mode to "GitHub URL"
2. User enters public GitHub URL (e.g., `https://github.com/owner/repo`)
3. User selects **Diagram Type** and **Node Theme**
4. Backend parses URL and fetches repository tree via GitHub API
5. Backend selects key files (package.json, tsconfig, entry points)
6. AI analyzes codebase structure and tech stack
7. AI generates enhanced diagram prompt based on analysis
8. Provider generates diagram with `related_files` metadata for nodes
9. Frontend renders diagram with interactive tooltips

---

## Workflow 9: Node Theme Update (NEW)
*(Visual Customization)*

1. User selects a new **Node Theme** (e.g., "Technical") from the style toolbar
2. Frontend updates the global `StyleState`
3. `MermaidRenderer` detects the change
4. Renderer applies new `classDef` and `style` blocks to the *existing* Mermaid source
5. Diagram re-renders instantly without calling the AI or backend

---

## Workflow 4: Conversational Refinement (Updated)

1. User sends follow-up (e.g., "Add accessibility testing layer")
2. Backend classifies intent (PATCH, ADD, REMOVE, etc.)
3. AI loads previous context (Design Prompt or Codebase Analysis)
4. AI generates Mermaid patch + new node metadata
5. For codebase diagrams, new nodes are mapped to repo paths where possible
6. New diagram version created and rendered

---

## Workflow 6: Export (Updated)

1. User clicks export action
2. User selects format:
    - **MMD**: Raw Mermaid source file download
    - **JSON**: Full structured data (topology, metadata, style) download
3. System generates file and triggers browser download
4. Success feedback shown (toast notification)

---

## Workflow 7: Error Recovery (Updated)

1. GitHub API rate limit hit or private repo detected
2. Backend returns specific error code (`GITHUB_RATE_LIMIT`, `GITHUB_REPO_NOT_FOUND`)
3. Frontend shows mode-specific error with guidance (e.g., "Repository is private or non-existent")
4. AI-related generation errors trigger retry logic once before failing

---

## Workflow 10: Refresh Restore (NEW)

1. User refreshes the browser page
2. `WorkspacePage` calls `hydrateFromStorage()` on mount
3. Storage adapter reads `localStorage` key `ai-design-system-diagram-assistant:workspace:v1`
4. Schema version is validated; loading state is reset to `idle`
5. Zustand store is hydrated with persisted conversation, diagram, versions, and settings
6. UI renders the restored state; no API calls are triggered automatically

---

## Workflow 11: New Conversation (NEW)

1. User clicks the **New Conversation** button in the header
2. If active work exists (messages or diagram), a confirmation dialog appears
3. `startNewConversation()` creates a fresh conversation ID
4. Current messages, diagram, versions, prompts, and repo URL are cleared
5. Global preferences (provider, theme, style defaults) are preserved
6. Clean state is persisted to `localStorage`
7. UI resets to empty prompt input state
