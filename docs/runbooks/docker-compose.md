# Panic! At The Syslog - Docker Compose Runbook

This runbook describes running the platform with Docker Compose profiles.

## Profiles

- `tier1` (default): Kafka + Postgres + core services + UI
- `tier1-obs`: Adds Prometheus/Grafana (optional)
- `tier2-nats`: Swaps bus adapter to NATS (if enabled)
- `tier2-opensearch`: Adds OpenSearch and indexer consumer
- `keycloak`: Enables OIDC mode

> Profiles are examples; exact names should match `deploy/compose/compose.yaml`.

## Typical flow

1. Copy `.env.example` to `.env` and fill required values.
2. Start Tier 1:
   - `docker compose --profile tier1 up -d`
3. Open UI and verify health endpoints:
   - `GET /healthz` on API
   - Service readiness endpoints (if exposed internally)

## Operational notes

- Syslog ingress port:
  - Prefer mapping to non-privileged ports (e.g., 1514 UDP/TCP) unless you control host networking.
- Storage:
  - Mount volumes for Kafka and Postgres to persist data.
- Upgrades:
  - Pin versions for Kafka/Postgres images.
  - Run database migrations via a controlled job/container.

## Troubleshooting

- If ingestion is silent:
  - Confirm router syslog destination, protocol (UDP vs TCP), and port.
  - Verify container port mappings and host firewall rules.
- If the pipeline stalls:
  - Check consumer group lag in Kafka.
  - Check DLQ topics for poison messages.
