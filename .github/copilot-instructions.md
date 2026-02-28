# Panic! At The Syslog - Copilot Repository Instructions

## What this repo is
Panic! At The Syslog is an open-source, event-driven pipeline for syslog ingestion and actionable recommendations:
Ingress -> Normalize -> Detect -> Analyze -> API -> UI.

## Non-negotiables
- Contracts-first: update `/contracts/**` (schemas + fixtures) before changing producers/consumers.
- Adapter-first: infrastructure is swappable via `/libs/adapters/**` interfaces.
- OSI-only core distribution: Tier 1 defaults must be OSI-approved open source.
- External LLM providers are optional plugins and disabled by default.

## Tier 1 baseline (CI/e2e)
- Bus: Kafka
- Storage: Postgres
- Auth: built-in JWT (local users/roles)
- LLM: Ollama adapter (local-first)
- Observability: OpenTelemetry hooks + Prometheus

## Build and test expectations
- Prefer `make <target>` over ad-hoc commands.
- Required targets: `make lint`, `make test`, `make contract-validate`, `make e2e-tier1`.
- Keep tests deterministic; avoid requiring proprietary services.

## Service boundary rules
- Services do not share DB tables directly for integration.
- Integration is via message bus topics and public APIs.
- At-least-once delivery: consumers must be idempotent (dedupe by stable IDs).

## Coding conventions
- Python: type hints, structured logging, explicit error handling.
- Validate all inbound payloads at boundaries.
- No secrets, tokens, or real log samples committed.