from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Rural Guardian Intelligence Platform"
    app_version: str = "1.0.0"
    env: str = "development"
    dev_seed: bool = False
    secret_key: str
    database_url: str
    redis_url: str
    cors_origins: str = "http://localhost:5173"
    rate_limit_per_minute: int = 60
    max_message_chars: int = 6000
    model_provider: str = "demo"
    foundry_project_endpoint: str | None = None
    foundry_agent_name: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_deployment: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_fallback_models: str = ""
    openrouter_http_referer: str | None = None
    openrouter_app_name: str = "Rural Guardian Intelligence Platform"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
