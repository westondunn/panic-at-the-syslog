from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    environment: str = "dev"
    log_level: str = "INFO"
    llm_provider: str = "ollama"
    openai_plugin_enabled: bool = False


def load_settings() -> Settings:
    return Settings(
        environment=os.getenv("PANIC_ENV", "dev"),
        log_level=os.getenv("PANIC_LOG_LEVEL", "INFO"),
        llm_provider=os.getenv("PANIC_LLM_PROVIDER", "ollama"),
        openai_plugin_enabled=os.getenv("PANIC_OPENAI_PLUGIN_ENABLED", "false").lower()
        in {"1", "true", "yes"},
    )