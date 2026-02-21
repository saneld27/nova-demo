from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Auth0
    auth0_domain: str
    auth0_audience: str
    revit_provider_claim_key: str = "https://nova-demo/provider"
    revit_provider_claim_value: str = "revit-plugin"

    # OpenAI / LangGraph
    openai_api_key: str
    openai_model: str = "gpt-4o"

    # App
    app_env: str = "development"
    log_level: str = "INFO"

    @property
    def auth0_jwks_uri(self) -> str:
        return f"https://{self.auth0_domain}/.well-known/jwks.json"

    @property
    def auth0_algorithms(self) -> list[str]:
        return ["RS256"]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
