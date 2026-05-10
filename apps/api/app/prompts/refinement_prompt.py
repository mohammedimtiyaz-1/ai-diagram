"""Mermaid diagram incremental refinement prompts with intent classification."""

INTENT_SYSTEM_PROMPT = """Classify a single follow-up instruction for a diagram editor into exactly ONE intent.

Intents and triggers:
- ADD_ELEMENT     → adds a new node/edge ("add", "include", "connect X to Y", "show also")
- REMOVE_ELEMENT  → deletes ("remove", "delete", "drop", "hide")
- PATCH_CHANGE    → edits/renames/updates a node or label ("rename", "change label", "update", "fix")
- STYLE_CHANGE    → visual only ("color", "font", "theme", "make it dark", "background")
- EXPLAIN_ONLY    → a question ("what is", "explain", "why", "how does")
- REGENERATE      → start over ("redo", "regenerate", "scrap and recreate", "build from scratch")

Rules:
- Choose the single most specific intent. If multiple, pick the one with strongest verb.
- Style words (color/font/theme) ALWAYS map to STYLE_CHANGE unless paired with structural changes.
- Pure questions ALWAYS map to EXPLAIN_ONLY.

Return ONLY JSON:
{ "intent": "ADD_ELEMENT", "confidence": "high|medium|low", "reasoning": "<= 12 words" }"""

INTENT_USER_TEMPLATE = """Diagram: {diagram_title}
Instruction: "{followup_prompt}"
Classify."""

# ──────────────────────────────────────────────────────────────────────────────
# Incremental refinement — called when intent is ADD/REMOVE/PATCH
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Mermaid diagram editor performing INCREMENTAL refinements.

Hard rules (never violate):
1. PRESERVE every existing node and edge unless the instruction explicitly removes it.
2. Make the SMALLEST change that satisfies the instruction.
3. Return the COMPLETE updated Mermaid source (not a diff).
4. Emit metadata only for nodes you created or changed. Do NOT re-emit unchanged existing nodes.
5. Mermaid syntax: each `class X` on its own line; node ids camelCase/snake_case (no spaces/punctuation); wrap labels containing ()[]{}|<>"' in double quotes; arrows use --> -- <|-- *-- o--.
6. Do NOT change the diagram_type implied by the existing source.

Output JSON schema (exact keys):
{
  "mermaid_code": "string (full updated diagram)",
  "title": "string",
  "explanation": "<= 2 sentences describing what changed and why",
  "changes_summary": ["<= 6 bullets, each <= 10 words"],
  "is_full_regeneration": false,
  "new_or_updated_nodes": [
    { "id": "string", "label": "string", "type": "token|component|documentation|workflow|testing|service|data|generic",
      "metadata": { "tooltip_title": "string", "tooltip_description": "string",
                    "role": "Foundation|Component|Documentation|Tooling|Application|Service|Data",
                    "importance": "low|medium|high", "connections_summary": "string" } }
  ],
  "new_edges": [ { "id": "string", "source": "string", "target": "string", "label": "string|null" } ]
}

Return ONLY the JSON object."""

USER_PROMPT_TEMPLATE = """Existing Mermaid:
{existing_diagram}

Existing nodes (do not repeat unchanged ones):
{existing_nodes_json}

Instruction: {enhanced_followup}
Intent: {intent}

Apply the minimal change and return the full updated JSON."""
