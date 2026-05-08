from datetime import datetime
from typing import Any

from app.schemas.diagram import DiagramVersionListItem


class VersionRecord:
    def __init__(
        self,
        diagram_id: str,
        conversation_id: str,
        version: int,
        title: str,
        diagram_type: str,
        provider: str,
        diagram_source: str,
        diagram_format: str,
        explanation: str,
        changes_summary: list[str],
        metadata: dict[str, Any],
        created_at: datetime | None = None,
    ):
        self.diagram_id = diagram_id
        self.conversation_id = conversation_id
        self.version = version
        self.title = title
        self.diagram_type = diagram_type
        self.provider = provider
        self.diagram_source = diagram_source
        self.diagram_format = diagram_format
        self.explanation = explanation
        self.changes_summary = changes_summary
        self.metadata = metadata
        self.created_at = created_at or datetime.utcnow()


class VersionService:
    """In-memory diagram version store."""

    _store: dict[str, list[VersionRecord]] = {}

    def create_version(
        self,
        diagram_id: str,
        conversation_id: str,
        version: int,
        title: str,
        diagram_type: str,
        provider: str,
        diagram_source: str,
        diagram_format: str,
        explanation: str,
        changes_summary: list[str],
        metadata: dict[str, Any],
    ) -> VersionRecord:
        record = VersionRecord(
            diagram_id=diagram_id,
            conversation_id=conversation_id,
            version=version,
            title=title,
            diagram_type=diagram_type,
            provider=provider,
            diagram_source=diagram_source,
            diagram_format=diagram_format,
            explanation=explanation,
            changes_summary=changes_summary,
            metadata=metadata,
        )
        if conversation_id not in self._store:
            self._store[conversation_id] = []
        self._store[conversation_id].append(record)
        return record

    def get_versions(self, conversation_id: str) -> list[VersionRecord]:
        return self._store.get(conversation_id, [])

    def get_latest_version(self, conversation_id: str) -> VersionRecord | None:
        versions = self._store.get(conversation_id, [])
        return versions[-1] if versions else None

    def get_version_by_id(self, conversation_id: str, diagram_id: str) -> VersionRecord | None:
        versions = self._store.get(conversation_id, [])
        for v in versions:
            if v.diagram_id == diagram_id:
                return v
        return None
