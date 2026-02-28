Create the initial v1 JSON Schemas for Panic! At The Syslog events:
- raw.syslog.v1
- events.normalized.v1
- findings.realtime.v1
- insights.recommendations.v1

Rules:
- Include schema_version and correlation_id on all messages.
- Prefer strict typing, enums for severity, and explicit required fields.
- Include a stable id field per record type (event_id/finding_id/insight_id).
- Provide example fixtures that validate against schemas.
- Add a short contracts.md in /docs explaining how to evolve schemas safely (versioning rules).