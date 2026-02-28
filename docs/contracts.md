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