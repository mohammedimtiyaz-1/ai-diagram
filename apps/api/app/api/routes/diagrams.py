from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.core.timeouts import with_timeout
from app.core.errors import TimeoutError as AppTimeoutError
from app.schemas.common import ErrorResponse
from app.schemas.diagram import (
    DiagramResult,
    DiagramStyle,
    ExportRequest,
    ExportResult,
    GenerateRequest,
    RefineRequest,
    StyleUpdateRequest,
    StyleUpdateResponse,
)
from app.services.diagram_generator import DiagramGeneratorService
from app.services.export_service import ExportService
from app.services.refinement_service import RefinementService

router = APIRouter()
generator = DiagramGeneratorService()
refiner = RefinementService()
export_service = ExportService()

# In-memory style store: { diagram_id -> DiagramStyle }
_style_store: dict[str, DiagramStyle] = {}


@router.post("/generate", response_model=DiagramResult)
async def generate_diagram(request: GenerateRequest):
    try:
        result = await generator.generate(
            raw_prompt=request.raw_prompt,
            enhanced_prompt=request.enhanced_prompt,
            diagram_type=request.diagram_type,
            provider=request.provider,
            conversation_id=request.conversation_id,
        )
        # Seed style store for the new diagram
        _style_store[result.diagram_id] = DiagramStyle()
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


@router.post(
    "/refine",
    response_model=DiagramResult,
    dependencies=[Depends(rate_limit(settings.refine_rate_limit))],
)
async def refine_diagram(request: RefineRequest):
    try:
        existing_style = _style_store.get(request.diagram_id, DiagramStyle())

        result = await with_timeout(
            refiner.refine(
                conversation_id=request.conversation_id,
                diagram_id=request.diagram_id,
                followup_prompt=request.followup_prompt,
                current_diagram_source=request.current_diagram_source,
                provider=request.provider,
                existing_nodes=request.nodes,
                existing_edges=request.edges,
                existing_style=existing_style,
            ),
            seconds=settings.refine_timeout_seconds,
            operation_name="Diagram refinement",
        )
        _style_store[result.diagram_id] = existing_style
        return result
    except AppTimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail=ErrorResponse(
                code=e.code,
                message=e.message,
                suggestion=e.suggestion,
                retry_allowed=True,
            ).model_dump(),
        )
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


@router.patch("/{diagram_id}/style", response_model=StyleUpdateResponse)
async def update_diagram_style(diagram_id: str, request: StyleUpdateRequest):
    """Update visual style of a diagram — no AI call, no topology change."""
    try:
        _style_store[diagram_id] = request.style
        return StyleUpdateResponse(diagram_id=diagram_id, style=request.style)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="STYLE_UPDATE_FAILED",
                message=str(e),
                retry_allowed=False,
            ).model_dump(),
        )


@router.get("/api/diagrams/{diagram_id}/style", response_model=StyleUpdateResponse)
async def get_diagram_style(diagram_id: str):
    """Retrieve current visual style for a diagram."""
    style = _style_store.get(diagram_id, DiagramStyle())
    return StyleUpdateResponse(diagram_id=diagram_id, style=style)


@router.post("/export", response_model=ExportResult)
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
