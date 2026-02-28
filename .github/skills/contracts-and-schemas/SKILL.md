# Skill: Contracts and Schemas (Panic! At The Syslog)

## When to use
Use this skill when creating or modifying:
- JSON Schemas in /contracts/events
- Fixtures under /contracts/eval
- OpenAPI in /contracts/api

## Objectives
- Preserve backward compatibility rules.
- Ensure every schema includes schema_version and correlation_id.
- Provide fixtures that validate and represent realistic syslog-derived data.

## Checklist
1. Identify whether change is backward-compatible; if not, bump major version (v2).
2. Update schema and add at least one validating fixture.
3. Update /docs/contracts.md if versioning rules evolve.
4. Run: make contract-validate

## Resources
- resources/schema-versioning.md
- resources/fixtures-checklist.md