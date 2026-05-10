import asyncio
import logging
import re
from app.core.config import settings
from app.core.errors import AiTimeoutError
from app.providers.base import DiagramContext
from app.providers.registry import ProviderRegistry
from app.schemas.diagram import DiagramMetadata, DiagramNode, DiagramEdge, DiagramResult, DiagramStyle
from app.services.conversation_service import ConversationService
from app.services.version_service import VersionService

logger = logging.getLogger(__name__)


def _parse_mermaid_nodes_edges(diagram_source: str) -> tuple[list[DiagramNode], list[DiagramEdge]]:
    """Simple parser to extract nodes and edges from Mermaid diagram source."""
    nodes: list[DiagramNode] = []
    edges: list[DiagramEdge] = []
    node_ids: set[str] = set()

    try:
        lines = diagram_source.strip().split('\n')
        # Node with label: ID[Label], ID(Label), ID((Label)), ID{Label}, ID{{Label}}, ID[[Label]], ID[(Label)]
        node_with_label_pattern = re.compile(r'(\b[\w\-]+)\s*([\[\(\{\d]+)\s*["\']?([^"\'\]\)\}]*)["\']?\s*([\]\)\}\d]+)')
        # Simple node: ID (only if on its own line)
        simple_node_pattern = re.compile(r'^(\s*)(\b[\w\-]+)(\s*)$')
        # Edge pattern that accounts for optional labels on source
        edge_pattern = re.compile(r'(\b[\w\-]+)(?:\s*[\[\(\{\d].*?[\]\)\}\d])?\s*(?:--\>|-\>|-\.\-\>|==\>)\s*(\b[\w\-]+)')

        for line in lines:
            line = line.strip()
            # Skip graph declaration and comments
            if line.startswith(('graph', 'flowchart', '%%', 'sequenceDiagram', 'classDiagram', 'subgraph')):
                continue
            if not line or line == 'end':
                continue

            # Parse edges
            edge_match = edge_pattern.search(line)
            if edge_match:
                source = edge_match.group(1)
                target = edge_match.group(2)
                edges.append(DiagramEdge(
                    id=f"{source}_{target}",
                    source=source,
                    target=target,
                    label=None
                ))
                node_ids.add(source)
                node_ids.add(target)

            # Parse nodes with labels (find all since a line can have multiple nodes like in an edge)
            for node_label_match in node_with_label_pattern.finditer(line):
                node_id = node_label_match.group(1)
                node_label = node_label_match.group(3) or node_id
                if node_id not in [n.id for n in nodes]:
                    nodes.append(DiagramNode(
                        id=node_id,
                        label=node_label,
                        type="generic"
                    ))
                    node_ids.discard(node_id)
            
            # If no edge and no labeled node, try simple node
            if not edge_match and not any(node_with_label_pattern.search(line) for _ in [1]):
                simple_match = simple_node_pattern.search(line)
                if simple_match:
                    node_id = simple_match.group(2)
                    if node_id not in [n.id for n in nodes]:
                        nodes.append(DiagramNode(
                            id=node_id,
                            label=node_id,
                            type="generic"
                        ))
                        node_ids.discard(node_id)

        # Add nodes that were only mentioned in edges
        for node_id in node_ids:
            if node_id not in [n.id for n in nodes]:
                nodes.append(DiagramNode(
                    id=node_id,
                    label=node_id,
                    type="generic"
                ))

        logger.info(f"Parsed {len(nodes)} nodes and {len(edges)} edges from diagram source")
    except Exception as e:
        logger.error(f"Failed to parse Mermaid diagram: {e}")

    return nodes, edges


