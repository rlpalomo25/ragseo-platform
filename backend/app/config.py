from functools import lru_cache

from pydantic_settings import BaseSettings

# Sentinel value used for the default admin password when none is supplied; the
# production entrypoint refuses to seed an admin with it.
DEFAULT_ADMIN_PASSWORD_PLACEHOLDER = "changeme"


class Settings(BaseSettings):
    database_url: str = "postgresql://ragseo:changeme@localhost:5432/ragseo"
    redis_url: str = "redis://localhost:6379"
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-5"
    llm_max_tokens: int = 8000
    # LLM call resilience (Fix 5): the client timeout must stay below the
    # celery soft limit (600s) so a single request timeout fits inside one
    # task slot, and the retry budget stays bounded so a flaky provider cannot
    # silently eat the whole hard limit (900s).
    llm_timeout_seconds: int = 540
    llm_max_retries: int = 2
    llm_retry_backoff_base: float = 2.0  # backoff = base * 2**attempt
    secret_key: str = "change-this-to-a-random-string"
    session_expiry_hours: int = 24
    default_admin_username: str = "admin"
    default_admin_password: str = DEFAULT_ADMIN_PASSWORD_PLACEHOLDER
    doctrine_path: str = "/app/doctrine"
    external_data_path: str = "/app/external"
    external_upload_path: str = "/app/uploads/external"

    environment: str = "development"  # "development" | "production"
    cors_origins: str = "http://localhost:3000"

    voyage_api_key: str = ""
    voyage_api_url: str = "https://api.voyageai.com/api/v1/embeddings"
    ollama_base_url: str = "http://localhost:11434"
    embedding_provider: str = "ollama"  # "ollama" | "voyage" | "none"
    embedding_model: str = "nomic-embed-text"  # 768-dim. Ollama clamps ALL nomic tags to 2048-token context
    embedding_dimensions: int = 768
    embedding_batch_size: int = 64
    embedding_context_length: int = 2048  # Ollama nomic hard cap (GGUF clamps despite params 8192)
    embedding_chars_per_token: float = 4.0  # chars-per-token budget for truncating oversized inputs

    retrieval_top_k: int = 8
    context_budget_chars: int = 24000
    chunk_max_chars: int = 4000
    governing_doc_max_chars: int = 20000

    scope_packaging_checks: bool = (
        True  # demote Doc 192 publish-readiness findings until Phase 4 packaging lands
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def embeddings_enabled(self) -> bool:
        if self.embedding_provider == "voyage":
            return bool(self.voyage_api_key)
        if self.embedding_provider == "ollama":
            return bool(self.ollama_base_url)
        return False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
