from pydantic import BaseModel, Field
from typing import Literal


class ErrorResponse(BaseModel):
    code: str
    message: str
    suggestion: str | None = None
    field: str | None = None
    retry_allowed: bool = False


class SuccessResponse(BaseModel):
    success: Literal[True] = True
