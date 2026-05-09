import asyncio
import json
import logging
import re
import uuid

from app.core.config import settings
from app.core.openai_client import OpenAIClient
from app.core.errors import AiTimeoutError
from app.prompts.mermaid_prompt import SYSTEM_PROMPT as GENERATION_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE as GENERATION_USER_PROMPT_TEMPLATE
from app.prompts.refinement_prompt import (
    INTENT_SYSTEM_PROMPT,
    INTENT_USER_TEMPLATE,
    SYSTEM_PROMPT as REFINEMENT_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as REFINEMENT_USER_PROMPT_TEMPLATE,
)
from app.prompts.codebase_prompt import CODEBASE_GENERATION_SYSTEM_PROMPT
from app.providers.base import DiagramContext, DiagramProvider, DiagramResult
from app.schemas.diagram import DiagramEdge, DiagramNode, DiagramStyle, NodeMetadata, NodeStyle, EdgeMetadata, EdgeStyle

logger = logging.getLogger(__name__)


class MermaidProvider(DiagramProvider):
    name = "mermaid"

    def __init__(self, max_retries: int = 1):
        self.max_retries = max_retries

    # ──────────────────────────────────────────────────────────────────────────
    # Public: generate_diagram
    # ──────────────────────────────────────────────────────────────────────────

    async def generate_diagram(
        self,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        """Generate a Mermaid diagram with full node metadata."""
        client = OpenAIClient.get_async()

        entities_str = ", ".join(context.entities) if context.entities else "none"
        relationships_str = (
            ", ".join(f"{r.from_entity} → {r.to_entity} ({r.type})" for r in (context.relationships or []))
            or "none"
        )

        user_prompt = GENERATION_USER_PROMPT_TEMPLATE.format(
            enhanced_prompt=enhanced_prompt,
            diagram_type=diagram_type,
            entities=entities_str,
            relationships=relationships_str,
        )

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.7,
                        max_tokens=3000,
                    ),
                    timeout=settings.ai_timeout_seconds
                )

                content = response.choices[0].message.content
                if not content:
                    raise ValueError("OpenAI returned empty content")

                data = json.loads(content)
                mermaid_code = self._sanitize_mermaid(data.get("mermaid_code", ""))

                nodes = self._parse_nodes(data.get("nodes", []))
                edges = self._parse_edges(data.get("edges", []))

                return DiagramResult(
                    diagram_id=str(uuid.uuid4()),
                    conversation_id="",  # filled by service layer
                    title=data.get("title", "Design System Architecture"),
                    diagram_type=diagram_type or "flowchart",
                    provider=self.name,
                    diagram_source=mermaid_code,
                    diagram_format="mermaid",
                    explanation=data.get("explanation", ""),
                    nodes=nodes,
                    edges=edges,
                    style=DiagramStyle(),
                    change_intent="NEW_DIAGRAM",
                    is_full_regeneration=True,
                    metadata={"node_count": len(nodes), "edge_count": len(edges)},
                )

            except asyncio.TimeoutError:
                logger.error(f"Generation timed out after {settings.ai_timeout_seconds}s")
                raise AiTimeoutError(f"Generation timed out after {settings.ai_timeout_seconds}s. This usually happens with very complex prompts.")
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")

        logger.error(f"Generation failed after {self.max_retries + 1} attempts: {last_error}")
        return self._fallback_diagram(diagram_type)

    # ──────────────────────────────────────────────────────────────────────────
    # Public: generate_codebase_diagram
    # ──────────────────────────────────────────────────────────────────────────

    async def generate_codebase_diagram(
        self,
        analysis_summary: str,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        """Generate a codebase-aware diagram with file path metadata."""
        client = OpenAIClient.get_async()

        user_prompt = f"""
Codebase Analysis Summary:
{analysis_summary}

Diagram Goal:
{enhanced_prompt}

Diagram Type: {diagram_type}

Task:
Generate a Mermaid diagram representing the codebase architecture. 
For each node, include 'related_files' metadata which should be a list of relevant file paths from the repository.
Return valid JSON as specified in the system prompt.
"""

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": CODEBASE_GENERATION_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.4,
                        max_tokens=3500,
                    ),
                    timeout=settings.ai_timeout_seconds
                )

                content = response.choices[0].message.content
                if not content:
                    raise ValueError("OpenAI returned empty content")

                data = json.loads(content)
                mermaid_code = self._sanitize_mermaid(data.get("mermaid_code", ""))

                nodes = self._parse_nodes(data.get("nodes", []))
                edges = self._parse_edges(data.get("edges", []))

                return DiagramResult(
                    diagram_id=str(uuid.uuid4()),
                    conversation_id="",  # filled by service layer
                    title=data.get("title", "Codebase Architecture"),
                    diagram_type=diagram_type or "flowchart",
                    provider=self.name,
                    diagram_source=mermaid_code,
                    diagram_format="mermaid",
                    explanation=data.get("explanation", ""),
                    nodes=nodes,
                    edges=edges,
                    style=DiagramStyle(),
                    change_intent="NEW_DIAGRAM",
                    is_full_regeneration=True,
                    metadata={"node_count": len(nodes), "edge_count": len(edges)},
                )

            except asyncio.TimeoutError:
                logger.error(f"Codebase generation timed out after {settings.ai_timeout_seconds}s")
                raise AiTimeoutError(f"Codebase generation timed out after {settings.ai_timeout_seconds}s. Large repository analyses might take longer.")
            except Exception as e:
                last_error = e
                logger.warning(f"Codebase generation attempt {attempt + 1} failed: {e}")

        logger.error(f"Codebase generation failed after {self.max_retries + 1} attempts: {last_error}")
        return self._fallback_diagram(diagram_type)

    # ──────────────────────────────────────────────────────────────────────────
    # Public: classify_intent
    # ──────────────────────────────────────────────────────────────────────────

    async def classify_intent(self, diagram_title: str, followup_prompt: str) -> str:
        """Return intent string: ADD_ELEMENT | REMOVE_ELEMENT | PATCH_CHANGE | STYLE_CHANGE | EXPLAIN_ONLY | REGENERATE."""
        client = OpenAIClient.get_async()
        user_prompt = INTENT_USER_TEMPLATE.format(
            diagram_title=diagram_title,
            followup_prompt=followup_prompt,
        )
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": INTENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=200,
            )
            data = json.loads(response.choices[0].message.content or "{}")
            return data.get("intent", "PATCH_CHANGE")
        except Exception as e:
            logger.warning(f"Intent classification failed: {e}, defaulting to PATCH_CHANGE")
            return "PATCH_CHANGE"

    # ──────────────────────────────────────────────────────────────────────────
    # Public: refine_diagram  (incremental)
    # ──────────────────────────────────────────────────────────────────────────

    async def refine_diagram(
        self,
        existing_diagram: str,
        enhanced_followup: str,
        diagram_type: str,
        context: DiagramContext,
        existing_nodes: list[DiagramNode] | None = None,
        existing_edges: list[DiagramEdge] | None = None,
        intent: str = "PATCH_CHANGE",
        parent_diagram_id: str | None = None,
        base_diagram_id: str | None = None,
    ) -> DiagramResult:
        """Incrementally refine an existing diagram, preserving its topology."""
        client = OpenAIClient.get_async()

        # Serialize existing nodes for the prompt context
        existing_nodes_json = json.dumps(
            [n.model_dump() for n in (existing_nodes or [])], indent=2
        )

        user_prompt = REFINEMENT_USER_PROMPT_TEMPLATE.format(
            existing_diagram=existing_diagram,
            existing_nodes_json=existing_nodes_json,
            enhanced_followup=enhanced_followup,
            intent=intent,
        )

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": REFINEMENT_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.6,
                        max_tokens=3000,
                    ),
                    timeout=settings.ai_timeout_seconds
                )

                content = response.choices[0].message.content
                if not content:
                    raise ValueError("OpenAI returned empty content")

                data = json.loads(content)
                mermaid_code = self._sanitize_mermaid(data.get("mermaid_code", ""))

                # Merge: preserve existing nodes, add/update new ones
                new_parsed = self._parse_nodes(data.get("new_or_updated_nodes", []))
                new_edges = self._parse_edges(data.get("new_edges", []))
                merged_nodes = self._merge_nodes(existing_nodes or [], new_parsed)
                merged_edges = self._merge_edges(
                    existing_edges or [],
                    new_edges,
                )

                return DiagramResult(
                    diagram_id=str(uuid.uuid4()),
                    conversation_id="",  # filled by service layer
                    title=data.get("title", "Design System Architecture (Refined)"),
                    diagram_type=diagram_type or "flowchart",
                    provider=self.name,
                    diagram_source=mermaid_code,
                    diagram_format="mermaid",
                    explanation=data.get("explanation", ""),
                    changes_summary=data.get("changes_summary", []),
                    nodes=merged_nodes,
                    edges=merged_edges,
                    style=DiagramStyle(),  # style is preserved by service layer
                    change_intent=intent,
                    is_full_regeneration=data.get("is_full_regeneration", False),
                    base_diagram_id=base_diagram_id,
                    parent_diagram_id=parent_diagram_id,
                    metadata={"node_count": len(merged_nodes), "edge_count": len(merged_edges)},
                )

            except asyncio.TimeoutError:
                logger.error(f"Refinement timed out after {settings.ai_timeout_seconds}s")
                raise AiTimeoutError(f"Refinement timed out after {settings.ai_timeout_seconds}s. Complex refinements can sometimes exceed this limit.")
            except Exception as e:
                last_error = e
                logger.warning(f"Refinement attempt {attempt + 1} failed: {e}")

        logger.error(f"Refinement failed after {self.max_retries + 1} attempts: {last_error}")
        return self._fallback_refinement(existing_diagram, diagram_type, parent_diagram_id, base_diagram_id)

    # ──────────────────────────────────────────────────────────────────────────
    # Public: export_diagram
    # ──────────────────────────────────────────────────────────────────────────

    async def export_diagram(
        self,
        diagram_source: str,
        diagram_format: str,
        export_format: str,
    ) -> str:
        if export_format == "mermaid":
            return diagram_source
        elif export_format == "json":
            return json.dumps({"source": diagram_source, "format": diagram_format}, indent=2)
        return diagram_source

    # ──────────────────────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _parse_nodes(self, raw: list[dict]) -> list[DiagramNode]:
        nodes = []
        for item in raw:
            meta = item.get("metadata", {})
            nodes.append(
                DiagramNode(
                    id=item.get("id", str(uuid.uuid4())),
                    label=item.get("label", ""),
                    type=item.get("type", "generic"),
                    metadata=NodeMetadata(
                        tooltip_title=meta.get("tooltip_title", ""),
                        tooltip_description=meta.get("tooltip_description", ""),
                        role=meta.get("role", ""),
                        importance=meta.get("importance", "medium"),
                        connections_summary=meta.get("connections_summary", ""),
                        related_files=meta.get("related_files", None),
                    ),
                    style=NodeStyle(),
                )
            )
        return nodes

    def _parse_edges(self, raw: list[dict]) -> list[DiagramEdge]:
        edges = []
        for e in raw:
            meta = e.get("metadata", {})
            edges.append(
                DiagramEdge(
                    id=e.get("id", str(uuid.uuid4())),
                    source=e.get("source", ""),
                    target=e.get("target", ""),
                    label=e.get("label"),
                    description=e.get("description"),
                    metadata=EdgeMetadata(
                        tooltip_title=meta.get("tooltip_title", ""),
                        tooltip_description=meta.get("tooltip_description", ""),
                        relationship_type=meta.get("relationship_type", "generic"),
                        source_to_target_summary=meta.get("source_to_target_summary", ""),
                        importance=meta.get("importance", "medium"),
                        related_files=meta.get("related_files", None),
                    ),
                    style=EdgeStyle(),
                )
            )
        return edges

    def _merge_nodes(
        self, existing: list[DiagramNode], updated: list[DiagramNode]
    ) -> list[DiagramNode]:
        """Replace existing nodes that have matching IDs; append brand-new ones."""
        existing_map = {n.id: n for n in existing}
        for node in updated:
            existing_map[node.id] = node  # overwrite or add
        return list(existing_map.values())

    def _merge_edges(
        self, existing: list[DiagramEdge], new: list[DiagramEdge]
    ) -> list[DiagramEdge]:
        """Preserve existing edge metadata if source/target match; otherwise take new."""
        existing_map = {(e.source, e.target): e for e in existing}
        result_map = {(e.source, e.target): e for e in existing}
        
        for edge in new:
            pair = (edge.source, edge.target)
            if pair in existing_map:
                # If existing edge had metadata and new one doesn't (or we want to preserve), 
                # we merge them. For now, take the new one but we could be smarter.
                result_map[pair] = edge
            else:
                result_map[pair] = edge
                

    def _sanitize_mermaid(self, mermaid_code: str) -> str:
        """Fix common Mermaid syntax issues produced by the AI.

        1. Expands comma-separated class declarations.
        2. Quotes node labels that contain special characters (parentheses,
           brackets, braces, quotes) to prevent Mermaid parse errors.
        """
        if not mermaid_code:
            return mermaid_code

        lines = mermaid_code.splitlines()
        result: list[str] = []

        for line in lines:
            stripped = line.strip()

            # Fix comma-separated class declarations
            m = re.match(r'^(\s*)class\s+([A-Za-z_][\w,\s]+)$', stripped)
            if m:
                indent = m.group(1)
                names = [n.strip() for n in m.group(2).split(',') if n.strip()]
                if len(names) > 1:
                    for name in names:
                        result.append(f"{indent}class {name}")
                    continue
                result.append(line)
                continue

            # Skip edge definitions, directives, comments
            if (
                re.search(r'(--[>.\-~]|==[>]|~~~)', stripped)
                or stripped.startswith(("class ", "click ", "style ", "subgraph "))
                or stripped == "end"
                or stripped.startswith("%%")
            ):
                result.append(line)
                continue

            # Fix node labels with special characters by quoting them
            # Characters that break Mermaid: ()[]{}"'<>|
            special_chars_pattern = r'[()\[\]{}"\'<>|]'

            def _quote_label(match: re.Match) -> str:
                node_id = match.group(1)
                open_delim = match.group(2)
                label = match.group(3)
                close_delim = match.group(4)

                # Already quoted — just escape inner double-quotes
                if label.startswith('"') and label.endswith('"'):
                    inner = label[1:-1].replace('"', '\\"')
                    return f'{node_id}{open_delim}"{inner}"{close_delim}'

                # Only wrap if label actually contains problematic characters
                if re.search(special_chars_pattern, label):
                    safe_label = label.replace('"', '\\"')
                    return f'{node_id}{open_delim}"{safe_label}"{close_delim}'

                return match.group(0)

            # Order matters — multi-char delimiters first
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\[\[)([^\]]*?)(\]\])', _quote_label, line
            )  # [[...]]
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\[\()([^\)]*?)(\)\])', _quote_label, line
            )  # [(...)]
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\(\()([^\)]*?)(\)\))', _quote_label, line
            )  # ((...))
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\{\{)([^\}]*?)(\}\})', _quote_label, line
            )  # {{...}}
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\[)([^\]]*?)(\])(?!\[)', _quote_label, line
            )  # [...]
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\()([^\)]*?)(\))(?!\))', _quote_label, line
            )  # (...)
            line = re.sub(
                r'(\b[\w_][\w\d_]*)(\{)([^\}]*?)(\})(?!\{)', _quote_label, line
            )  # {...}

            result.append(line)

        return "\n".join(result)

    def _validate_mermaid_syntax(self, mermaid_code: str) -> bool:
        if not mermaid_code:
            return False
        valid_keywords = ["flowchart", "sequenceDiagram", "classDiagram", "stateDiagram", "erDiagram", "gantt"]
        has_keyword = any(k in mermaid_code for k in valid_keywords)
        has_connections = "-->" in mermaid_code or "->" in mermaid_code or ":::" in mermaid_code
        return has_keyword and has_connections

    def _fallback_diagram(self, diagram_type: str) -> DiagramResult:
        nodes = self._parse_nodes(_FALLBACK_NODES)
        return DiagramResult(
            diagram_id=str(uuid.uuid4()),
            conversation_id="",
            title="Design System Architecture",
            diagram_type=diagram_type or "flowchart",
            provider=self.name,
            diagram_source=_MOCK_MERMAID,
            diagram_format="mermaid",
            explanation="Fallback diagram — AI generation failed. Please try again.",
            nodes=nodes,
            edges=[],
            style=DiagramStyle(),
            change_intent="NEW_DIAGRAM",
            is_full_regeneration=True,
            metadata={"node_count": len(nodes), "edge_count": 6},
        )

    def _fallback_refinement(
        self, existing_diagram: str, diagram_type: str, parent_id: str | None, base_id: str | None
    ) -> DiagramResult:
        return DiagramResult(
            diagram_id=str(uuid.uuid4()),
            conversation_id="",
            title="Design System Architecture (Refined)",
            diagram_type=diagram_type or "flowchart",
            provider=self.name,
            diagram_source=existing_diagram,  # return unchanged diagram
            diagram_format="mermaid",
            explanation="Fallback — refinement failed. The original diagram is preserved.",
            changes_summary=["Refinement failed — original diagram preserved"],
            nodes=[],
            edges=[],
            style=DiagramStyle(),
            change_intent="PATCH_CHANGE",
            is_full_regeneration=False,
            base_diagram_id=base_id,
            parent_diagram_id=parent_id,
            metadata={"node_count": 0, "edge_count": 0},
        )


