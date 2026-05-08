from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "ai-design-system-diagram-assistant-api",
    }
