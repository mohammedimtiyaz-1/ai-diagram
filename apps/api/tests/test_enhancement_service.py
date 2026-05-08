import json
from unittest.mock import AsyncMock, patch

import pytest

from app.core.openai_client import OpenAIClient
from app.services.prompt_enhancer import PromptEnhancerService


@pytest.mark.asyncio
async def test_enhance_with_openai_success():
    """Test successful prompt enhancement with OpenAI."""
    service = PromptEnhancerService(max_retries=0)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = json.dumps({
        "enhanced_prompt": "Create a detailed design system architecture diagram showing design tokens, component library, and documentation.",
        "entities": [
            {"name": "Design Tokens", "type": "layer", "description": "Token system"},
            {"name": "Component Library", "type": "system", "description": "React components"},
        ],
        "relationships": [
            {"from": "Design Tokens", "to": "Component Library", "type": "styles"},
        ],
        "assumptions": ["Using React"],
        "diagram_type": "flowchart",
    })

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    return_value=mock_response,
                ):
                    result = await service.enhance("design system with tokens", "auto")

                    assert result.enhanced_prompt.startswith("Create a detailed")
                    assert "Design Tokens" in result.entities
                    assert "Component Library" in result.entities
                    assert len(result.relationships) == 1
                    assert result.relationships[0].from_entity == "Design Tokens"
                    assert result.relationships[0].to_entity == "Component Library"
                    assert result.detected_diagram_type == "flowchart"


@pytest.mark.asyncio
async def test_enhance_with_openai_fallback():
    """Test fallback enhancement when OpenAI fails."""
    service = PromptEnhancerService(max_retries=0)

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    side_effect=Exception("OpenAI error"),
                ):
                    result = await service.enhance("design system", "auto")

                    # Should fall back to simple enhancement
                    assert result.enhanced_prompt.startswith("Create a")
                    assert "design system" in result.enhanced_prompt
                    assert len(result.entities) == 3
                    assert result.assumptions is not None


@pytest.mark.asyncio
async def test_enhance_with_retry():
    """Test retry logic on OpenAI failure."""
    service = PromptEnhancerService(max_retries=1)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = json.dumps({
        "enhanced_prompt": "Enhanced prompt after retry",
        "entities": [{"name": "Entity1", "type": "layer", "description": "Test"}],
        "relationships": [],
        "assumptions": [],
        "diagram_type": "auto",
    })

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    side_effect=[Exception("First attempt fails"), mock_response],
                ):
                    result = await service.enhance("test prompt", "auto")

                    assert result.enhanced_prompt == "Enhanced prompt after retry"


@pytest.mark.asyncio
async def test_enhance_with_invalid_json():
    """Test handling of invalid JSON response from OpenAI."""
    service = PromptEnhancerService(max_retries=0)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "invalid json"

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    return_value=mock_response,
                ):
                    result = await service.enhance("test", "auto")

                    # Should fall back to simple enhancement
                    assert result.enhanced_prompt.startswith("Create a")


@pytest.mark.asyncio
async def test_enhance_with_empty_content():
    """Test handling of empty content from OpenAI."""
    service = PromptEnhancerService(max_retries=0)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = None

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    return_value=mock_response,
                ):
                    result = await service.enhance("test", "auto")

                    # Should fall back to simple enhancement
                    assert result.enhanced_prompt.startswith("Create a")