# ──────────────────────────────────────────────────────────────────────────────
# Fallback data
# ──────────────────────────────────────────────────────────────────────────────

_FALLBACK_NODES = [
    {"id": "PT", "label": "Primitive Tokens", "type": "token", "metadata": {"tooltip_title": "Primitive Tokens", "tooltip_description": "Raw design values (colors, spacing) with no semantic meaning.", "role": "Foundation", "importance": "high", "connections_summary": "Feeds into Semantic Tokens."}},
    {"id": "ST", "label": "Semantic Tokens", "type": "token", "metadata": {"tooltip_title": "Semantic Tokens", "tooltip_description": "Purpose-driven tokens like color.brand.primary.", "role": "Foundation", "importance": "high", "connections_summary": "Derived from Primitive Tokens; used by Component Tokens."}},
    {"id": "CT", "label": "Component Tokens", "type": "token", "metadata": {"tooltip_title": "Component Tokens", "tooltip_description": "Component-specific style references.", "role": "Foundation", "importance": "medium", "connections_summary": "Feeds into Atoms."}},
    {"id": "ATOMS", "label": "Atoms", "type": "component", "metadata": {"tooltip_title": "Atomic Components", "tooltip_description": "The smallest reusable UI building blocks (Button, Input, Icon).", "role": "Component", "importance": "high", "connections_summary": "Composed into Molecules."}},
    {"id": "MOL", "label": "Molecules", "type": "component", "metadata": {"tooltip_title": "Molecule Components", "tooltip_description": "Combinations of atoms forming functional UI patterns.", "role": "Component", "importance": "medium", "connections_summary": "Composed into Organisms."}},
    {"id": "ORG", "label": "Organisms", "type": "component", "metadata": {"tooltip_title": "Organism Components", "tooltip_description": "Complex UI sections assembled from molecules.", "role": "Component", "importance": "medium", "connections_summary": "Used in application pages."}},
    {"id": "NX", "label": "Next.js App", "type": "generic", "metadata": {"tooltip_title": "Application Layer", "tooltip_description": "The consuming application that uses the design system.", "role": "Application", "importance": "medium", "connections_summary": "Receives Organisms."}},
]

_MOCK_MERMAID = """flowchart TD
    subgraph Tokens["Design Tokens"]
        PT[Primitive Tokens]
        ST[Semantic Tokens]
        CT[Component Tokens]
    end
    subgraph Components["Component Library"]
        ATOMS[Atoms]
        MOL[Molecules]
        ORG[Organisms]
    end
    subgraph App["Application"]
        NX[Next.js App]
    end

    PT --> ST
    ST --> CT
    CT --> ATOMS
    ATOMS --> MOL
    MOL --> ORG
    ORG --> NX
"""
