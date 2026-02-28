# Panic! At The Syslog — AI Provider Policy

## Default behavior
The platform is **local-first**:
- Primary LLM provider: **Ollama** (local or LAN endpoint)
- No external providers are required for Tier 1 operation.

## Optional external provider plugin
External providers (e.g., OpenAI) may be supported as a plugin, but must be:
- **Disabled by default**
- Explicitly enabled by an admin
- Governed by redaction, budgets, and audit logging

## Requirements for any external AI call
1. **Redaction**
   - Enabled by default
   - Replace internal IPs, hostnames, MACs with stable tokens unless explicitly allowed
2. **Audit log**
   - Record: timestamp, reason for fallback, prompt version, redaction mode, response hash, model id, and token usage (if available)
3. **Budgets**
   - Enforce daily/monthly token or cost caps
   - Refuse calls when budgets are exhausted
4. **Circuit breaker**
   - Trip on repeated failures/timeouts
   - Provide a visible UI indicator when external fallback is disabled by policy or breaker

## Prompt injection and model safety
- Treat log content as untrusted input.
- Use structured outputs (JSON schema) and validate outputs strictly.
- Never auto-apply network configuration changes solely based on model output.
- Require human review for recommendations that change security posture (firewall rules, port exposure, etc.).

## External provider plugin architecture

The external LLM provider lives in a **separate plugin boundary**
(`libs/adapters/llm_external/`) so that it is never imported by default
Tier 1 / Tier 2 deploy profiles.

| Module | Purpose |
|--------|---------|
| `provider.py` | `ExternalLlmProvider` adapter — wraps any `LlmAdapter` inner implementation with governance controls. |
| `policy.py` | `PolicyGate` composite of all policy hooks (redaction, audit, budgets, circuit breaker). |

### Enabling the plugin

1. Set `enabled=True` on `ExternalLlmProvider`.
2. Supply a concrete `LlmAdapter` inner implementation (e.g. an OpenAI adapter).
3. Configure `PolicyGate` thresholds for budget limits and circuit-breaker recovery.
4. Ensure the corresponding Helm profile sets `llm.fallback.type: external`
   and provides any required secrets via Kubernetes Secrets.

### Policy hooks reference

| Hook | Default | Description |
|------|---------|-------------|
| **Redaction** | Enabled | Replaces IPs, MACs, and FQDNs with stable tokens before sending prompts externally. |
| **Audit log** | Always on | Records timestamp, correlation_id, prompt version, redaction mode, response hash, model id, and token usage. |
| **Budget** | 100,000 tokens/day, 2,000,000 tokens/month | Refuses calls when limits are exhausted; reset via `reset_daily()` / `reset_monthly()`. |
| **Circuit breaker** | 5 consecutive failures, 60 s recovery | Trips to open state on repeated failures; half-opens after recovery timeout. |

## Operational guidance
- Keep external provider integration out of default deploy manifests.
- Document data flow clearly in the UI when external processing is enabled.

## Plugin architecture

External LLM providers are implemented in `libs/adapters/llm_external_plugin.py`
as a separate module boundary, wrapped by `ExternalLlmPlugin`.

### Activation
- **Disabled by default** — not imported by any default service code.
- Requires explicit opt-in via configuration (e.g., environment variable
  `PANIC_EXTERNAL_LLM_ENABLED=true`).
- No default deploy profile (Helm `values.yaml`) enables external providers.

### Policy hooks enforced on every call
| Hook | Behavior |
|------|----------|
| **Redaction** | IPs, MACs, and other PII are replaced with `[REDACTED_*]` tokens before the prompt leaves the system. Enabled by default. |
| **Audit** | Every call is logged with: timestamp, model id, redaction mode, response length, and an optional callback for custom sinks. |
| **Budget** | A configurable token/cost cap (`budget_remaining`). Calls are refused once the budget reaches zero. |
| **Circuit breaker** | After `circuit_breaker_threshold` consecutive failures the breaker opens and all subsequent calls are immediately rejected until manually reset. |

### Policy dataclass
```python
@dataclass
class LlmPolicy:
    redaction_enabled: bool = True
    audit_callback: Callable[[dict], None] | None = None
    budget_remaining: float = 1000.0
    circuit_breaker_threshold: int = 5
```