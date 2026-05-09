from fastapi import APIRouter, HTTPException, Depends
from app.schemas.codebase import CodebaseAnalysisRequest, CodebaseAnalysisResponse, CodebaseGenerateRequest
from app.services.codebase_service import codebase_service
from app.services.diagram_generator import DiagramGeneratorService
from app.schemas.diagram import DiagramResult
from app.core.errors import AppError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/codebase", tags=["codebase"])

@router.post("/analyze", response_model=CodebaseAnalysisResponse)
async def analyze_codebase(request: CodebaseAnalysisRequest):
    """Analyze a public GitHub repository."""
    try:
        result = await codebase_service.analyze_repository(
            repo_url=request.repo_url,
            diagram_type=request.diagram_type
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze repository")

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
