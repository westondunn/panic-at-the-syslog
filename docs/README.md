# Panic! At The Syslog — Documentation

Welcome to **Panic! At The Syslog**, an event-driven pipeline that ingests router syslog, normalizes and detects issues in real time, and produces actionable insights and recommendations using a **local-first LLM** (Ollama).

## Quick links
- Architecture: `docs/architecture.md`
- Contracts: `docs/contracts.md`
- Figma import spec: `docs/figma-import-spec.md`
- Support matrix: `docs/support-matrix.md`
- Governance:
  - Licensing: `docs/governance/licensing.md`
  - Security: `docs/governance/security.md`
  - Data retention: `docs/governance/data-retention.md`
  - AI provider policy: `docs/governance/ai-fallback.md`
  - Prompt versioning: `docs/governance/prompt-versioning.md`
- Runbooks:
  - Docker Compose: `docs/runbooks/docker-compose.md`
  - Kubernetes: `docs/runbooks/kubernetes.md`

## Design intent
This project is built for long-term maintainability and open-source contributions:
- **Contracts-first:** versioned JSON schemas define service boundaries.
- **Adapter-first:** infrastructure components are swappable without code changes.
- **OSI-only core:** the default distribution uses only OSI-approved components.
- **Compose + Kubernetes:** both are first-class deployment targets.
- **External LLM integrations:** optional plugins, **disabled by default**, with redaction, audit, and budgets.

## Glossary
- **Event:** A canonical record produced from raw syslog (normalized schema).
- **Finding:** A rule/heuristic detection derived from normalized events.
- **Insight:** An analysis/recommendation artifact (often LLM-produced), stored long-term.
- **Tier:** Support level for adapter combinations (Tier 1 is CI/e2e guaranteed).
