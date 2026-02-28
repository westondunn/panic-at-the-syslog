# Panic! At The Syslog — Security Posture

## Threat model (high-level)
### Ingestion threats
- **Syslog spoofing**: any host on the network could send fake syslog lines.
- **Injection**: crafted messages attempting to break parsers or poison downstream analysis.
- **Burst traffic / DoS**: syslog floods causing backpressure or disk fill.

### Application/API threats
- **Unauthorized access** to logs/insights (sensitive internal topology).
- **Privilege escalation** between viewer/admin roles.
- **Secret leakage** through configs, logs, or crash dumps.

### AI-related threats
- **Data exfiltration** if external LLM fallback is enabled.
- **Prompt injection** via log lines influencing the model output.
- **Hallucinated recommendations** causing unsafe changes.

## Baseline controls (required)
1. **Network controls**
   - Restrict syslog ingress to known senders (IP allowlist where possible).
   - Prefer TCP syslog if supported; if UDP, implement rate limiting and validation.
2. **Input validation**
   - Validate message shapes at boundaries.
   - Sanitize/limit raw line length; defend parsers against pathological inputs.
3. **Auth and authorization**
   - Protect UI/API with auth.
   - Role separation: admin vs viewer.
4. **Secrets management**
   - Secrets via environment variables or secret stores only.
   - No secrets committed to git; CI includes secret scanning.
5. **Auditability**
   - Record review decisions and retention actions.
   - Record external AI usage (if enabled) with reason, redaction mode, and budgets.
6. **Safe-by-default AI**
   - External AI disabled by default.
   - Redaction enabled by default for any external call.
   - Require structured JSON outputs; reject invalid outputs.
   - Treat model output as advisory; require human review for risky actions.

## Recommended controls (strongly encouraged)
- TLS termination for UI/API if crossing trust boundaries.
- NetworkPolicies (K8s) or firewall rules (Docker host) to isolate services.
- SSO via OIDC (Keycloak/authentik) for production deployments.
- Dependency pinning and regular patching.

## Security response
- Provide a clear reporting path in `.github/SECURITY.md`.
- Treat log samples as sensitive; avoid posting unredacted logs publicly.