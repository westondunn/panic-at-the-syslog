# Idempotency rules for consumers
- Assume messages can be delivered multiple times.
- Dedupe using stable IDs (event_id/finding_id/insight_id).
- Writes should be upserts with unique constraints where appropriate.
- Ack only after durable write.
- Poison messages go to DLQ with error context.