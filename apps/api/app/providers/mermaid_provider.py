import json
import logging
import uuid

from app.core.openai_client import OpenAIClient
from app.prompts.mermaid_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.providers.base import DiagramContext, DiagramProvider, DiagramResult

logger = logging.getLogger(__name__)


class MermaidProvider(DiagramProvider):
    name = "mermaid"

    def __init__(self, max_retries: int = 1):
        self.max_retries = max_retries

    async def generate_diagram(
        self,
        enhanced_prompt: str,
        diagram_type: str,
        context: DiagramContext,
    ) -> DiagramResult:
        """Generate Mermaid diagram using OpenAI GPT-4o."""
        client = OpenAIClient.get_async()

        # Format entities and relationships for the prompt
        entities_str = ", ".join(context.entities) if context.entities else "none"
        relationships_str = ", ".join(
            f"{r.from_entity} → {r.to_entity} ({r.type})"
            for r in (context.relationships or [])
        ) or "none"

        user_prompt = USER_PROMPT_TEMPLATE.format(
            enhanced_prompt=enhanced_prompt,
            diagram_type=diagram_type,
            entities=entities_str,
            relationships=relationships_str,
        )

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7,
                    max_tokens=2000,
                )

                content = response.choices[0].message.content
                if not content:
                    raise ValueError("OpenAI returned empty content")

                data = json.loads(content)

                # Validate Mermaid syntax
                mermaid_code = data.get("mermaid_code", "")
                if not self._validate_mermaid_syntax(mermaid_code):
                    logger.warning("Generated Mermaid failed syntax validation, using fallback")

                return DiagramResult(
                    diagram_id=str(uuid.uuid4()),
                    title=data.get("title", "Design System Architecture"),
                    diagram_type=diagram_type or "flowchart",
                    provider=self.name,
                    diagram_source=mermaid_code,
                    diagram_format="mermaid",
                    explanation=data.get("explanation", ""),
                    metadata={"node_count": self._count_nodes(mermaid_code), "edge_count": self._count_edges(mermaid_code)},
                )

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries:
                    continue

        # All retries failed, fall back to mock
        logger.error(f"OpenAI generation failed after {self.max_retries + 1} attempts: {last_error}")
        return self._fallback_diagram(diagram_type)

    def _validate_mermaid_syntax(self, mermaid_code: str) -> bool:
        """Basic Mermaid syntax validation."""
        if not mermaid_code:
            return False

        # Check for basic Mermaid diagram keywords
        valid_keywords = ["flowchart", "sequenceDiagram", "classDiagram", "stateDiagram", "erDiagram", "gantt"]
        has_keyword = any(keyword in mermaid_code for keyword in valid_keywords)

        # Check for basic structure (has some content with arrows or connections)
        has_connections = "-->" in mermaid_code or "->" in mermaid_code or ":::" in mermaid_code

        return has_keyword and has_connections

    def _count_nodes(self, mermaid_code: str) -> int:
        """Estimate node count from Mermaid code."""
        # Count occurrences of [...] which typically represent nodes
        import re
        nodes = re.findall(r'\[([^\]]+)\]', mermaid_code)
        return len(nodes)

    def _count_edges(self, mermaid_code: str) -> int:
        """Estimate edge count from Mermaid code."""
        # Count occurrences of arrows
        arrows = mermaid_code.count("-->") + mermaid_code.count("--") + mermaid_code.count("->")
        return arrows

    def _fallback_diagram(self, diagram_type: str) -> DiagramResult:
        """Fallback to mock diagram if AI fails."""
        return DiagramResult(
            diagram_id=str(uuid.uuid4()),
            title="Design System Architecture",
            diagram_type=diagram_type or "flowchart",
            provider=self.name,
            diagram_source=_MOCK_MERMAID,
            diagram_format="mermaid",
            explanation="Fallback diagram due to AI generation failure.",
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
