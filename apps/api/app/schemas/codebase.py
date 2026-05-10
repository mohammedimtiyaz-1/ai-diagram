from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from uuid import UUID


class ModuleInfo(BaseModel):
    name: str
    path: str
    responsibility: str


class CodebaseAnalysisRequest(BaseModel):
    repo_url: str = Field(..., description="The public GitHub repository URL")
    diagram_type: str = Field("auto", description="The type of diagram to generate")
    node_theme: str = Field("default", description="The visual theme for nodes")


class CodebaseAnalysisResponse(BaseModel):
    analysis_id: str
    repo_name: str
    detected_stack: List[str] = []
    important_files: List[str] = []
    major_modules: List[ModuleInfo] = []
    entry_points: List[str] = []
    deployment_targets: List[str] = []
    architecture_pattern: str = ""
    project_summary: str = ""
    architecture_summary: str = ""
    recommended_diagram_type: str = "flowchart"
    enhanced_prompt: str = ""
    warnings: List[str] = []


class CodebaseGenerateRequest(BaseModel):
    repo_url: str
    analysis_id: Optional[str] = None
    diagram_type: str = "architecture"
    node_theme: str = "default"
    conversation_id: Optional[str] = None
