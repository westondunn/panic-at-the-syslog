# Panic! At The Syslog — Prompt Versioning & Evaluation

## Purpose
Prompts are part of the system behavior. To keep recommendations stable and reviewable:
- Prompts are versioned artifacts.
- Outputs are validated against JSON Schemas.
- Changes are evaluated against fixtures.

## Rules
1. Every prompt has a version directory:
   - `/contracts/prompts/<prompt-name>.v1/`
2. Each version must include:
   - `system.md`
   - `user_template.md`
   - `output_schema.json`
   - Optional `examples/`
3. Output must be valid JSON and pass schema validation.
4. Prompt changes must run the evaluation harness:
   - Compare outputs to expected structure and key classifications (as feasible).
5. No secrets in prompts.

## Evaluation approach
- Use sanitized fixtures (no real private identifiers).
- Keep a small suite of representative events:
  - brute-force auth failures
  - WAN flap patterns
  - repeated firewall denies
  - DHCP churn
- Track regressions:
  - missing critical issues
  - increased false positives
  - invalid JSON outputs

## Governance
Prompt changes require maintainer review, especially if they alter:
- severity mapping
- recommendation content
- redaction behavior