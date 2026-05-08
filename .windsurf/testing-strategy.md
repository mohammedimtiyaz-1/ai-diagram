# Testing Strategy: AI Design System Diagram Assistant

---

## Backend Tests

### Schema Validation
- Pydantic model tests for all request/response schemas
- Invalid input rejection (short prompts, missing fields, invalid types)
- Diagram type enum validation
- Conversation model integrity

### Prompt Enhancement API
- Enhancement returns valid JSON matching schema
- All 5 example inputs produce sensible enhanced prompts
- Entity extraction accuracy
- Diagram type classification correctness
- Assumption flagging works
- Error handling for empty/gibberish input

### Diagram Generation API
- MermaidProvider returns valid Mermaid syntax
- Generated Mermaid is parseable by Mermaid.js
- Retry mechanism works on first failure
- Second failure returns proper error response
- Diagram metadata populated correctly
- Conversation ID assigned on first generation

### Refinement API
- Follow-up modifies existing diagram (not generates from scratch)
- Context preserved (new diagram references previous)
- Changes summary accurately reflects modifications
- Version number incremented
- Invalid follow-up returns helpful error

### Provider Abstraction
- MermaidProvider implements full interface
- Provider can be swapped without changing API layer
- Each provider returns normalized DiagramResult

### Export Service
- Mermaid export matches current diagram state
- JSON export includes all fields
- Prompt export returns enhanced prompt
- Explanation export returns diagram explanation

---

## Frontend Tests

### Text Input Flow
- Input validates minimum length (10 chars)
- Input rejects exceeding maximum (2000 chars)
- Diagram type selector works
- Submit disabled when invalid
- Example prompts populate input on click
- Submit triggers API call

### Voice Transcript Flow
- Mic button visible on supported browsers
- Recording state shown while active
- Transcript appears after recording stops
- Transcript is editable
- Confirm sends transcript to generation
- Cancel clears transcript
- Graceful fallback on unsupported browsers

### Enhanced Prompt Preview
- Shows both raw and enhanced prompt
- Copy button works
- Toggle between raw/enhanced
- Displays loading while enhancing

### Diagram Rendering
- Mermaid source renders without error
- Diagram title displayed
- Diagram explanation displayed
- Invalid Mermaid shows error state (no crash)
- Diagram scales reasonably in viewport

### Chat Refinement
- Follow-up input available after diagram exists
- Message appears in conversation history
- New diagram version renders after refinement
- Previous messages visible in history

### Version History
- Shows list of diagram versions
- Each version shows version number and timestamp
- Clicking version shows that diagram
- Current version highlighted

### Export Actions
- Mermaid copy works
- JSON copy works
- Enhanced prompt copy works
- Success feedback shown (toast)
- All exports reflect current diagram state

---

## AI Quality Tests

### Prompt Enhancement Quality
- Enhanced prompt is more specific than raw input
- Entities extracted match design-system domain
- Relationships are logical
- Diagram type recommendation is appropriate
- Assumptions are reasonable and flagged

### Diagram Generation Quality
- Generated diagrams have 5-15 nodes (readable)
- Node labels are meaningful (not generic "Node1")
- Relationships reflect actual design-system patterns
- Mermaid syntax is valid
- Diagram matches enhanced prompt intent

### Refinement Consistency
- Refined diagram preserves unchanged elements
- Only requested additions/changes appear
- Diagram doesn't grow unbounded
- Context maintained across 3+ refinements
- Explanation accurately describes changes

### Invalid Output Recovery
- Malformed JSON triggers repair prompt
- Invalid Mermaid triggers repair prompt
- Repair prompt produces valid output
- If repair fails, error is graceful

---

## Manual QA Checklist

### Demo Scenario 1: Design System Architecture
- Input: "Create a design system architecture for a React and Next.js app with tokens, components, themes, and documentation."
- Expected: Multi-layer architecture diagram
- Verify: Renders, is readable, entities correct

### Demo Scenario 2: Component Hierarchy
- Input: "Show how buttons, forms, modals, and layout components should be structured."
- Expected: Hierarchical component diagram
- Verify: Hierarchy is logical, atomic design levels if present

### Demo Scenario 3: Token Architecture
- Input: "Generate a diagram for design tokens, semantic tokens, component variants, and Tailwind integration."
- Expected: Token flow diagram
- Verify: Pipeline shows transformation steps

### Demo Scenario 4: Design-to-Code Workflow
- Input: "Create a design system workflow showing Figma tokens, code tokens, React components, Storybook, and app usage."
- Expected: Workflow diagram left-to-right
- Verify: Tools and steps connected logically

### Demo Scenario 5: Conversational Refinement
- Start: Generate Scenario 1
- Follow-up: "Add accessibility testing and documentation layers."
- Verify: Original preserved, new layers added, version 2 created

### Edge Cases
- Empty input → validation error shown
- Very short input ("tokens") → enhancement adds context, or error
- Gibberish input → helpful error message
- Very long input (2000 chars) → works within limits
- Rapid successive submits → loading state prevents double-submit
- Network failure → error state with retry option
- Mobile viewport → layout doesn't break (desktop-first but no crash)

---

## Test Metrics

| Metric | Target |
|--------|--------|
| Schema tests passing | 100% |
| API endpoint tests passing | 100% |
| Enhancement accuracy (manual review) | ≥80% |
| Diagram generation success rate | ≥80% |
| Mermaid validity rate | 100% (after retry) |
| Refinement accuracy | ≥70% |
| UI states covered (loading/error/empty) | 100% |
| Demo scenarios passing | 5/5 |
