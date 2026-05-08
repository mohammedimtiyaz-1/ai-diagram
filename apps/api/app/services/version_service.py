from datetime import datetime
import json
from pathlib import Path
from typing import Any

from app.schemas.diagram import DiagramVersionListItem

DATA_DIR = Path("/Users/imtiyaz/projects/ai/ai-diagram/apps/api/data")
VERSIONS_FILE = DATA_DIR / "versions.json"

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
        base_diagram_id: str | None = None,
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
        self.base_diagram_id = base_diagram_id
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "diagram_id": self.diagram_id,
            "conversation_id": self.conversation_id,
            "version": self.version,
            "title": self.title,
            "diagram_type": self.diagram_type,
            "provider": self.provider,
            "diagram_source": self.diagram_source,
            "diagram_format": self.diagram_format,
            "explanation": self.explanation,
            "changes_summary": self.changes_summary,
            "metadata": self.metadata,
            "base_diagram_id": self.base_diagram_id,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


class VersionService:
    """File-backed diagram version store."""

    _store: dict[str, list[VersionRecord]] = {}

    def __init__(self):
        self._load_from_disk()

    def _load_from_disk(self):
        if not VERSIONS_FILE.exists():
            return
        try:
            with open(VERSIONS_FILE, "r") as f:
                data = json.load(f)
                for cid, records_data in data.items():
                    self._store[cid] = [VersionRecord.from_dict(r) for r in records_data]
        except Exception as e:
            print(f"Failed to load versions: {e}")

    def _save_to_disk(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(VERSIONS_FILE, "w") as f:
                export_data = {
                    cid: [r.to_dict() for r in records] 
                    for cid, records in self._store.items()
                }
                json.dump(export_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save versions: {e}")

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
        base_diagram_id: str | None = None,
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
            base_diagram_id=base_diagram_id,
        )
        if conversation_id not in self._store:
            self._store[conversation_id] = []
        self._store[conversation_id].append(record)
        self._save_to_disk()
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
