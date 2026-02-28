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

## Operational guidance
- Keep external provider integration out of default deploy manifests.
- Document data flow clearly in the UI when external processing is enabled.