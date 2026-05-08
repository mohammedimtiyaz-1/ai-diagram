from app.schemas.prompt import EnhanceRequest, EnhancementResult, Relationship
from app.schemas.diagram import GenerateRequest, DiagramResult
from app.schemas.common import ErrorResponse


def test_enhance_request_validation():
    valid = EnhanceRequest(raw_prompt="A valid prompt with enough length for testing")
    assert valid.diagram_type == "auto"
    assert valid.source == "text"


def test_enhancement_result_creation():
    result = EnhancementResult(
        enhanced_prompt="Enhanced description",
        diagram_goal="Show architecture",
        detected_diagram_type="design-system-architecture",
        entities=["Tokens", "Components"],
        relationships=[
            Relationship(from_entity="Tokens", to_entity="Components", type="feeds-into"),
        ],
        structure_hints="Top-down layered",
        assumptions=["Atomic design"],
        recommended_provider="mermaid",
    )
    assert result.recommended_provider == "mermaid"
    assert len(result.entities) == 2


def test_generate_request_validation():
    req = GenerateRequest(
        raw_prompt="A valid prompt with enough length for testing",
        enhanced_prompt="Enhanced",
        diagram_type="design-system-architecture",
        provider="mermaid",
    )
    assert req.provider == "mermaid"
    assert req.conversation_id is None


def test_error_response():
    error = ErrorResponse(
        code="GENERATION_FAILED",
        message="Failed to generate",
        suggestion="Try again",
        retry_allowed=True,
    )
    assert error.code == "GENERATION_FAILED"
    assert error.retry_allowed is True
