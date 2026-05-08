# Development Plan: AI Design System Diagram Assistant

## Guiding Principles

1. **Build small** — each milestone delivers a working increment
2. **Start with Mermaid** — simplest provider, renders in browser
3. **Prompt enhancement first** — the differentiator, build it early
4. **Chat refinement is core** — not a nice-to-have, implement before polish
5. **Voice after text** — text flow must be stable first
6. **Polish last** — UI polish happens after features work
7. **Document as portfolio** — README and case study are final deliverables

---

## Phase 1: Foundation (Milestones 1-2)

### Milestone 1: Context & Planning ✅
**Deliverables**: All planning files
**Acceptance**: All `.windsurf/` and `docs/` files reflect current direction
**Status**: Complete

### Milestone 2: Project Setup
**Owner**: Architect + Developers
**Estimated effort**: 1-2 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Monorepo structure | `/frontend` + `/backend` folders | Both exist with configs |
| Next.js init | App Router, TypeScript, Tailwind, shadcn/ui | `npm run dev` works |
| FastAPI init | Pydantic, uvicorn, health endpoint | `/health` returns 200 |
| Environment | `.env.example`, `.gitignore` | Documented, no secrets committed |
| Dev scripts | Makefile or package.json scripts | Single command starts both |
| README | Basic setup instructions | New dev can start in 5 min |

**Risks**: None (standard setup)

---

## Phase 2: Backend Core (Milestones 3-5)

### Milestone 3: Schemas & Provider Abstraction
**Owner**: Architect + Backend Developer
**Estimated effort**: 2-3 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Pydantic models | All schemas from API_CONTRACTS.md | Models validate correctly |
| Provider interface | Abstract `DiagramProvider` class | Interface documented |
| Provider registry | Factory/registry for providers | Can instantiate by name |
| MermaidProvider stub | Returns mock diagram | Implements full interface |
| Tests | Schema validation tests | 100% pass |

**Risks**: Over-engineering the provider interface
**Mitigation**: Keep it to 3 methods only, don't add features speculatively

### Milestone 4: Prompt Enhancement API
**Owner**: AI Workflow Engineer + Backend Developer
**Estimated effort**: 3-4 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Enhancement service | Calls OpenAI, returns structured result | Works for 5 example inputs |
| Prompt template | Design-system enhancement prompt | Produces useful output |
| Entity extraction | Extracts design-system entities | Entities are relevant |
| Type classification | Detects diagram type | Correct for 4/5 examples |
| API endpoint | `POST /api/prompts/enhance` | Returns valid schema |
| Error handling | Invalid input, AI failure | Graceful error responses |
| Tests | Enhancement quality tests | 5 examples tested |

**Risks**: Prompt quality; AI returning inconsistent formats
**Mitigation**: Strict JSON schema enforcement; repair/retry on invalid

### Milestone 5: Mermaid Provider MVP
**Owner**: AI Workflow Engineer + Backend Developer
**Estimated effort**: 3-4 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| MermaidProvider (real) | Calls OpenAI with diagram prompt | Returns valid Mermaid |
| Prompt templates | Per-diagram-type generation prompts | 4 types supported |
| Mermaid validation | Basic syntax check | Catches obvious errors |
| Retry mechanism | Retry once on failure | Second attempt works or errors |
| Generate endpoint | `POST /api/diagrams/generate` | End-to-end works |
| Conversation init | Create conversation on first generate | conversation_id returned |
| Tests | Generation tests for each type | 4/5 produce valid Mermaid |

**Risks**: Mermaid syntax validity; AI producing unrenderable output
**Mitigation**: Basic Mermaid parser validation; repair prompt on failure

---

## Phase 3: Frontend Core (Milestone 6-7)

### Milestone 6: Next.js Workspace UI
**Owner**: Frontend Developer
**Estimated effort**: 4-5 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Landing page | Hero, examples, CTA | Polished, responsive |
| Workspace layout | Split panel (chat + diagram) | Renders correctly |
| Prompt input | Textarea, type selector, submit | Validates, submits to API |
| Example prompts | 3-5 clickable DS examples | Populate input on click |
| Loading state | Spinner during API calls | Shows/hides correctly |
| Error state | Error message with suggestion | Renders on API error |
| Empty state | Guidance before first diagram | Shows on initial load |
| Zustand store | Workspace state management | State updates correctly |

**Risks**: Mermaid rendering library integration complexity
**Mitigation**: Use simple `mermaid.render()` API; fallback to code block on failure

### Milestone 7: Diagram Rendering & Enhancement Preview
**Owner**: Frontend Developer
**Estimated effort**: 3-4 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Mermaid.js integration | Render diagram from source | Diagram visible |
| Title/explanation display | Show below/above diagram | Readable |
| Enhanced prompt preview | Show raw vs enhanced | Side-by-side or toggle |
| Entities display | Show extracted entities | Visible list |
| Copy enhanced prompt | Copy button | Clipboard works |
| Error rendering | Invalid Mermaid fallback | Shows error, not crash |

**Risks**: Mermaid.js SSR compatibility with Next.js
**Mitigation**: Dynamic import with `ssr: false`; render client-side only

--- [ ] Phase 4: AI Prompt Enhancement (Tooltip Metadata)
- [ ] Phase 5: Mermaid Diagram Generation (with nodes/edges/metadata)
- [ ] Phase 6: Conversational Refinement (Incremental Patching)
- [ ] Phase 7: Node Tooltip UI (Hover interaction)
- [ ] Phase 8: Diagram Style Toolbar (Visual customizations)
- [ ] Phase 9: Voice Input Integration
- [ ] Phase 10: Export, Persistence & Polish
- [ ] Phase 11: Final Testing & Documentation

