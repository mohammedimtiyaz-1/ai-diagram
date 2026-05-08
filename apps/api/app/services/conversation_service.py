import uuid
from datetime import datetime

from app.schemas.conversation import Conversation, Message


class ConversationService:
    """In-memory conversation store."""

    _store: dict[str, Conversation] = {}

    def create(self, conversation_id: str | None = None) -> str:
        cid = conversation_id or str(uuid.uuid4())
        self._store[cid] = Conversation(
            id=cid,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
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

    def set_current_diagram(self, conversation_id: str, diagram_id: str) -> None:
        conv = self._store.get(conversation_id)
        if conv:
            conv.current_diagram_id = diagram_id
            conv.diagram_version_ids.append(diagram_id)
