from fastapi import APIRouter, HTTPException

from app.schemas.common import ErrorResponse
from app.schemas.conversation import VersionListResponse
from app.services.version_service import VersionService

router = APIRouter()
version_service = VersionService()


@router.get("/{conversation_id}/versions", response_model=VersionListResponse)
async def list_versions(conversation_id: str):
    try:
        versions = version_service.get_versions(conversation_id)
        from app.schemas.diagram import DiagramVersionListItem

        version_items = [
            DiagramVersionListItem(
                diagram_id=v.diagram_id,
                version=v.version,
                title=v.title,
                diagram_type=v.diagram_type,
                changes_summary=v.changes_summary,
                created_at=v.created_at,
            )
            for v in versions
        ]
        return VersionListResponse(
            conversation_id=conversation_id,
            versions=version_items,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code="VERSION_LIST_FAILED",
                message=str(e),
                retry_allowed=False,
            ).model_dump(),
        )
