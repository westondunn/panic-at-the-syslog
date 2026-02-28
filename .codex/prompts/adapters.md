Define Python adapter interfaces (Protocols/ABCs) for:
- BusAdapter
- StorageAdapter
- AuthAdapter
- LLMAdapter
- SchedulerAdapter
- SearchAdapter

Requirements:
- Include minimal “in-memory/dev” implementations where appropriate so tests can run without heavy infra.
- Provide Kafka and NATS stub adapters (real wiring can be added later).
- Ensure adapters carry correlation_id and schema_version headers consistently.
- Document Tier 1 vs Tier 2/3 adapters in /docs/support-matrix.md.