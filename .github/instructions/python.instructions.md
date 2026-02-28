---
applyTo: "**/*.py"
---

## Python standards (Panic! At The Syslog)
- Use clean architecture boundaries: domain / application / infrastructure.
- Prefer Protocol/ABC for adapter interfaces; keep concrete impls in adapter subfolders.
- All bus consumers must be idempotent and safe on retries.
- Use pydantic (or equivalent) only at boundaries; avoid leaking transport models into domain.
- Always include correlation_id propagation in logs and messages.

## Testing
- Unit tests must not require Kafka/Postgres unless explicitly marked integration.
- Prefer in-memory adapters for unit tests.