from app.providers.base import DiagramProvider
from app.providers.mermaid_provider import MermaidProvider


class ProviderRegistry:
    """Factory/registry for diagram providers."""

    _providers: dict[str, type[DiagramProvider]] = {
        "mermaid": MermaidProvider,
    }

    @classmethod
    def get(cls, name: str) -> DiagramProvider:
        provider_cls = cls._providers.get(name)
        if not provider_cls:
            raise ValueError(f"Unknown provider: {name}")
        return provider_cls()

    @classmethod
    def register(cls, name: str, provider_cls: type[DiagramProvider]) -> None:
        cls._providers[name] = provider_cls

    @classmethod
    def list(cls) -> list[str]:
        return list(cls._providers.keys())
