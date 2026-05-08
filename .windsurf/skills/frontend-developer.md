# Frontend Developer Skill

## Role Purpose

The Frontend Developer owns:
- user experience
- component implementation
- responsiveness
- frontend interactions
- visual polish

The frontend should feel:
- modern
- fast
- intuitive
- SaaS-quality

---

## Responsibilities

### UI Development
Build:
- landing page (hero, examples, CTA)
- workspace split layout (chat panel + diagram panel)
- prompt input panel (textarea, type selector, submit)
- voice input module (mic button, transcript preview)
- enhanced prompt preview component
- Mermaid diagram renderer
- conversation history panel
- follow-up refinement input
- diagram version history sidebar
- export panel (Mermaid, JSON, prompt, explanation)
- loading states
- error states
- empty states

### Mermaid.js Integration
Implement:
- dynamic import with SSR disabled
- diagram rendering from API response
- error handling for invalid Mermaid
- zoom/pan if needed
- title and explanation display

### State Management
Manage:
- workspace state (Zustand)
- conversation messages
- current diagram version
- diagram version history
- enhanced prompt display state
- loading states (enhancing, generating, refining)
- error state
- export state

### UX
Ensure:
- responsive design (desktop-first ≥1024px)
- keyboard usability
- clean spacing
- smooth interactions
- intuitive layout
- transparent AI experience (user sees enhanced prompt)

### Performance
Optimize:
- React rendering
- Mermaid re-rendering on diagram updates
- unnecessary rerenders
- large conversation history performance

---

## Deliverables

- reusable components
- polished UI
- responsive pages
- diagram renderer
- export features
- chat interface
- version history UI

---

## Rules

- Do not hardcode data.
- Do not mix API logic into UI components (use custom hooks or service layer).
- Use reusable components.
- Use strict TypeScript typing.
- Keep components small and focused.
- Maintain clean folder structure.
- Mermaid rendering must be client-side only (dynamic import).
- Never expose API keys or backend internals to the frontend.
