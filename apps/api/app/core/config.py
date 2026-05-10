from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    cors_origins: str = "http://localhost:3000,https://ai-design-system-diagram.vercel.app"
    openai_api_key: str = ""
    github_token: str = ""
    ai_timeout_seconds: int = 30

    # Expensive API timeouts
    enhance_timeout_seconds: int = 30
    refine_timeout_seconds: int = 45
    analyze_timeout_seconds: int = 60

    # Rate limits (requests per minute)
    enhance_rate_limit: int = 10
    refine_rate_limit: int = 8
    analyze_rate_limit: int = 5

    # ── AI Models per use-case ─────────────────────────────────────
    # Fast, small models for short prompt-shaping tasks
    enhance_model: str = "gpt-4o-mini"
    refine_model: str = "gpt-4o-mini"
    intent_model: str = "gpt-4o-mini"
    generation_model: str = "gpt-4o-mini"
    # Powerful model for deep, evidence-based codebase analysis
    analyze_model: str = "gpt-4o"
    codebase_generation_model: str = "gpt-4o"

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_origins:
            return ["*"]
        origins = [origin.strip() for origin in self.cors_origins.split(",")]
        # Ensure common variants are included
        if "https://ai-design-system-diagram.vercel.app" in origins:
            if "https://ai-design-system-diagram-three.vercel.app" not in origins:
                origins.append("https://ai-design-system-diagram-three.vercel.app")
        return origins


settings = Settings()
