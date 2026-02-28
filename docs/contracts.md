# Panic! At The Syslog — Contracts

## What contracts are

Contracts are the stable interfaces that allow independent services to evolve without breaking the system.
This project uses:

- **JSON Schemas** for bus messages (events/findings/insights),
- **OpenAPI** for the HTTP API,
- **Prompt/output schemas** for LLM-produced structured output.

Contracts live in `/contracts/**`.

## Contract locations

- Event schemas: `/contracts/events/*.json`
- OpenAPI spec: `/contracts/api/openapi.yaml`
- Prompts and output schema: `/contracts/prompts/**`
- Evaluation fixtures: `/contracts/eval/**`

## Event schemas

### raw.syslog.v1

Syslog ingress events from routers and devices.

**Required fields:**

- `schema_version`: `"1.0"`
- `event_id`: unique identifier
- `correlation_id`: trace ID
- `received_at`: ISO 8601 timestamp

### events.normalized.v1

Canonical, vendor-independent event representation produced by the normalizer.

**Required fields:**

- `schema_version`: `"1.0"`
- `event_id`: unique identifier
- `correlation_id`: inherited from raw event
- `normalized_at`: ISO 8601 timestamp
- `source_device`: string identifier

### findings.realtime.v1

Real-time findings produced by the detector (pattern matches, heuristics).

**Required fields:**

- `schema_version`: `"1.0"`
- `finding_id`: unique identifier
- `correlation_id`: inherited from event stream
- `detected_at`: ISO 8601 timestamp
- `category`: string (e.g., `"brute-force-suspected"`, `"wan-instability"`)
- `confidence`: number in range [0, 1]

### insights.recommendations.v1

Analysis output produced by the analyzer (recommendations, rationale, priority).

**Required fields:**

- `schema_version`: `"1.0"`
- `insight_id`: unique identifier (deterministically derived from `finding_id`)
- `finding_id`: links to source finding
- `correlation_id`: inherited from finding
- `analyzed_at`: ISO 8601 timestamp
- `summary`: human-readable one-liner
- `recommendation`: actionable step(s)
- `rationale`: explanation of analysis reasoning
- `priority`: one of `"low"`, `"medium"`, `"high"`, `"critical"`
- `confidence`: number in range [0, 1]

## Schema versioning rules

### Backward-compatible changes (stay in v1)

Allowed:

- Adding optional fields
- Widening enums only if consumers can ignore unknown values
- Adding new topics/streams

Not allowed:

- Removing fields
- Changing field meanings
- Changing types of existing fields
- Making an optional field required

### Breaking changes (require v2)

- Removal or type changes
- Semantic changes that alter interpretation
- Required field additions

Migration approach:

- Publish v2 alongside v1 for a time.
- Provide a bridging consumer/translator if needed.
- Update consumers and then retire v1 (with a documented deprecation window).

## Required envelope fields

Every bus message MUST include:

- `schema_version` (e.g., `"1.0"`)
- `correlation_id` (string; same across the pipeline for related work)
- A stable identifier:
  - `event_id` for raw/normalized events
  - `finding_id` for findings
  - `insight_id` for insights

## Fixtures and validation

Whenever a schema changes:

1. Update or add fixtures in `/contracts/eval/fixtures`
2. Ensure `make contract-validate` passes

## Prompt contracts

Prompts are treated as versioned artifacts. Each prompt version must:

- Produce output conforming to its `output_schema.json`
- Be evaluated against fixtures (where possible)
  See `docs/governance/prompt-versioning.md`.
