from app.providers.base import DiagramContext
from app.providers.registry import ProviderRegistry
from app.schemas.diagram import DiagramMetadata, DiagramResult
from app.services.conversation_service import ConversationService
from app.services.version_service import VersionService


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
    ) -> DiagramResult:
        provider_instance = ProviderRegistry.get(provider)
        context = DiagramContext(
            conversation_id=conversation_id,
        )

        diagram_result = await provider_instance.refine_diagram(
            existing_diagram=current_diagram_source,
            enhanced_followup=followup_prompt,
            diagram_type="design-system-architecture",
            context=context,
        )

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
        previous_version = self.version_service.get_latest_version(conversation_id)
        new_version_number = (previous_version.version + 1) if previous_version else 1

        version = self.version_service.create_version(
            diagram_id=new_diagram_id,
            conversation_id=conversation_id,
            version=new_version_number,
            title=diagram_result.title,
            diagram_type="design-system-architecture",
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            changes_summary=diagram_result.changes_summary,
            metadata={"node_count": 10, "edge_count": 9},
        )

        self.conversation_service.set_current_diagram(conversation_id, new_diagram_id)

        return DiagramResult(
            diagram_id=new_diagram_id,
            conversation_id=conversation_id,
            version=version.version,
            title=diagram_result.title,
            diagram_type="design-system-architecture",
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            changes_summary=diagram_result.changes_summary,
            metadata=DiagramMetadata(**version.metadata),
        )
