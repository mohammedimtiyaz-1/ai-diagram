import uuid
import json
import os
from datetime import datetime
from pathlib import Path

from app.schemas.conversation import Conversation, Message

DATA_DIR = Path("/Users/imtiyaz/projects/ai/ai-diagram/apps/api/data")
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"

class ConversationService:
    """File-backed conversation store."""

    _store: dict[str, Conversation] = {}

    def __init__(self):
        self._load_from_disk()

    def _load_from_disk(self):
        if not CONVERSATIONS_FILE.exists():
            return
        try:
            with open(CONVERSATIONS_FILE, "r") as f:
                data = json.load(f)
                for cid, conv_data in data.items():
                    # Handle datetime conversion
                    conv_data["created_at"] = datetime.fromisoformat(conv_data["created_at"])
                    conv_data["updated_at"] = datetime.fromisoformat(conv_data["updated_at"])
                    for msg in conv_data.get("messages", []):
                        msg["timestamp"] = datetime.fromisoformat(msg["timestamp"])
                    
                    self._store[cid] = Conversation(**conv_data)
        except Exception as e:
            print(f"Failed to load conversations: {e}")

    def _save_to_disk(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONVERSATIONS_FILE, "w") as f:
                # Helper to handle datetime in json.dump
                def serializer(obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    return obj.__dict__
                
                json_data = {cid: conv.model_dump() for cid, conv in self._store.items()}
                # model_dump() handles datetime usually if configured, 
                # but Pydantic v2 model_dump() with json mode is safer
                # or just use json.loads(conv.model_dump_json())
                
                # Let's use the cleaner pydantic method
                export_data = {}
                for cid, conv in self._store.items():
                    export_data[cid] = json.loads(conv.model_dump_json())
                
                json.dump(export_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save conversations: {e}")

    def create(self, conversation_id: str | None = None) -> str:
        cid = conversation_id or str(uuid.uuid4())
        self._store[cid] = Conversation(
            id=cid,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self._save_to_disk()
        return cid

    def get(self, conversation_id: str) -> Conversation | None:
        return self._store.get(conversation_id)

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        message_type: str,
    ) -> None:
        conv = self._store.get(conversation_id)
        if not conv:
            raise ValueError(f"Conversation not found: {conversation_id}")
        conv.messages.append(
            Message(
                id=str(uuid.uuid4()),
                role=role,
                content=content,
                message_type=message_type,
            )
        )
        conv.updated_at = datetime.utcnow()
        self._save_to_disk()

    def set_current_diagram(self, conversation_id: str, diagram_id: str) -> None:
        conv = self._store.get(conversation_id)
        if conv:
            conv.current_diagram_id = diagram_id
            if diagram_id not in conv.diagram_version_ids:
                conv.diagram_version_ids.append(diagram_id)
            self._save_to_disk()
