from abc import ABC, abstractmethod


class DiagramContext:
    """Context object passed to providers during generation."""

    def __init__(
        self,
        conversation_id: str | None = None,
        diagram_type: str = "auto",
    ):
        self.conversation_id = conversation_id
        self.diagram_type = diagram_type


class DiagramResult:
    """Normalized result returned by all providers."""

    def __init__(
        self,
        diagram_id: str,
        title: str,
        diagram_type: str,
        provider: str,
        diagram_source: str,
        diagram_format: str,
        explanation: str,
        changes_summary: list[str] | None = None,
        metadata: dict | None = None,
    ):
        self.diagram_id = diagram_id
        self.title = title
        self.diagram_type = diagram_type
        self.provider = provider
        self.diagram_source = diagram_source
        self.diagram_format = diagram_format
        self.explanation = explanation
        self.changes_summary = changes_summary or []
        self.metadata = metadata or {}


class DiagramProvider(ABC):
    """Abstract base class for diagram providers."""

    name: str = ""

    @abstractmethod
    async def generate_diagram(
        self,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        """Generate a new diagram from an enhanced prompt."""
        ...

    @abstractmethod
    async def refine_diagram(
        self,
        existing_diagram: str,
        enhanced_followup: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        """Refine an existing diagram based on follow-up instructions."""
        ...

    @abstractmethod
    async def export_diagram(
        self,
        diagram_source: str,
        diagram_format: str,
        export_format: str,
    ) -> str:
        """Export diagram in the requested format. Returns formatted content."""
        ...
