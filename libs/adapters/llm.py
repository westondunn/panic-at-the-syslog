from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LlmResponse:
    text: str


class LlmAdapter(Protocol):
    def complete(self, prompt: str) -> LlmResponse: ...


class OllamaLlmStub:
    """Tier 1 local-first placeholder implementation."""

    def complete(self, prompt: str) -> LlmResponse:
        return LlmResponse(text=f"stubbed-ollama-response: {prompt[:48]}")


class OpenAiLlmPluginStub:
    """Optional proprietary plugin placeholder. Disabled by default."""

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def complete(self, prompt: str) -> LlmResponse:
        if not self.enabled:
            raise RuntimeError("OpenAI plugin is disabled by default")
        return LlmResponse(text=f"stubbed-openai-response: {prompt[:48]}")