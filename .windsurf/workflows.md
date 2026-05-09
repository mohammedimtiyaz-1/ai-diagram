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
