from pydantic import BaseModel, Field


class EnhanceRequest(BaseModel):
    raw_prompt: str = Field(..., min_length=10, max_length=2000)
    diagram_type: str = Field(default="auto")
    source: str = Field(default="text")


class Relationship(BaseModel):
    from_entity: str = Field(alias="from")
    to_entity: str = Field(alias="to")
    type: str

    model_config = {"populate_by_name": True}


class EnhancementResult(BaseModel):
    enhanced_prompt: str
    diagram_goal: str
    detected_diagram_type: str
    entities: list[str]
    relationships: list[Relationship]
    structure_hints: str
    assumptions: list[str]
    recommended_provider: str = "mermaid"
