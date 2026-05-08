import json
from unittest.mock import AsyncMock, patch

import pytest

from app.core.openai_client import OpenAIClient
from app.providers.base import DiagramContext, DiagramResult
from app.providers.mermaid_provider import MermaidProvider


@pytest.mark.asyncio
async def test_generate_diagram_with_openai_success():
    """Test successful diagram generation with OpenAI."""
    provider = MermaidProvider(max_retries=0)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = json.dumps({
        "mermaid_code": "flowchart TD\n    A[Design Tokens] --> B[Components]",
        "title": "Design System Architecture",
        "explanation": "Shows the flow from design tokens to components",
    })

    context = DiagramContext(
        conversation_id="test-conv-1",
        entities=["Design Tokens", "Components"],
        relationships=[],
    )

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    return_value=mock_response,
                ):
                    result = await provider.generate_diagram(
                        "Create a design system diagram",
                        "flowchart",
                        context,
                    )

                    assert result.diagram_source.startswith("flowchart")
                    assert result.title == "Design System Architecture"
                    assert result.provider == "mermaid"
                    assert result.diagram_format == "mermaid"


@pytest.mark.asyncio
async def test_generate_diagram_with_fallback():
    """Test fallback diagram when OpenAI fails."""
    provider = MermaidProvider(max_retries=0)

    context = DiagramContext(
        conversation_id="test-conv-1",
        entities=["Design Tokens", "Components"],
        relationships=[],
    )

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    side_effect=Exception("OpenAI error"),
                ):
                    result = await provider.generate_diagram(
                        "Create a design system diagram",
                        "flowchart",
                        context,
                    )

                    # Should fall back to mock diagram
                    assert result.diagram_source.startswith("flowchart")
                    assert result.title == "Design System Architecture"
                    assert "fallback" in result.explanation.lower()


@pytest.mark.asyncio
async def test_generate_diagram_with_retry():
    """Test retry logic on OpenAI failure."""
    provider = MermaidProvider(max_retries=1)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = json.dumps({
        "mermaid_code": "flowchart TD\n    A[Tokens] --> B[Components]",
        "title": "Test Diagram",
        "explanation": "Test explanation",
    })

    context = DiagramContext(
        conversation_id="test-conv-1",
        entities=["Tokens", "Components"],
        relationships=[],
    )

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    side_effect=[Exception("First attempt fails"), mock_response],
                ):
                    result = await provider.generate_diagram(
                        "Test prompt",
                        "flowchart",
                        context,
                    )

                    assert result.diagram_source.startswith("flowchart")


@pytest.mark.asyncio
async def test_validate_mermaid_syntax():
    """Test Mermaid syntax validation."""
    provider = MermaidProvider()

    # Valid Mermaid
    assert provider._validate_mermaid_syntax("flowchart TD\n    A --> B")
    assert provider._validate_mermaid_syntax("sequenceDiagram\n    A->>B: Hello")

    # Invalid Mermaid
    assert not provider._validate_mermaid_syntax("")
    assert not provider._validate_mermaid_syntax("Some random text")
    assert not provider._validate_mermaid_syntax("flowchart")


@pytest.mark.asyncio
async def test_count_nodes_and_edges():
    """Test node and edge counting."""
    provider = MermaidProvider()

    mermaid_code = """flowchart TD
        A[Token 1] --> B[Token 2]
        B --> C[Component]
        C --> D[App]
    """

    assert provider._count_nodes(mermaid_code) == 4
    assert provider._count_edges(mermaid_code) >= 3


@pytest.mark.asyncio
async def test_refine_diagram_with_openai_success():
    """Test successful diagram refinement with OpenAI."""
    provider = MermaidProvider(max_retries=0)

    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = json.dumps({
        "mermaid_code": "flowchart TD\n    A[Design Tokens] --> B[Components]\n    B --> C[Storybook]\n    C --> D[App]",
        "title": "Design System Architecture (Refined)",
        "explanation": "Added Storybook documentation layer",
        "changes_summary": ["Added Storybook node", "Added connection to App"],
    })

    context = DiagramContext(
        conversation_id="test-conv-1",
        entities=["Design Tokens", "Components"],
        relationships=[],
    )

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    return_value=mock_response,
                ):
                    result = await provider.refine_diagram(
                        "flowchart TD\n    A[Design Tokens] --> B[Components]",
                        "Add Storybook documentation",
                        "flowchart",
                        context,
                    )

                    assert result.diagram_source.startswith("flowchart")
                    assert "refined" in result.title.lower()
                    assert result.changes_summary
                    assert len(result.changes_summary) >= 1


@pytest.mark.asyncio
async def test_refine_diagram_with_fallback():
    """Test fallback diagram when OpenAI fails."""
    provider = MermaidProvider(max_retries=0)

    context = DiagramContext(
        conversation_id="test-conv-1",
        entities=["Design Tokens"],
        relationships=[],
    )

    with patch.object(OpenAIClient, "get_async", return_value=AsyncMock()):
        with patch.object(OpenAIClient.get_async(), "chat", return_value=AsyncMock()):
            with patch.object(OpenAIClient.get_async().chat, "completions", return_value=AsyncMock()):
                with patch.object(
                    OpenAIClient.get_async().chat.completions,
                    "create",
                    side_effect=Exception("OpenAI error"),
                ):
                    result = await provider.refine_diagram(
                        "flowchart TD\n    A --> B",
                        "Add more details",
                        "flowchart",
                        context,
                    )

                    # Should fall back to mock diagram
                    assert result.diagram_source.startswith("flowchart")
                    assert "fallback" in result.explanation.lower()
