# AI Workflow Design: AI Design System Diagram Assistant

## Overview

The AI layer handles four main workflows:
1. **Prompt Enhancement** — improve raw user input for better diagrams
2. **Codebase Analysis (NEW)** — analyze GitHub repositories to visualize actual code
3. **Diagram Generation** — create Mermaid diagrams from enhanced prompts or code analysis
4. **Diagram Refinement** — modify existing diagrams based on follow-up instructions

All AI calls use OpenAI GPT-4o with `response_format: { type: "json_object" }` for structured output.

---

## Stage 1: Input Analysis & Intent Classification

Before processing, the system classifies the user's intent.

| Intent | Criteria | Strategy |
|--------|----------|----------|
| **NEW_DIAGRAM** | No active conversation or "start over" keywords | Full generation (Flow A) |
| **CODEBASE_ANALYSIS** | GitHub URL provided in input | Codebase analysis (Flow B) |
| **PATCH_CHANGE** | Specific edit to existing node/edge | Incremental Mermaid update |
| **ADD_ELEMENT** | Request to add new component/layer | Append to Mermaid source |
| **REMOVE_ELEMENT** | Request to delete component/layer | Remove from Mermaid source |
| **STYLE_CHANGE** | Color, font, or theme request | Visual Style state update |
| **REGENERATE** | "Ignore previous and start over" | Full replacement |

---

## Stage 2: Codebase Analysis Workflow (Flow B - NEW)

**Purpose**: Convert a GitHub repository into a high-quality diagram prompt.

### 2.1 Repository Extraction (Non-AI)
- Extract `owner` and `repo` from URL.
- Fetch recursive file tree via GitHub API.
- Filter out noise (node_modules, dist, .git, images).
- Identify "Important Files" (package.json, tsconfig, README, entry points, config files).

### 2.2 Content Preparation (Non-AI)
- Read top 500 lines of `package.json` and `README.md`.
- Read directory structure (up to 3 levels deep).
- Truncate and concatenate into an "Analysis Context" string.

### 2.3 Architecture Summary (AI Call #1 - Analyzer)
**Input**: Analysis Context + Filtered Tree.
**Output**:
- `detected_stack`: List of technologies
- `major_modules`: Key logical boundaries
- `architecture_summary`: Detailed plain-English summary
- `important_flows`: Key interaction patterns detected

### 2.4 Diagram Prompt Generation (AI Call #2 - Enhancer)
**Input**: Architecture Summary + Selected Diagram Type.
**Output**:
- `enhanced_prompt`: Structured instruction for the diagram generator.
- `metadata`: Entities and relationships specific to the codebase.

---

## Stage 3: Prompt Enhancement & Metadata Enrichment (Flow A)

For Flow A (Prompt to Diagram), the AI rewrites raw input into a structured instruction set.

**Metadata Enrichment**:
For every node identified, the AI must generate:
1. `tooltip_title`: Clear name
2. `tooltip_description`: Brief definition
3. `role`: Structural purpose
4. `importance`: low | medium | high
5. `connections_summary`: How it relates to neighbors
6. `related_files`: (For Flow B) Actual paths in the repo

---

## Stage 4: Diagram Generation Pipeline

### 4.1 Selection & Adaptation
- Use the `enhanced_prompt` (from either Flow A or Flow B).
- Select the `MermaidProvider`.
- Inject the **Node Theme** (Technical, Soft, etc.) into the generation context.

### 4.2 Mermaid Generation (AI Call)
The AI is prompted to produce:
1. Valid Mermaid source code.
2. Comprehensive Node and Edge metadata.
3. Plain-English explanation.
4. **Style overrides** corresponding to the selected Node Theme.

---

## Stage 5: Incremental Refinement Pipeline

For refinements, the engine uses a **Stabilized Context Window**:

1. **Load State**: Retrieve `vN` Mermaid source, nodes, and edges.
2. **Intent Match**: If the user asks to change the "Diagram Type" (e.g., "Show this as a sequence diagram"), classification shifts to `FULL_REGENERATION`.
3. **Topology Preservation**: For standard refinements, the system enforces that nodes not mentioned in the refinement remain unchanged.
4. **Style Preservation**: Visual style and Node Theme settings from `vN` are applied to `vN+1`.

---

## Stage 6: Node Theme Implementation

Node themes are applied as **Mermaid Class Definitions** (`classDef`) and **Style Statements**.

| Theme | Mermaid Style Strategy |
|-------|-----------------------|
| **Technical** | Sharp corners, mono font, high contrast borders, no fill. |
| **Soft** | Large border-radius (pill shape), pastel backgrounds, minimal borders. |
| **Colorful** | Assign different `classDef` colors based on node `type` (token, component, etc.). |
| **Dark** | Dark background, neon borders, white/neon text. |
| **Enterprise** | Formal navy/gray tones, square corners, bold headers. |

Changing a Node Theme locally (without AI) involves updating the `classDef` block in the existing Mermaid source.

---

## Stage 7: Context Preservation Strategy

### Codebase Context
- For codebase-generated diagrams, the `Architecture Summary` is stored in the conversation context.
- Follow-up refinements use this summary to ensure they remain grounded in the actual codebase structure.

---

## Stage 8: Error Categories and Recovery

| Error | Detection | Recovery |
|-------|-----------|----------|
| GITHUB_NOT_FOUND | GitHub API 404 | Return friendly "Repo not found" error. |
| RATE_LIMIT | GitHub API 403/429 | Suggest waiting or trying a smaller repo. |
| ANALYZER_FAILED | AI output invalid | Retry analysis with more tree context. |
| NO_TECH_STACK | AI cannot detect stack | Ask user to provide stack details manually. |
