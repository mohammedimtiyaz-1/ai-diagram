from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_diagram():
    response = client.post(
        "/api/diagrams/generate",
        json={
            "raw_prompt": "I need a design system diagram showing tokens, components, and storybook",
            "enhanced_prompt": "Create a detailed design system architecture diagram showing: design tokens, component library, storybook, and Next.js app",
            "diagram_type": "design-system-architecture",
            "provider": "mermaid",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "diagram_id" in data
    assert "conversation_id" in data
    assert "title" in data
    assert "diagram_source" in data
    assert "diagram_format" == "mermaid" or data["diagram_format"] == "mermaid"
    assert "explanation" in data
    assert "version" in data
    assert data["version"] == 1


def test_refine_diagram():
    response = client.post(
        "/api/diagrams/generate",
        json={
            "raw_prompt": "I need a design system diagram showing tokens, components, and storybook",
            "enhanced_prompt": "Create a detailed design system architecture diagram",
            "diagram_type": "design-system-architecture",
            "provider": "mermaid",
        },
    )
    assert response.status_code == 200
    first = response.json()
    conversation_id = first["conversation_id"]
    diagram_id = first["diagram_id"]

    response2 = client.post(
        "/api/diagrams/refine",
        json={
            "conversation_id": conversation_id,
            "diagram_id": diagram_id,
            "followup_prompt": "Add a documentation layer with Storybook and Docusaurus",
            "current_diagram_source": first["diagram_source"],
            "provider": "mermaid",
        },
    )
    assert response2.status_code == 200
    second = response2.json()
    assert second["version"] == 2
    assert "changes_summary" in second
    assert len(second["changes_summary"]) > 0


def test_export_diagram():
    response = client.post(
        "/api/diagrams/generate",
        json={
            "raw_prompt": "I need a design system diagram showing tokens, components, and storybook",
            "enhanced_prompt": "Create a detailed design system architecture diagram",
            "diagram_type": "design-system-architecture",
            "provider": "mermaid",
        },
    )
    assert response.status_code == 200
    first = response.json()
    conversation_id = first["conversation_id"]
    diagram_id = first["diagram_id"]

    for fmt in ["mermaid", "json", "enhanced-prompt", "explanation"]:
        resp = client.post(
            "/api/diagrams/export",
            json={
                "conversation_id": conversation_id,
                "diagram_id": diagram_id,
                "format": fmt,
            },
        )
        assert resp.status_code == 200
        export_data = resp.json()
        assert export_data["format"] == fmt
        assert "content" in export_data
        assert "filename_suggestion" in export_data


def test_generate_diagram_validation_error():
    response = client.post(
        "/api/diagrams/generate",
        json={
            "raw_prompt": "short",
            "enhanced_prompt": "Create a diagram",
            "diagram_type": "design-system-architecture",
            "provider": "mermaid",
        },
    )
    assert response.status_code == 422
