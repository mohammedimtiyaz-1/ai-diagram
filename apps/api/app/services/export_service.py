import json

from app.services.version_service import VersionService


class ExportService:
    def __init__(self, version_service: VersionService | None = None):
        self.version_service = version_service or VersionService()

    def export(self, diagram_id: str, conversation_id: str, format: str) -> dict:
        version = self.version_service.get_version_by_id(conversation_id, diagram_id)
        if not version:
            raise ValueError(f"Diagram not found: {diagram_id}")

        if format == "mermaid":
            content = version.diagram_source
            filename = f"{version.diagram_type.replace('_', '-')}.md"
        elif format == "json":
            content = json.dumps(
                {
                    "diagram_id": version.diagram_id,
                    "title": version.title,
                    "diagram_type": version.diagram_type,
                    "provider": version.provider,
                    "diagram_source": version.diagram_source,
                    "diagram_format": version.diagram_format,
                    "explanation": version.explanation,
                    "changes_summary": version.changes_summary,
                    "metadata": version.metadata,
                },
                indent=2,
            )
            filename = f"{version.diagram_type.replace('_', '-')}.json"
        elif format == "enhanced-prompt":
            content = version.explanation
            filename = "enhanced-prompt.txt"
        elif format == "explanation":
            content = version.explanation
            filename = "explanation.txt"
        else:
            content = version.diagram_source
            filename = "export.txt"

        return {
            "format": format,
            "content": content,
            "filename_suggestion": filename,
        }
