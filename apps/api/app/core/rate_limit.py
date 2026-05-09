"""In-memory sliding-window rate limiter.

Replaceable with Redis later without changing the public API.
"""

import time
from dataclasses import dataclass, field
from typing import Callable
from fastapi import HTTPException, Request

from app.core.errors import RateLimitError
from app.schemas.common import ErrorResponse


@dataclass
class _Window:
    requests: list[float] = field(default_factory=list)


class RateLimiter:
    """In-memory sliding-window rate limiter keyed by client identifier."""

    def __init__(self, requests_per_minute: int):
        self.limit = requests_per_minute
        self.window_seconds = 60.0
        self._store: dict[str, _Window] = {}

    def _key(self, request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "anonymous"

    def _prune(self, window: _Window, now: float) -> None:
        cutoff = now - self.window_seconds
        window.requests[:] = [ts for ts in window.requests if ts > cutoff]

    def allow(self, request: Request) -> tuple[bool, int]:
        """Return (allowed, retry_after_seconds)."""
        key = self._key(request)
        now = time.time()
        win = self._store.setdefault(key, _Window())
        self._prune(win, now)

        if len(win.requests) >= self.limit:
            if win.requests:
                oldest = win.requests[0]
                retry_after = int(self.window_seconds - (now - oldest)) + 1
                return False, max(retry_after, 1)
            return False, 60

        win.requests.append(now)
        return True, 0


def rate_limit(requests_per_minute: int) -> Callable:
    """FastAPI dependency factory that enforces rate limiting."""
    limiter = RateLimiter(requests_per_minute=requests_per_minute)

    def _check(request: Request):
        allowed, retry_after = limiter.allow(request)
        if not allowed:
            err = RateLimitError(retry_after=retry_after)
            raise HTTPException(
                status_code=429,
                detail=ErrorResponse(
                    code=err.code,
                    message=err.message,
                    suggestion=err.suggestion,
                    retry_allowed=True,
                ).model_dump(),
                headers={"Retry-After": str(retry_after)},
            )
        return None

    return _check
