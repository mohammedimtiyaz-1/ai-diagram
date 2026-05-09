from pydantic import BaseModel, Field
from datetime import datetime


# ──────────────────────────────────────────────
# Node & Edge models
# ──────────────────────────────────────────────

class NodeMetadata(BaseModel):
    tooltip_title: str = ""
    tooltip_description: str = ""
    role: str = ""
    importance: str = "medium"   # low | medium | high
    connections_summary: str = ""
    related_files: list[str] | None = None


class NodeStyle(BaseModel):
    background_color: str | None = None
    font_color: str | None = None


class DiagramNode(BaseModel):
    id: str
    label: str
    type: str = "generic"  # token | component | documentation | workflow | testing | generic
    metadata: NodeMetadata = Field(default_factory=NodeMetadata)
    style: NodeStyle = Field(default_factory=NodeStyle)


class DiagramEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str | None = None
    description: str | None = None


# ──────────────────────────────────────────────
# Visual Style model (toolbar / static)
# ──────────────────────────────────────────────

class DiagramStyle(BaseModel):
    font_family: str = "Inter"          # Inter | Arial | Roboto | System
    font_size: str = "medium"           # small | medium | large
    font_color: str = "default"         # default | dark | muted
    node_background_color: str = "default"  # default | white | soft-blue | soft-gray | soft-purple
    diagram_background_color: str = "default"  # default | white | light-gray
    node_theme: str = "default"         # default | minimal | soft | technical | colorful | dark | enterprise


# ──────────────────────────────────────────────
# Request models
# ──────────────────────────────────────────────

class GenerateRequest(BaseModel):
    raw_prompt: str = Field(..., min_length=10, max_length=2000)
    enhanced_prompt: str
    diagram_type: str
    provider: str = Field(default="mermaid")
    conversation_id: str | None = None


class RefineRequest(BaseModel):
    conversation_id: str
    diagram_id: str
    followup_prompt: str = Field(..., min_length=3, max_length=1000)
    current_diagram_source: str
    nodes: list[DiagramNode] = Field(default_factory=list)
    provider: str = "mermaid"


class StyleUpdateRequest(BaseModel):
    style: DiagramStyle


class StyleUpdateResponse(BaseModel):
    diagram_id: str
    style: DiagramStyle
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExportRequest(BaseModel):
    conversation_id: str
    diagram_id: str
    format: str = Field(..., pattern="^(mermaid|json|enhanced-prompt|explanation)$")


# ──────────────────────────────────────────────
# Result models
# ──────────────────────────────────────────────

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
    # ── New fields ──
    nodes: list[DiagramNode] = Field(default_factory=list)
    edges: list[DiagramEdge] = Field(default_factory=list)
    style: DiagramStyle = Field(default_factory=DiagramStyle)
    change_intent: str = "NEW_DIAGRAM"   # NEW_DIAGRAM | PATCH_CHANGE | ADD_ELEMENT | REMOVE_ELEMENT | STYLE_CHANGE | REGENERATE
    is_full_regeneration: bool = True
    base_diagram_id: str | None = None
    parent_diagram_id: str | None = None
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
