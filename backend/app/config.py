from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "FlowPilot AI"
    ENVIRONMENT: str = "local"
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    MCP_HOST: str = "127.0.0.1"
    MCP_PORT: int = 9000
    DATABASE_URL: str = "sqlite:///./data/flowpilot.db"
    PROVIDER: str = "offline"
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    DEBUG: bool = False

    @property
    def cors_origins(self) -> list[str]:
        return [item.strip() for item in self.CORS_ORIGINS.split(",") if item.strip()]

    @property
    def allowed_hosts(self) -> list[str]:
        return [item.strip() for item in self.ALLOWED_HOSTS.split(",") if item.strip()]


settings = Settings()
