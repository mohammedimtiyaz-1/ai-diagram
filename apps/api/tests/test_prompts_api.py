from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_enhance_prompt():
    response = client.post(
        "/api/prompts/enhance",
        json={
            "raw_prompt": "I need a design system diagram showing tokens, components, and storybook",
            "diagram_type": "design-system-architecture",
            "source": "text",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "enhanced_prompt" in data
    assert "diagram_goal" in data
    assert "detected_diagram_type" in data
    assert "entities" in data
    assert "relationships" in data
    assert "assumptions" in data
    # AI returns the diagram_type from the prompt, which may be "auto" or the specified type
    assert data["detected_diagram_type"] in ["auto", "design-system-architecture"]


def test_enhance_prompt_auto_type():
    response = client.post(
        "/api/prompts/enhance",
        json={
            "raw_prompt": "Design system with tokens and components",
            "diagram_type": "auto",
        },
    )
    assert response.status_code == 200
    data = response.json()
    # AI may return a specific type or "auto" based on its analysis
    assert data["detected_diagram_type"] in ["auto", "flowchart", "design-system-architecture"]


def test_enhance_prompt_validation_error():
    response = client.post(
        "/api/prompts/enhance",
        json={
            "raw_prompt": "short",
            "diagram_type": "auto",
        },
    )
    assert response.status_code == 422


def test_enhance_prompt_timeout():
    from unittest.mock import patch
    from app.core.errors import AiTimeoutError
    from app.services.prompt_enhancer import PromptEnhancerService

    with patch.object(
        PromptEnhancerService,
        "enhance",
        side_effect=AiTimeoutError("Test timeout"),
    ):
        response = client.post(
            "/api/prompts/enhance",
            json={
                "raw_prompt": "This will time out",
                "diagram_type": "auto",
            },
        )
        assert response.status_code == 504
        data = response.json()
        assert data["code"] == "AI_TIMEOUT"
        assert "taking longer than expected" in data["suggestion"]
