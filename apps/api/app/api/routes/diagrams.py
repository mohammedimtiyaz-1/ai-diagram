from fastapi import APIRouter, HTTPException

from app.schemas.common import ErrorResponse
from app.schemas.diagram import (
    DiagramResult,
    ExportRequest,
    ExportResult,
    GenerateRequest,
    RefineRequest,
)
from app.services.diagram_generator import DiagramGeneratorService
from app.services.export_service import ExportService
from app.services.refinement_service import RefinementService

router = APIRouter()
generator = DiagramGeneratorService()
refiner = RefinementService()
export_service = ExportService()


@router.post("/api/diagrams/generate", response_model=DiagramResult)
async def generate_diagram(request: GenerateRequest):
    try:
        result = await generator.generate(
            raw_prompt=request.raw_prompt,
            enhanced_prompt=request.enhanced_prompt,
            diagram_type=request.diagram_type,
            provider=request.provider,
            conversation_id=request.conversation_id,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="GENERATION_FAILED",
                message=str(e),
                suggestion="Try simplifying your description or selecting a specific diagram type.",
                retry_allowed=True,
            ).model_dump(),
        )


@router.post("/api/diagrams/refine", response_model=DiagramResult)
async def refine_diagram(request: RefineRequest):
    try:
        result = await refiner.refine(
            conversation_id=request.conversation_id,
            diagram_id=request.diagram_id,
            followup_prompt=request.followup_prompt,
            current_diagram_source=request.current_diagram_source,
            provider=request.provider,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="REFINEMENT_FAILED",
                message=str(e),
                suggestion="Try being more specific about what to change in the diagram.",
                retry_allowed=True,
            ).model_dump(),
        )


@router.post("/api/diagrams/export", response_model=ExportResult)
async def export_diagram(request: ExportRequest):
    try:
        result = export_service.export(
            diagram_id=request.diagram_id,
            conversation_id=request.conversation_id,
            format=request.format,
        )
        return ExportResult(
            format=result["format"],
            content=result["content"],
            filename_suggestion=result["filename_suggestion"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="EXPORT_FAILED",
                message=str(e),
                retry_allowed=False,
            ).model_dump(),
        )
