from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.core.timeouts import with_timeout
from app.core.errors import TimeoutError as AppTimeoutError, AiTimeoutError
from app.schemas.common import ErrorResponse
from app.schemas.prompt import EnhanceRequest, EnhancementResult
from app.services.prompt_enhancer import PromptEnhancerService

router = APIRouter()
enhancer = PromptEnhancerService()


@router.post(
    "/enhance",
    response_model=EnhancementResult,
    dependencies=[Depends(rate_limit(settings.enhance_rate_limit))],
)
async def enhance_prompt(request: EnhanceRequest):
    try:
        result = await with_timeout(
            enhancer.enhance(
                raw_prompt=request.raw_prompt,
                diagram_type=request.diagram_type,
            ),
            seconds=settings.enhance_timeout_seconds,
            operation_name="Prompt enhancement",
        )
        return result
    except (AppTimeoutError, AiTimeoutError) as e:
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
                code="ENHANCEMENT_FAILED",
                message=str(e),
                suggestion="Try rephrasing your description with more detail.",
                retry_allowed=True,
            ).model_dump(),
        )
