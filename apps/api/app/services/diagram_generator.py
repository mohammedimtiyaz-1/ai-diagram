import uuid

from app.providers.base import DiagramContext
from app.providers.registry import ProviderRegistry
from app.schemas.diagram import DiagramMetadata, DiagramNode, DiagramResult, DiagramStyle
from app.services.conversation_service import ConversationService
from app.services.version_service import VersionService


class DiagramGeneratorService:
    def __init__(
        self,
        conversation_service: ConversationService | None = None,
        version_service: VersionService | None = None,
    ):
        self.conversation_service = conversation_service or ConversationService()
        self.version_service = version_service or VersionService()

    async def generate(
        self,
        raw_prompt: str,
        enhanced_prompt: str,
        diagram_type: str,
        provider: str,
        conversation_id: str | None,
    ) -> DiagramResult:
        provider_instance = ProviderRegistry.get(provider)
        context = DiagramContext(
            conversation_id=conversation_id,
            diagram_type=diagram_type,
        )

        diagram_result = await provider_instance.generate_diagram(
            enhanced_prompt, diagram_type, context
        )

        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            self.conversation_service.create(conversation_id)

        diagram_id = diagram_result.diagram_id
        self.conversation_service.add_message(
            conversation_id,
            role="user",
            content=raw_prompt,
            message_type="input",
        )
        self.conversation_service.add_message(
            conversation_id,
            role="assistant",
            content=diagram_result.explanation,
            message_type="diagram",
        )
        self.conversation_service.set_current_diagram(conversation_id, diagram_id)

        version = self.version_service.create_version(
            diagram_id=diagram_id,
            conversation_id=conversation_id,
            version=1,
            title=diagram_result.title,
            diagram_type=diagram_type,
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            changes_summary=[],
            metadata={
                "node_count": len(diagram_result.nodes),
                "edge_count": len(diagram_result.edges),
            },
        )

    async def generate_from_codebase(
        self,
        analysis_summary: str,
        enhanced_prompt: str,
        diagram_type: str,
        provider: str,
        conversation_id: str | None,
        repo_url: str,
    ) -> DiagramResult:
        provider_instance = ProviderRegistry.get(provider)
        context = DiagramContext(
            conversation_id=conversation_id,
            diagram_type=diagram_type,
        )

        diagram_result = await provider_instance.generate_codebase_diagram(
            analysis_summary, enhanced_prompt, diagram_type, context
        )

        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            self.conversation_service.create(conversation_id)

        diagram_id = diagram_result.diagram_id
        
        # Store metadata about the repository
        self.conversation_service.add_message(
            conversation_id,
            role="user",
            content=f"Generate diagram from codebase: {repo_url}",
            message_type="input",
        )
        self.conversation_service.add_message(
            conversation_id,
            role="assistant",
            content=f"Analyzed {repo_url}. {diagram_result.explanation}",
            message_type="diagram",
        )
        self.conversation_service.set_current_diagram(conversation_id, diagram_id)

        version = self.version_service.create_version(
            diagram_id=diagram_id,
            conversation_id=conversation_id,
            version=1,
            title=diagram_result.title,
            diagram_type=diagram_type,
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            changes_summary=[],
            metadata={
                "node_count": len(diagram_result.nodes),
                "edge_count": len(diagram_result.edges),
                "repo_url": repo_url
            },
        )

        return DiagramResult(
            diagram_id=diagram_id,
            conversation_id=conversation_id,
            version=version.version,
            title=diagram_result.title,
            diagram_type=diagram_type,
            provider=provider,
            diagram_source=diagram_result.diagram_source,
            diagram_format=diagram_result.diagram_format,
            explanation=diagram_result.explanation,
            nodes=diagram_result.nodes,
            edges=diagram_result.edges,
            style=DiagramStyle(),
            change_intent="NEW_DIAGRAM",
            is_full_regeneration=True,
            base_diagram_id=diagram_id,
            parent_diagram_id=None,
            changes_summary=[],
            metadata=DiagramMetadata(
                node_count=len(diagram_result.nodes),
                edge_count=len(diagram_result.edges),
            ),
        )
