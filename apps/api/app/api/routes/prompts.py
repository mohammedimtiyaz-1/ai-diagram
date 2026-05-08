from fastapi import APIRouter, HTTPException

from app.schemas.common import ErrorResponse
from app.schemas.prompt import EnhanceRequest, EnhancementResult
from app.services.prompt_enhancer import PromptEnhancerService

router = APIRouter()
enhancer = PromptEnhancerService()


@router.post("/api/prompts/enhance", response_model=EnhancementResult)
async def enhance_prompt(request: EnhanceRequest):
    try:
        result = await enhancer.enhance(
            raw_prompt=request.raw_prompt,
            diagram_type=request.diagram_type,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="ENHANCEMENT_FAILED",
                message=str(e),
                suggestion="Try rephrasing your description with more detail.",
                retry_allowed=True,
            ).model_dump(),
        )
