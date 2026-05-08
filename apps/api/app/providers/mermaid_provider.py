import uuid

from app.providers.base import DiagramContext, DiagramProvider, DiagramResult


class MermaidProvider(DiagramProvider):
    name = "mermaid"

    async def generate_diagram(
        self,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        return DiagramResult(
            diagram_id=str(uuid.uuid4()),
            title="Design System Architecture",
            diagram_type=diagram_type or "design-system-architecture",
            provider=self.name,
            diagram_source=_MOCK_MERMAID,
            diagram_format="mermaid",
            explanation="Mock diagram for development. This will be replaced with AI-generated Mermaid in Phase 5.",
            metadata={"node_count": 8, "edge_count": 7},
        )

    async def refine_diagram(
        self,
        existing_diagram: str,
        enhanced_followup: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        return DiagramResult(
            diagram_id=str(uuid.uuid4()),
            title="Design System Architecture (Refined)",
            diagram_type=diagram_type or "design-system-architecture",
            provider=self.name,
            diagram_source=_MOCK_MERMAID_REFINED,
            diagram_format="mermaid",
            explanation="Mock refined diagram. Real AI refinement coming in Phase 6.",
            changes_summary=["Added mock refinement layer"],
            metadata={"node_count": 10, "edge_count": 9},
        )

    async def export_diagram(
        self,
        diagram_source: str,
        diagram_format: str,
        export_format: str,
    ) -> str:
        if export_format == "mermaid":
            return diagram_source
        elif export_format == "json":
            import json

            return json.dumps(
                {"source": diagram_source, "format": diagram_format},
                indent=2,
            )
        else:
            return diagram_source


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

_MOCK_MERMAID_REFINED = """flowchart TD
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
    subgraph Docs["Documentation"]
        SB[Storybook]
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
    ORG --> SB
"""
