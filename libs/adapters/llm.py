from __future__ import annotations

import json
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LlmResponse:
    text: str
    model: str = ""


class LlmAdapter(Protocol):
    def complete(self, prompt: str) -> LlmResponse: ...


class LlmUnavailableError(Exception):
    """Raised when the LLM backend is unreachable or returns a transport error."""


class OllamaLlmAdapter:
    """Tier 1 local-first Ollama implementation.

    Connects to an Ollama HTTP endpoint (default ``http://localhost:11434``).
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3",
        timeout: int = 120,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def complete(self, prompt: str) -> LlmResponse:
        url = f"{self.base_url}/api/generate"
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return LlmResponse(
                    text=body.get("response", ""),
                    model=body.get("model", self.model),
                )
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            raise LlmUnavailableError(f"Ollama endpoint unavailable: {exc}") from exc


class OllamaLlmStub:
    """Tier 1 local-first stub for testing (no network required)."""

    def complete(self, prompt: str) -> LlmResponse:
        return LlmResponse(text=f"stubbed-ollama-response: {prompt[:48]}")


class NullLlmAdapter:
    """No-op adapter used when no LLM is configured."""

    def complete(self, prompt: str) -> LlmResponse:
        return LlmResponse(text="")


class OpenAiLlmPluginStub:
    """Optional proprietary plugin placeholder. Disabled by default."""

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def complete(self, prompt: str) -> LlmResponse:
        if not self.enabled:
            raise RuntimeError("OpenAI plugin is disabled by default")
        return LlmResponse(text=f"stubbed-openai-response: {prompt[:48]}")