# AI Design System Diagram Assistant — Feature Modules

Modules organized by **user-facing capability**, not technical implementation.

---

## Frontend Modules

### Module 10: Codebase Analysis Input (NEW)

**User Goal**: Visualize the architecture of an existing GitHub repository.

**Inputs**: GitHub URL + Diagram Type + Node Theme
**Outputs**: Codebase analysis summary + generated diagram

**Capabilities**:
- Input Mode Toggle (Design Prompt vs GitHub URL)
- GitHub URL validator
- Codebase-specific diagram type selector (Architecture, Folder Map, API Flow)
- Node Theme selector (Technical, Soft, Dark, etc.)
- Progress indicators for analysis phase

### Module 11: Theme Controller (NEW)

**User Goal**: Instantly customize the visual style of the diagram.

**Inputs**: Theme selection from Style Toolbar
**Outputs**: Instantly updated diagram visual without AI lag

**Capabilities**:
- Bottom ribbon (toolbar) for style controls
- Instant mapping of themes to Mermaid `classDef` and CSS variables
- State persistence (theme stays active during refinement)

---

## Backend Modules

### Module B9: Codebase Analysis Service (NEW)

**Purpose**: Extract architecture insights from a repository tree.

**Capabilities**:
- Recursive tree fetching via GitHub API
- Tech stack detection (React, Next.js, FastAPI, etc.)
- Important file identification (package.json, entry points)
- AI-driven architecture summarization
- Diagram prompt generation from analysis

### Module B10: Theme Mapper Service (NEW)

**Purpose**: Map abstract themes to technical styling rules.

**Capabilities**:
- Store theme-to-Mermaid-style configurations
- Provide style snippets for different diagram types
- Update diagram style metadata

---

## Post-MVP Modules (Updated)

| Module | Reason Deferred |
|--------|-----------------|
| User Authentication | Deferred for portfolio simplicity |
| Private Repositories | Requires OAuth and security complexity |
| Git Provider Extension | MVP focuses on GitHub |
