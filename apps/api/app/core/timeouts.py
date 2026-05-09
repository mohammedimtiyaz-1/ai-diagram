"""Timeout helpers for expensive API operations."""

import asyncio
from typing import Awaitable, TypeVar

from app.core.errors import TimeoutError

T = TypeVar("T")


async def with_timeout(
    coroutine: Awaitable[T],
    seconds: float,
    operation_name: str = "operation",
) -> T:
    """Run a coroutine with a strict timeout."""
    try:
        return await asyncio.wait_for(coroutine, timeout=seconds)
    except asyncio.TimeoutError:
        raise TimeoutError(
            f"{operation_name} timed out after {seconds} seconds"
        ) from None
