from pydantic import BaseModel, Field
from datetime import datetime


class GenerateRequest(BaseModel):
    raw_prompt: str = Field(..., min_length=10, max_length=2000)
    enhanced_prompt: str
    diagram_type: str
    provider: str = Field(default="mermaid")
    conversation_id: str | None = None


class RefineRequest(BaseModel):
    conversation_id: str
    diagram_id: str
    followup_prompt: str = Field(..., min_length=10, max_length=1000)
    current_diagram_source: str
    provider: str = "mermaid"


class ExportRequest(BaseModel):
    conversation_id: str
    diagram_id: str
    format: str = Field(..., pattern="^(mermaid|json|enhanced-prompt|explanation)$")


class DiagramMetadata(BaseModel):
    node_count: int = 0
    edge_count: int = 0
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class DiagramResult(BaseModel):
    diagram_id: str
    conversation_id: str
    version: int = 1
    title: str
    diagram_type: str
    provider: str
    diagram_source: str
    diagram_format: str
    explanation: str
    changes_summary: list[str] = Field(default_factory=list)
    metadata: DiagramMetadata = Field(default_factory=DiagramMetadata)


class ExportResult(BaseModel):
    format: str
    content: str
    filename_suggestion: str


class DiagramVersionListItem(BaseModel):
    diagram_id: str
    version: int
    title: str
    diagram_type: str
    changes_summary: list[str]
    created_at: datetime
