# Panic! At The Syslog — Architecture

## Overview
Panic! At The Syslog is a modular, event-driven pipeline that:
1. **Ingests** syslog from a router (and mesh nodes by implication through router logs),
2. **Normalizes** vendor-specific formats into a canonical event schema,
3. **Detects** suspicious or operationally relevant patterns in real time,
4. **Analyzes** important windows/findings using a local-first LLM,
5. **Serves** results through an API and web UI,
6. **Retains** only what is needed (raw logs short-lived; critical evidence and insights long-lived).

The platform is designed to run on anything from a single Docker host to full Kubernetes.

## Pipeline
**Ingress → Normalize → Detect → Analyze → API → UI**

### Ingress
- Receives syslog via a direct Python asyncio UDP/TCP receiver (Tier 1) or syslog-ng/rsyslog (Tier 2).
- Parses RFC 3164 syslog headers (PRI, facility, severity, hostname, program).
- Enforces rate limiting and maximum line length.
- Emits `raw.syslog.v1` messages to the bus.
- Optionally spools raw events to disk with configurable TTL for reprocessing.

### Normalizer
- Consumes `raw.syslog.v1`.
- Parses Synology Router patterns into canonical fields.
- Enriches with lightweight context (source IP, device identity hints).
- Emits `events.normalized.v1`.

### Detector
- Consumes `events.normalized.v1`.
- Applies deterministic rules and heuristics:
  - **Brute-force / auth failures**: groups auth-labelled events with warn/error severity by device; threshold ≥ 5.
  - **WAN flaps / link instability**: groups wan/link-labelled events with up/down summaries by device; threshold ≥ 3.
  - **Firewall deny flood**: groups firewall-labelled events with warn/error severity by device; threshold ≥ 10.
  - **DHCP churn**: groups dhcp-labelled events by device; threshold ≥ 5.
- Findings include severity (derived from confidence) and evidence pointers (event_id, source_device, summary) for traceability.
- Finding IDs are deterministic (SHA-256 of category + device + sorted event IDs) to guarantee idempotent consumer behavior.
- Emits `findings.realtime.v1`.

### Analyzer
- Consumes `findings.realtime.v1` and runs scheduled batch analysis over time windows.
- Uses **LLM provider abstraction**:
  - Primary: Ollama (local endpoint)
  - Optional: external provider plugin (disabled by default; governed)
- Emits `insights.recommendations.v1`.

### API
- Serves read-model queries to the UI (incidents, insights, devices, review tasks).
- Exposes OpenAPI and health endpoints.
- Enforces auth and authorization.

### UI
- Dashboards for posture, incidents, devices, insights, and review workflow.
- Clear labeling of any external processing (if enabled).

## Contracts-first boundaries
Service boundaries are **contracts**, not shared tables:
- Services integrate via the **message bus** and **public APIs**.
- JSON Schemas define event shapes and versioning rules.
- Contract changes require fixtures and validation.

## Adapter-first infrastructure
Every dependency is abstracted behind a stable interface:
- Bus: Kafka (Tier 1), NATS (Tier 2), etc.
- Storage: Postgres (Tier 1)
- Search: optional (OpenSearch)
- Auth: built-in JWT (Tier 1), OIDC providers (Tier 2)
- LLM: Ollama (Tier 1), optional external plugins (Tier 3/proprietary)
- Scheduler: in-proc / Celery / K8s CronJobs profiles

Deployment uses **profiles** to select adapters without code changes.

## Reliability & delivery semantics
- Delivery is **at-least-once**.
- Consumers must be **idempotent** (dedupe via event IDs).
- A **dead-letter stream** collects poison messages with error context.
- Correlation IDs propagate through the pipeline for traceability.

## Data retention & review workflow
- Raw syslog is retained short-term for processing and human review.
- Critical events and pinned evidence can be retained indefinitely.
- Insights (recommendations + rationale) are retained long-term.
See `docs/governance/data-retention.md`.

## Security posture (high-level)
- Do not assume syslog is trustworthy; validate and rate-limit.
- Default deployments are LAN-only; protect UI/API with auth.
- External LLM calls are off by default; if enabled they require redaction, audit, and budgets.
See `docs/governance/security.md` and `docs/governance/ai-fallback.md`.

## Scaling notes
- For higher throughput, scale Normalizer/Detector/Analyzer horizontally.
- Kafka partitions and consumer groups provide parallelism.
- Optional analytics/search backends can be introduced via adapters without rewriting services.