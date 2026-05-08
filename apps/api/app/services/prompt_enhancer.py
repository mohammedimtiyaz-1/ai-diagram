import json
import logging

from app.core.openai_client import OpenAIClient
from app.prompts.enhancement_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.prompt import EnhancementResult, Relationship

logger = logging.getLogger(__name__)


class PromptEnhancerService:
    """AI-powered prompt enhancement service using OpenAI GPT-4o."""

    def __init__(self, max_retries: int = 1):
        self.max_retries = max_retries

    async def enhance(self, raw_prompt: str, diagram_type: str) -> EnhancementResult:
        """Enhance a raw prompt using OpenAI GPT-4o.

        Args:
            raw_prompt: The user's raw prompt text
            diagram_type: Preferred diagram type (e.g., "auto", "flowchart", "sequence")

        Returns:
            EnhancementResult with structured enhancement data

        Raises:
            Exception: If OpenAI call fails after retries
        """
        client = OpenAIClient.get_async()

        user_prompt = USER_PROMPT_TEMPLATE.format(
            raw_prompt=raw_prompt,
            diagram_type=diagram_type,
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
                    max_tokens=1000,
                )

                content = response.choices[0].message.content
                if not content:
                    raise ValueError("OpenAI returned empty content")

                data = json.loads(content)

                # Validate and map to EnhancementResult
                return EnhancementResult(
                    enhanced_prompt=data.get("enhanced_prompt", raw_prompt),
                    diagram_goal=f"Visualize the design system architecture described: {raw_prompt[:60]}...",
                    detected_diagram_type=data.get("diagram_type", diagram_type or "auto"),
                    entities=[e["name"] for e in data.get("entities", [])],
                    relationships=[
                        Relationship(
                            from_entity=r["from"],
                            to_entity=r["to"],
                            type=r["type"],
                        )
                        for r in data.get("relationships", [])
                    ],
                    structure_hints="AI-generated structure based on entities and relationships",
                    assumptions=data.get("assumptions", []),
                    recommended_provider="mermaid",
                )

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries:
                    continue

        # All retries failed, fall back to mock for resilience
        logger.error(f"OpenAI enhancement failed after {self.max_retries + 1} attempts: {last_error}")
        return self._fallback_enhancement(raw_prompt, diagram_type)

    def _fallback_enhancement(self, raw_prompt: str, diagram_type: str) -> EnhancementResult:
        """Fallback to a simple enhancement if AI fails."""
        detected_type = diagram_type if diagram_type != "auto" else "design-system-architecture"
        return EnhancementResult(
            enhanced_prompt=f"Create a {detected_type} diagram showing the design system architecture: {raw_prompt}",
            diagram_goal=f"Visualize: {raw_prompt[:60]}...",
            detected_diagram_type=detected_type,
            entities=["Design System", "Components", "Tokens"],
            relationships=[
                Relationship(from_entity="Tokens", to_entity="Components", type="styles"),
            ],
            structure_hints="Simple architecture",
            assumptions=["Using standard design system patterns"],
            recommended_provider="mermaid",
        )
