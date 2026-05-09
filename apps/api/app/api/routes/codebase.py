from fastapi import APIRouter, Depends, HTTPException
from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.core.timeouts import with_timeout
from app.core.errors import TimeoutError as AppTimeoutError
from app.schemas.codebase import CodebaseAnalysisRequest, CodebaseAnalysisResponse, CodebaseGenerateRequest
from app.schemas.common import ErrorResponse
from app.services.codebase_service import codebase_service
from app.services.diagram_generator import DiagramGeneratorService
from app.schemas.diagram import DiagramResult
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/codebase", tags=["codebase"])


@router.post(
    "/analyze",
    response_model=CodebaseAnalysisResponse,
    dependencies=[Depends(rate_limit(settings.analyze_rate_limit))],
)
async def analyze_codebase(request: CodebaseAnalysisRequest):
    """Analyze a public GitHub repository."""
    try:
        result = await with_timeout(
            codebase_service.analyze_repository(
                repo_url=request.repo_url,
                diagram_type=request.diagram_type,
            ),
            seconds=settings.analyze_timeout_seconds,
            operation_name="Codebase analysis",
        )
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="ANALYSIS_FAILED",
                message="Failed to analyze repository",
                suggestion="Please check the repository URL and try again.",
                retry_allowed=True,
            ).model_dump(),
        )

@router.post("/generate-diagram", response_model=DiagramResult)
async def generate_codebase_diagram(request: CodebaseGenerateRequest):
    """Generate a diagram from codebase analysis."""
    try:
        # If analysis_id is provided, we'd normally look it up.
        # For MVP, we'll re-analyze or use the provided data if we had a cache.
        # Since we don't have a cache yet, we re-analyze if necessary, 
        # but the request should ideally have the analysis summary.
        
        # To keep it simple for now, we'll re-run analysis to get the summary.
        analysis = await codebase_service.analyze_repository(
            repo_url=request.repo_url,
            diagram_type=request.diagram_type
        )
        
        generator = DiagramGeneratorService()
        result = await generator.generate_from_codebase(
            analysis_summary=analysis.architecture_summary,
            enhanced_prompt=analysis.enhanced_prompt,
            diagram_type=request.diagram_type,
            provider="mermaid",
            conversation_id=request.conversation_id,
            repo_url=request.repo_url
        )
        return result
    except Exception as e:
        logger.error(f"Codebase generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