class RefinementService:
    def __init__(
        self,
        conversation_service: ConversationService | None = None,
        version_service: VersionService | None = None,
    ):
        self.conversation_service = conversation_service or ConversationService()
        self.version_service = version_service or VersionService()

    async def refine(
        self,
        conversation_id: str,
        diagram_id: str,
        followup_prompt: str,
        current_diagram_source: str,
        provider: str,
        existing_nodes: list[DiagramNode] | None = None,
        existing_edges: list[DiagramEdge] | None = None,
        existing_style: DiagramStyle | None = None,
    ) -> DiagramResult:
        provider_instance = ProviderRegistry.get(provider)

        # If nodes/edges are not provided, try version history then diagram source
        if not existing_nodes or not existing_edges:
            if current_version := self.version_service.get_version_by_id(conversation_id, diagram_id):
                meta = current_version.metadata
                if not existing_nodes and "nodes" in meta:
                    existing_nodes = [DiagramNode(**n) for n in meta["nodes"]]
                if not existing_edges and "edges" in meta:
                    existing_edges = [DiagramEdge(**e) for e in meta["edges"]]

            if not existing_nodes or not existing_edges:
                logger.warning(f"Missing nodes/edges in refine request, attempting to parse from diagram source")
                try:
                    parsed_nodes, parsed_edges = _parse_mermaid_nodes_edges(current_diagram_source)
                    if not existing_nodes and parsed_nodes:
                        existing_nodes = parsed_nodes
                    if not existing_edges and parsed_edges:
                        existing_edges = parsed_edges
                except Exception as e:
                    logger.error(f"Failed to parse diagram source: {e}")
                    existing_nodes = existing_nodes or []
                    existing_edges = existing_edges or []

        # ── Step 1: Classify intent ─────────────────────────────────────────
        # Retrieve the current diagram title from version history for cleaner classification
        current_version = self.version_service.get_latest_version(conversation_id)
        diagram_title = current_version.title if current_version else "Design System Diagram"

        try:
            intent = await asyncio.wait_for(
                provider_instance.classify_intent(
                    diagram_title=diagram_title,
                    followup_prompt=followup_prompt,
                ),
                timeout=settings.refine_timeout_seconds,
            )

            # ── Step 2: Handle STYLE_CHANGE without AI topology mutation ────────
            if intent == "STYLE_CHANGE":
                return self._style_only_response(
                    conversation_id=conversation_id,
                    diagram_id=diagram_id,
                    followup_prompt=followup_prompt,
                    current_diagram_source=current_diagram_source,
                    existing_nodes=existing_nodes or [],
                    existing_edges=existing_edges or [],
                    existing_style=existing_style or DiagramStyle(),
                )

            # ── Step 2.5: Handle EXPLAIN_ONLY without AI topology mutation ────────
            if intent == "EXPLAIN_ONLY":
                return self._explain_only_response(
                    conversation_id=conversation_id,
                    diagram_id=diagram_id,
                    followup_prompt=followup_prompt,
                    current_diagram_source=current_diagram_source,
                    existing_nodes=existing_nodes or [],
                    existing_edges=existing_edges or [],
                    existing_style=existing_style or DiagramStyle(),
                    current_version=current_version,
                )

            # ── Step 3: Determine versioning chain ──────────────────────────────
            previous_version = self.version_service.get_latest_version(conversation_id)
            new_version_number = (previous_version.version + 1) if previous_version else 2

            # Retrieve base_diagram_id — stays the same for the entire conversation
            base_diagram_id = (
                getattr(previous_version, "base_diagram_id", diagram_id) if previous_version else diagram_id
            )

            # ── Step 4: Incremental AI refinement ───────────────────────────────
            context = DiagramContext(conversation_id=conversation_id)
            diagram_result = await asyncio.wait_for(
                provider_instance.refine_diagram(
                    existing_diagram=current_diagram_source,
                    enhanced_followup=followup_prompt,
                    diagram_type=current_version.diagram_type if current_version else "design-system-architecture",
                    context=context,
                    existing_nodes=existing_nodes or [],
                    existing_edges=existing_edges or [],
                    intent=intent,
                    parent_diagram_id=diagram_id,
                    base_diagram_id=base_diagram_id,
                ),
                timeout=settings.refine_timeout_seconds,
            )
        except asyncio.TimeoutError:
            logger.error(f"Refinement timed out after {settings.refine_timeout_seconds}s")
            raise AiTimeoutError(
                f"Refinement timed out after {settings.refine_timeout_seconds}s. "
                "Please try a shorter follow-up."
            )

        # ── Step 5: Preserve existing style unless AI changed it ────────────
        final_style = existing_style or DiagramStyle()

        self.conversation_service.add_message(
            conversation_id,
            role="user",
            content=followup_prompt,
            message_type="refinement",
        )
        self.conversation_service.add_message(
            conversation_id,
            role="assistant",
            content=diagram_result.explanation,
            message_type="diagram",
        )

        new_diagram_id = diagram_result.diagram_id
        version = self.version_service.create_version(
            diagram_id=new_diagram_id,
            conversation_id=conversation_id,
            version=new_version_number,
            title=diagram_result.title,
            diagram_type=current_version.diagram_type if current_version else "design-system-architecture",
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            changes_summary=diagram_result.changes_summary,
            metadata={
                "node_count": len(diagram_result.nodes),
                "edge_count": len(diagram_result.edges),
                "nodes": [n.model_dump() for n in diagram_result.nodes],
                "edges": [e.model_dump() for e in diagram_result.edges],
            },
        )

        self.conversation_service.set_current_diagram(conversation_id, new_diagram_id)

        return DiagramResult(
            diagram_id=new_diagram_id,
            conversation_id=conversation_id,
            version=version.version,
            title=diagram_result.title,
            diagram_type=version.diagram_type,
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            nodes=diagram_result.nodes,
            edges=diagram_result.edges,
            style=final_style,
            change_intent=intent,
            is_full_regeneration=diagram_result.is_full_regeneration,
            base_diagram_id=base_diagram_id,
            parent_diagram_id=diagram_id,
            changes_summary=diagram_result.changes_summary,
            metadata=DiagramMetadata(
                node_count=len(diagram_result.nodes),
                edge_count=len(diagram_result.edges),
            ),
        )

    def _style_only_response(
        self,
        conversation_id: str,
        diagram_id: str,
        followup_prompt: str,
        current_diagram_source: str,
        existing_nodes: list[DiagramNode],
        existing_edges: list[DiagramEdge],
        existing_style: DiagramStyle,
    ) -> DiagramResult:
        """Return the exact same diagram topology with a note that only style changed."""
        current_version = self.version_service.get_latest_version(conversation_id)

        # Final safety check
        if not existing_nodes or not existing_edges:
            parsed_nodes, parsed_edges = _parse_mermaid_nodes_edges(current_diagram_source)
            existing_nodes = existing_nodes or parsed_nodes
            existing_edges = existing_edges or parsed_edges

        self.conversation_service.add_message(
            conversation_id,
            role="user",
            content=followup_prompt,
            message_type="refinement",
        )
        self.conversation_service.add_message(
            conversation_id,
            role="assistant",
            content="Style preference noted — please use the Style Toolbar to apply visual changes instantly.",
            message_type="diagram",
        )

        return DiagramResult(
            diagram_id=diagram_id,
            conversation_id=conversation_id,
            version=current_version.version if current_version else 1,
            title=current_version.title if current_version else "Design System Architecture",
            diagram_type=current_version.diagram_type if current_version else "design-system-architecture",
            provider="mermaid",
            diagram_source=current_diagram_source,
            diagram_format="mermaid",
            explanation="Style preference noted — use the Style Toolbar to apply visual changes instantly without re-generating the diagram.",
            nodes=existing_nodes,
            edges=existing_edges,
            style=existing_style,
            change_intent="STYLE_CHANGE",
            is_full_regeneration=False,
            changes_summary=["Style change requested — use the toolbar for instant visual updates"],
            metadata=DiagramMetadata(node_count=len(existing_nodes)),
        )

    def _explain_only_response(
        self,
        conversation_id: str,
        diagram_id: str,
        followup_prompt: str,
        current_diagram_source: str,
        existing_nodes: list[DiagramNode],
        existing_edges: list[DiagramEdge],
        existing_style: DiagramStyle,
        current_version: any,
    ) -> DiagramResult:
        """Return the existing diagram with an explanation (no structural changes)."""
        # Final safety check
        if not existing_nodes or not existing_edges:
            parsed_nodes, parsed_edges = _parse_mermaid_nodes_edges(current_diagram_source)
            existing_nodes = existing_nodes or parsed_nodes
            existing_edges = existing_edges or parsed_edges
        # Generate a simple explanation based on the diagram
        node_count = len(existing_nodes)
        edge_count = len(existing_edges)
        explanation = f"This diagram shows {node_count} node(s) and {edge_count} connection(s). "

        if current_version and current_version.explanation:
            explanation += current_version.explanation

        self.conversation_service.add_message(
            conversation_id,
            role="user",
            content=followup_prompt,
            message_type="refinement",
        )
        self.conversation_service.add_message(
            conversation_id,
            role="assistant",
            content=explanation,
            message_type="diagram",
        )

        return DiagramResult(
            diagram_id=diagram_id,
            conversation_id=conversation_id,
            version=current_version.version if current_version else 1,
            title=current_version.title if current_version else "Design System Architecture",
            diagram_type=current_version.diagram_type if current_version else "design-system-architecture",
            provider="mermaid",
            diagram_source=current_diagram_source,
            diagram_format="mermaid",
            explanation=explanation,
            nodes=existing_nodes,
            edges=existing_edges,
            style=existing_style,
            change_intent="EXPLAIN_ONLY",
            is_full_regeneration=False,
            changes_summary=["Explanation provided — no structural changes made"],
            metadata=DiagramMetadata(node_count=node_count, edge_count=edge_count),
        )
