from openai import AsyncOpenAI, OpenAI

from app.core.config import settings


class OpenAIClient:
    """Singleton OpenAI client for AI operations."""

    _instance: OpenAI | None = None
    _async_instance: AsyncOpenAI | None = None

    @classmethod
    def get(cls) -> OpenAI:
        """Get the synchronous OpenAI client instance."""
        if cls._instance is None:
            api_key = settings.openai_api_key
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            cls._instance = OpenAI(api_key=api_key)
        return cls._instance

    @classmethod
    def get_async(cls) -> AsyncOpenAI:
        """Get the asynchronous OpenAI client instance."""
        if cls._async_instance is None:
            api_key = settings.openai_api_key
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            cls._async_instance = AsyncOpenAI(api_key=api_key)
        return cls._async_instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instances (useful for testing)."""
        cls._instance = None
        cls._async_instance = None
