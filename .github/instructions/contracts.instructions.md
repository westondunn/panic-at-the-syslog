---
applyTo: "contracts/**"
---

## Contracts rules
- Schemas are versioned and must remain backward compatible within a major version.
- Add/adjust fixtures in `contracts/eval/fixtures` whenever schemas change.
- Every event must include: schema_version, correlation_id, and a stable id (event_id/finding_id/insight_id).
- Keep enums explicit (severity/category) and required fields minimal but sufficient.