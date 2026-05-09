import asyncio
import logging
from app.core.config import settings
from app.core.errors import AiTimeoutError
from app.providers.base import DiagramContext
from app.providers.registry import ProviderRegistry
from app.schemas.diagram import DiagramMetadata, DiagramNode, DiagramResult, DiagramStyle
from app.services.conversation_service import ConversationService
from app.services.version_service import VersionService

logger = logging.getLogger(__name__)


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
        existing_edges: list[any] | None = None,
        existing_style: DiagramStyle | None = None,
    ) -> DiagramResult:
        provider_instance = ProviderRegistry.get(provider)

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
                timeout=settings.ai_timeout_seconds
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
                    # existing_edges is passed via context if needed, but provider.refine_diagram signature may need update
                    intent=intent,
                    parent_diagram_id=diagram_id,
                    base_diagram_id=base_diagram_id,
                ),
                timeout=settings.ai_timeout_seconds
            )
        except asyncio.TimeoutError:
            logger.error(f"Refinement timed out after {settings.ai_timeout_seconds}s")
            raise AiTimeoutError(f"Refinement timed out after {settings.ai_timeout_seconds}s. This is taking longer than expected. Please try again with a shorter prompt.")

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
        existing_edges: list[any],
        existing_style: DiagramStyle,
    ) -> DiagramResult:
        """Return the exact same diagram topology with a note that only style changed."""
        current_version = self.version_service.get_latest_version(conversation_id)

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
