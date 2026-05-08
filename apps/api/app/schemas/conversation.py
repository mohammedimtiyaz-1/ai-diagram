from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class Message(BaseModel):
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    message_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Conversation(BaseModel):
    id: str
    messages: list[Message] = Field(default_factory=list)
    current_diagram_id: str | None = None
    diagram_version_ids: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class VersionListResponse(BaseModel):
    conversation_id: str
    versions: list
