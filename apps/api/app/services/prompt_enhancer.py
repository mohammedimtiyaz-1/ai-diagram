import uuid

from app.schemas.prompt import EnhancementResult, Relationship


class PromptEnhancerService:
    """Mock prompt enhancement service.

    Real AI integration will be implemented in Phase 4.
    """

    async def enhance(self, raw_prompt: str, diagram_type: str) -> EnhancementResult:
        detected_type = diagram_type if diagram_type != "auto" else "design-system-architecture"
        return EnhancementResult(
            enhanced_prompt=f"Create a detailed {detected_type} diagram showing: design tokens (primitive, semantic, component), a React component library (atoms, molecules, organisms), Tailwind theme integration, Storybook documentation, and a Next.js application consuming the component library. Show all dependencies flowing top-to-bottom.",
            diagram_goal=f"Visualize the design system architecture described: {raw_prompt[:60]}...",
            detected_diagram_type=detected_type,
            entities=[
                "Primitive Tokens",
                "Semantic Tokens",
                "Component Tokens",
                "React Component Library",
                "Tailwind Theme",
                "Storybook",
                "Next.js App",
            ],
            relationships=[
                Relationship(from_entity="Primitive Tokens", to_entity="Semantic Tokens", type="feeds-into"),
                Relationship(from_entity="Semantic Tokens", to_entity="Component Tokens", type="feeds-into"),
                Relationship(from_entity="Component Tokens", to_entity="React Component Library", type="styles"),
                Relationship(from_entity="React Component Library", to_entity="Storybook", type="documented-by"),
                Relationship(from_entity="React Component Library", to_entity="Next.js App", type="consumed-by"),
            ],
            structure_hints="top-down layered architecture with 4-5 layers",
            assumptions=[
                "Using Tailwind CSS for styling",
                "Storybook for component documentation",
                "Atomic design pattern for component hierarchy",
            ],
            recommended_provider="mermaid",
        )
