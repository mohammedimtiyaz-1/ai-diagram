"""Example inputs for prompt enhancement validation.

These are example prompts to validate the enhancement service works correctly.
To run with real OpenAI, set OPENAI_API_KEY environment variable.

Example prompts:
1. "design system with tokens and components"
2. "flow from Figma to code"
3. "component library with Storybook"
4. "design tokens primitive semantic component"
5. "design system architecture for e-commerce"
"""

import asyncio
import os

from app.core.openai_client import OpenAIClient
from app.services.prompt_enhancer import PromptEnhancerService

EXAMPLE_PROMPTS = [
    ("design system with tokens and components", "auto"),
    ("flow from Figma to code", "flowchart"),
    ("component library with Storybook", "auto"),
    ("design tokens primitive semantic component", "auto"),
    ("design system architecture for e-commerce", "auto"),
]


async def validate_examples():
    """Validate enhancement service with example prompts."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping validation: OPENAI_API_KEY not set")
        print("To run validation, set OPENAI_API_KEY environment variable")
        return

    service = PromptEnhancerService(max_retries=1)

    for i, (prompt, diagram_type) in enumerate(EXAMPLE_PROMPTS, 1):
        print(f"\n--- Example {i} ---")
        print(f"Raw prompt: {prompt}")
        print(f"Diagram type: {diagram_type}")

        try:
            result = await service.enhance(prompt, diagram_type)
            print(f"Enhanced prompt: {result.enhanced_prompt}")
            print(f"Detected type: {result.detected_diagram_type}")
            print(f"Entities: {result.entities}")
            print(f"Relationships: {len(result.relationships)}")
            print(f"Assumptions: {result.assumptions}")
            print("✓ Success")
        except Exception as e:
            print(f"✗ Failed: {e}")


if __name__ == "__main__":
    asyncio.run(validate_examples())
