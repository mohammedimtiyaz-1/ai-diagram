# Testing Strategy: AI Design System Diagram Assistant

---

## Backend Tests

### Schema Validation
- Pydantic model tests for all request/response schemas
- Invalid input rejection (short prompts, missing fields, invalid types)
- Diagram type enum validation
- Conversation model integrity

### Codebase Analysis (NEW)
- GitHub URL parser handles owner/repo extraction
- Tree fetcher filters noise correctly
- Stack detection identifies React, Next.js, FastAPI, etc.
- AI analyzer returns valid architecture summary
- Prompt enhancer generates specific codebase-focused prompt

### Diagram Generation API
- MermaidProvider returns valid Mermaid syntax
- Generated Mermaid is parseable by Mermaid.js
- Retry mechanism works on first failure
- Diagram metadata populated correctly (including `related_files`)

### Refinement API
- Follow-up modifies existing diagram
- Context preserved (Codebase summary used in refinement)
- Version number incremented

---

## Frontend Tests

### Input Mode Flow (NEW)
- Toggle between Prompt and GitHub modes works
- Input field placeholder changes based on mode
- GitHub mode shows Diagram Type and Node Theme selectors
- URL validation for GitHub links

### Codebase Analysis Flow (NEW)
- Analyze button triggers analysis API
- Loading state shows "Analyzing repository..."
- Results populate the workspace appropriately

### Node Tooltips & Themes (NEW)
- `related_files` displayed in tooltips for codebase diagrams
- Node Theme dropdown updates diagram visuals immediately (local CSS/Mermaid update)
- Node Theme persists after refinement

### Diagram Rendering
- Mermaid source renders without error
- Invalid Mermaid shows error state (no crash)

---

## AI Quality Tests

### Codebase Analysis Quality
- Detected stack matches actual repository dependencies
- Major modules are logical based on file structure
- Architecture summary accurately describes project type (monorepo, etc.)

### Diagram Generation Quality
- Diagrams represent actual folder/file structure (for folder-structure diagrams)
- Architecture diagrams show logical service boundaries
- API flow diagrams identify actual route files
- Node metadata (`related_files`) points to valid repo paths

---

## Demo Scenarios

### Scenario 6: GitHub Architecture (NEW)
- Input URL: `https://github.com/microsoft/TypeScript` (or a smaller known repo)
- Diagram Type: Architecture
- Verify: Renders logical architecture, tooltips show related source files

### Scenario 7: Folder Structure Visualization (NEW)
- Input URL: `https://github.com/facebook/react`
- Diagram Type: Folder Structure
- Verify: Renders high-level folder map (src, packages, etc.)

### Scenario 8: Node Theme Customization (NEW)
- Generate a diagram, then change Node Theme to "Technical"
- Verify: Sharp corners, mono font, high contrast, no re-regeneration from AI

### Scenario 9: Codebase Refinement (NEW)
- Generate codebase diagram
- Follow-up: "Add the deployment flow based on the GitHub actions in the repo"
- Verify: Diagram updated to include CI/CD nodes, version 2 created

---

## Test Metrics (Updated)

| Metric | Target |
|--------|--------|
| GitHub analysis success rate | ≥95% |
| Codebase stack detection accuracy | ≥90% |
| Node Theme update time | <100ms |
| Mermaid validity rate (Codebase) | 100% |
| Related Files accuracy | ≥80% |
