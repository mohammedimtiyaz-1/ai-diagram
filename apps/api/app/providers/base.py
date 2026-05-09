from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.diagram import DiagramNode, DiagramEdge, DiagramStyle


class DiagramContext:
    """Context object passed to providers during generation."""

    def __init__(
        self,
        conversation_id: str | None = None,
        diagram_type: str = "auto",
        entities: list[str] | None = None,
        relationships: list | None = None,
    ):
        self.conversation_id = conversation_id
        self.diagram_type = diagram_type
        self.entities = entities or []
        self.relationships = relationships or []


class DiagramResult:
    """Normalized result returned by all providers."""

    def __init__(
        self,
        diagram_id: str,
        conversation_id: str,
        title: str,
        diagram_type: str,
        provider: str,
        diagram_source: str,
        diagram_format: str,
        explanation: str,
        changes_summary: list[str] | None = None,
        metadata: dict | None = None,
        nodes: list["DiagramNode"] | None = None,
        edges: list["DiagramEdge"] | None = None,
        style: "DiagramStyle" | None = None,
        change_intent: str = "NEW_DIAGRAM",
        is_full_regeneration: bool = True,
        base_diagram_id: str | None = None,
        parent_diagram_id: str | None = None,
    ):
        self.diagram_id = diagram_id
        self.conversation_id = conversation_id
        self.title = title
        self.diagram_type = diagram_type
        self.provider = provider
        self.diagram_source = diagram_source
        self.diagram_format = diagram_format
        self.explanation = explanation
        self.changes_summary = changes_summary or []
        self.metadata = metadata or {}
        self.nodes = nodes or []
        self.edges = edges or []
        self.style = style
        self.change_intent = change_intent
        self.is_full_regeneration = is_full_regeneration
        self.base_diagram_id = base_diagram_id
        self.parent_diagram_id = parent_diagram_id


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
    async def generate_codebase_diagram(
        self,
        analysis_summary: str,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        """Generate a diagram from codebase analysis."""
        ...

    @abstractmethod
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
