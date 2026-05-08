from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]
    openai_api_key: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.cors_origins, str):
            self.cors_origins = [
                origin.strip() for origin in self.cors_origins.split(",")
            ]


settings = Settings()
