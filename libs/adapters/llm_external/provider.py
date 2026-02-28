from __future__ import annotations

import hashlib

from libs.adapters.llm import LlmAdapter, LlmResponse
from libs.adapters.llm_external.policy import PolicyGate


class ExternalLlmProvider:
    """Governed external LLM adapter — disabled by default.

    All calls are gated by a :class:`PolicyGate` that enforces redaction,
    budget limits, circuit-breaker, and audit logging.

    ``inner`` should be a concrete :class:`LlmAdapter` implementation that
    actually calls the external API (e.g. OpenAI).  If no inner adapter is
    supplied the provider operates in stub mode and returns a placeholder
    response.
    """

    def __init__(
        self,
        *,
        enabled: bool = False,
        model_id: str = "external-stub",
        prompt_version: str = "1.0",
        inner: LlmAdapter | None = None,
        policy: PolicyGate | None = None,
    ) -> None:
        self.enabled = enabled
        self.model_id = model_id
        self.prompt_version = prompt_version
        self._inner = inner
        self.policy = policy or PolicyGate()

    # -- LlmAdapter Protocol --------------------------------------------------

    def complete(self, prompt: str, *, correlation_id: str = "") -> LlmResponse:
        if not self.enabled:
            raise RuntimeError(
                "External LLM provider plugin is disabled. "
                "Set enabled=True and configure policy to use."
            )

        gate = self.policy.pre_request(prompt, estimated_tokens=len(prompt.split()))
        if not gate["allowed"]:
            raise RuntimeError(
                f"External LLM call blocked by policy: {gate['reason']}"
            )

        governed_prompt: str = gate["prompt"]

        try:
            if self._inner is not None:
                response = self._inner.complete(governed_prompt)
            else:
                # Stub mode — no real API call
                response = LlmResponse(
                    text=f"external-stub-response: {governed_prompt[:48]}"
                )
            success = True
        except Exception:
            success = False
            self.policy.post_request(
                correlation_id=correlation_id,
                prompt_version=self.prompt_version,
                response_hash="",
                model_id=self.model_id,
                success=False,
                reason="inner_adapter_error",
            )
            raise

        response_hash = hashlib.sha256(response.text.encode()).hexdigest()

        self.policy.post_request(
            correlation_id=correlation_id,
            prompt_version=self.prompt_version,
            response_hash=response_hash,
            model_id=self.model_id,
            token_usage=len(response.text.split()),
            success=success,
        )

        return response
