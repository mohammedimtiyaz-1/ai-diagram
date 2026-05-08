# Workflows: AI Design System Diagram Assistant

---

## Workflow 1: Text to Design System Diagram

**Trigger**: User types a design-system description and submits.

**Steps**:
1. User enters text in chat input panel
2. Frontend validates input (≥10 chars, ≤2000 chars)
3. Frontend sends raw prompt to `/api/prompts/enhance`
4. AI enhances prompt (adds entities, relationships, structure, clarity)
5. Frontend shows enhanced prompt preview
6. Frontend sends enhanced prompt to `/api/diagrams/generate`
7. Provider generates diagram (Mermaid syntax)
8. Frontend renders diagram in preview panel
9. Conversation initialized with context

---

## Workflow 2: Voice to Design System Diagram

**Trigger**: User clicks microphone and speaks.

**Steps**:
1. User clicks mic button — browser requests permission
2. Speech recognition captures audio
3. Transcript displayed in editable text area
4. User reviews/edits transcript
5. User confirms → transcript sent through Workflow 1 (step 2 onward)
6. Diagram generated and rendered

---

## Workflow 3: Prompt Enhancement

**Trigger**: Raw user input received by backend.

**Steps**:
1. Raw prompt received
2. Design-system intent extracted (entities, relationships)
3. Missing context inferred carefully (flagged as assumptions)
4. Diagram type classified (architecture / hierarchy / token / workflow)
5. Prompt rewritten for diagram generation clarity
6. Enhanced prompt returned with:
   - diagram goal
   - entities list
   - relationships
   - recommended type
   - visual structure hints
   - assumptions made

---

## Workflow 4: Conversational Refinement

**Trigger**: User sends follow-up message after diagram exists.

**Steps**:
1. User types follow-up (e.g., "Add accessibility testing layer")
2. Frontend sends to `/api/diagrams/refine` with conversation_id and current diagram
3. AI loads previous context (original prompt, enhanced prompt, diagram, messages)
4. Follow-up is enhanced in context of existing diagram
5. Provider generates updated diagram
6. New diagram version created
7. Frontend renders new version
8. Version history updated

---

## Workflow 5: Provider Switching

**Trigger**: User selects different provider (future feature).

**Steps**:
1. Same enhanced prompt can be sent to different providers
2. Provider adapter translates prompt to provider-specific format
3. Provider returns normalized diagram response
4. Frontend renders regardless of provider used
5. Frontend remains provider-agnostic

---

## Workflow 6: Export

**Trigger**: User clicks export action.

**Steps**:
1. User selects export format (Mermaid / JSON / prompt / explanation)
2. System retrieves current diagram state
3. Format-specific export generated
4. Content displayed and/or copied to clipboard
5. Success feedback shown (toast notification)

---

## Workflow 7: Error Recovery

**Trigger**: AI returns invalid or unusable diagram.

**Steps**:
1. Diagram provider returns invalid output
2. Backend validates output against schema
3. If invalid → retry once with repair prompt
4. If still invalid → return clear error to frontend
5. Frontend shows actionable error message
6. User can rephrase or try different diagram type
7. Previous valid diagram remains visible if exists
