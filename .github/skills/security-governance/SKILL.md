# Skill: Security & Governance — Panic! At The Syslog

## When to use
Use this skill when changes touch:
- External network exposure (ingress/syslog ports)
- Authentication/authorization
- LLM providers (especially external)
- Retention/audit behaviors
- Licensing/support tier changes

## Non-negotiables
- OSI-only Tier 1 core.
- External LLM fallback disabled by default.
- If external LLM exists: redaction + audit + budgets + circuit breaker.

## Resources
- resources/osi-only.md
- resources/ai-fallback-guardrails.md