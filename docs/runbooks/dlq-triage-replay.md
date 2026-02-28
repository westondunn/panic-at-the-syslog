# DLQ Triage & Replay Runbook

## Overview

The **dead-letter queue (DLQ)** captures events that a service could not
process successfully.  Each service publishes failed messages to its own DLQ
topic so operators can inspect, triage, and optionally replay them after the
root cause is resolved.

### DLQ topic naming convention

| Service     | DLQ topic              | Source topic               |
|-------------|------------------------|----------------------------|
| Normalizer  | `dlq.normalizer.v1`   | `raw.syslog.v1`           |
| Detector    | `dlq.detector.v1`     | `events.normalized.v1`    |

Additional services should follow the pattern `dlq.<service>.v1`.

## DLQ envelope schema

Every DLQ message uses a consistent envelope (see
`contracts/events/dlq.detector.v1.schema.json`):

| Field            | Description                                           |
|------------------|-------------------------------------------------------|
| `schema_version` | Always `"1.0"`.                                       |
| `dlq_id`         | Deterministic ID derived from the error and event IDs.|
| `correlation_id` | Propagated from the original event for traceability.  |
| `failed_at`      | ISO-8601 timestamp of when the failure occurred.      |
| `source_topic`   | The topic the original event was consumed from.       |
| `error`          | Human-readable error message.                         |
| `error_type`     | One of `validation`, `rule_error`, `unexpected`.      |
| `original_event` | The full original payload for reprocessing.           |

## Triage workflow

### 1. Identify DLQ messages

Consume (peek) the DLQ topic to see what is queued:

```bash
# Using the replay tool in dry-run mode to list pending messages
python -m tools.dlq_replay --dlq-topic dlq.detector.v1 --dry-run
```

In a Kafka deployment you can also use native tooling:

```bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic dlq.detector.v1 \
  --from-beginning \
  --max-messages 10
```

### 2. Classify the failure

Check the `error_type` field in each DLQ envelope:

| `error_type`  | Likely cause                            | Action                          |
|---------------|----------------------------------------|---------------------------------|
| `validation`  | Malformed event payload                | Fix upstream producer / schema  |
| `rule_error`  | Bug in a detection rule                | Fix rule code, then replay      |
| `unexpected`  | Transient or unknown error             | Investigate logs, then replay   |

### 3. Investigate root cause

- Search structured logs for the `correlation_id` from the DLQ envelope.
- Check the `error` field for stack traces or error details.
- If `error_type` is `rule_error`, review the named rule in
  `services/detector/rules.py`.

### 4. Resolve

Fix the root cause (code bug, schema mismatch, transient issue) and deploy the
fix before replaying.

## Replay

### Using the CLI tool

```bash
# Replay all DLQ messages for the detector back to the normalized events topic
python -m tools.dlq_replay \
  --dlq-topic dlq.detector.v1 \
  --target-topic events.normalized.v1

# Preview what would be replayed (no messages published)
python -m tools.dlq_replay \
  --dlq-topic dlq.detector.v1 \
  --target-topic events.normalized.v1 \
  --dry-run
```

### Replay for other services

```bash
# Replay normalizer DLQ back to raw syslog topic
python -m tools.dlq_replay \
  --dlq-topic dlq.normalizer.v1 \
  --target-topic raw.syslog.v1
```

### Post-replay verification

After replaying:

1. Monitor the target service logs for successful processing.
2. Verify the DLQ topic is no longer growing.
3. Confirm expected findings/insights appear downstream.

## Alerts & monitoring

- **Recommended**: set up an alert when any `dlq.*` topic has messages older
  than a configurable threshold (e.g., 30 minutes).
- Track DLQ depth as a Prometheus metric via the OpenTelemetry hooks.
- Include DLQ topic lag in Grafana dashboards alongside normal consumer lag.

## FAQ

**Q: Can I replay the same DLQ messages multiple times?**
A: Yes.  Downstream consumers are idempotent (dedupe by deterministic IDs), so
replaying the same events will not create duplicate findings.

**Q: What if the original event is itself malformed?**
A: The `validation` error type indicates the payload cannot be processed.
Fix the upstream producer first; replaying a malformed event will land in the
DLQ again.

**Q: How do I purge the DLQ after successful replay?**
A: In Kafka, use topic retention policies or `kafka-delete-records.sh`.
For in-memory/stub buses, DLQ messages are ephemeral.