---

## 4. Detailed Phase Breakdown

### Phase 4: AI Prompt Enhancement (Tooltip Metadata)
- Update enhancement prompt to require node metadata (role, description, importance)
- Test enhancement with diverse design system scenarios

### Phase 5: Mermaid Diagram Generation
- Server-side generation of Mermaid + structured node/edge list
- Validation of Mermaid syntax and metadata presence
- Response includes full topology + metadata

### Phase 6: Conversational Refinement (Incremental)
- Implement intent classification (NEW, PATCH, STYLE, etc.)
- Create "Minimal Edit" prompt for refinement
- Enforce topology preservation for unchanged nodes
- Versioning support for incremental updates

### Phase 7: Node Tooltip UI
- Frontend hover interaction for Mermaid nodes
- Tooltip component showing title, role, connection summary, and description
- Clean, non-intrusive popover design

### Phase 8: Diagram Style Toolbar
- Implement bottom ribbon/toolbar
- Controls for font family, size, color, and background colors
- Immediate preview update without AI calls
- Persistent style state for the current diagram version

---

## Phase 4: Refinement & Interaction (Milestone 8-9)

### Milestone 8: Conversational Refinement
**Owner**: AI Workflow Engineer + Backend + Frontend
**Estimated effort**: 4-5 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Conversation context service | In-memory message storage | Messages persist in session |
| Refinement prompt template | Context-aware follow-up | Preserves existing diagram |
| Refine endpoint | `POST /api/diagrams/refine` | Returns updated diagram |
| Versioning service | Track versions in-memory | Version list works |
| Follow-up UI | Input below conversation | Submits refinement |
| Conversation history | Display messages | User/assistant styled |
| Version history UI | List versions, switch | Clicking shows version |
| Context summarization | Summarize long conversations | Works after 5+ messages |

**Risks**: Context drift (diagram diverging from conversation intent)
**Mitigation**: Always include current diagram source in refinement prompt

### Milestone 9: Voice Input
**Owner**: Frontend Developer
**Estimated effort**: 2-3 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Web Speech API integration | Browser speech recognition | Records in Chrome/Edge |
| Mic button | Start/stop recording | Visual state indicator |
| Transcript display | Show in editable textarea | Editable before submit |
| Confirm/cancel | Actions on transcript | Confirm → enhancement pipeline |
| Permission handling | Request mic permission | Graceful on denied |
| Unsupported fallback | Hide/disable on unsupported | No crash on Safari/Firefox |

**Risks**: Web Speech API browser support inconsistency
**Mitigation**: Feature detection; hide button if unsupported

---

## Phase 5: Export & Polish (Milestone 10-11)

### Milestone 10: Export & Version History
**Owner**: Frontend + Backend Developer
**Estimated effort**: 2-3 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Export endpoint | `POST /api/diagrams/export` | Returns formatted content |
| Export panel UI | Buttons for each format | All formats work |
| Copy to clipboard | One-click copy | Toast on success |
| Version history sidebar | List + switch | Navigation works |

### Milestone 11: Testing & Polish
**Owner**: QA + All Developers
**Estimated effort**: 3-4 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| Backend unit tests | Schemas, services, endpoints | 100% critical paths |
| Frontend smoke tests | Input, rendering, export | No crashes |
| AI quality tests | 5 demo scenarios | 80%+ accuracy |
| Manual QA | Full checklist execution | All pass |
| UI polish | Spacing, transitions, responsive | Portfolio-ready |
| Error review | All error messages checked | Actionable, no internals |
| Performance | Generation <15s | Measured and documented |

---

## Phase 6: Documentation (Milestone 12)

### Milestone 12: Documentation & Portfolio
**Owner**: Documentation Engineer
**Estimated effort**: 2-3 hours

**Tasks**:
| Task | Description | Done When |
|------|-------------|-----------|
| README | Complete setup + usage | 5-minute onboarding |
| Architecture docs | Update with final state | Matches implementation |
| Portfolio case study | Problem → approach → result | Presentation-ready |
| Screenshots/GIF | Visual demo | Added to README |
| API docs | Final endpoint documentation | Matches actual API |

---

## Total Estimated Effort

| Phase | Milestones | Estimated Hours |
|-------|-----------|-----------------|
| Foundation | 1-2 | 1-2 |
| Backend Core | 3-5 | 8-11 |
| Frontend Core | 6-7 | 7-9 |
| Refinement | 8-9 | 6-8 |
| Export & Polish | 10-11 | 5-7 |
| Documentation | 12 | 2-3 |
| **Total** | **12** | **29-40 hours** |

---

## Scope Control Rules

1. **No feature additions** until all milestones are complete
2. **Cut voice before refinement** if time is tight (voice is P1; refinement is P0)
3. **One provider only** — do not add Eraser until Mermaid is solid
4. **No database** unless specifically needed for a demo feature
5. **No auth** — stateless is acceptable for portfolio
6. **Polish is last** — ugly and working beats pretty and broken

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| AI output inconsistency | Medium | High | Strict JSON schema; repair/retry |
| Mermaid rendering issues in Next.js | Medium | Medium | Dynamic import, client-only render |
| Prompt enhancement doesn't add value | High | Low | Test with 5 examples before integrating |
| Scope creep | High | Medium | Strict scope rules; task board discipline |
| OpenAI rate limits during development | Low | Low | Cache responses locally during dev |
| Web Speech API browser incompatibility | Low | Medium | Feature detection; graceful fallback |
