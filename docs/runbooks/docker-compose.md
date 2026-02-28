# Panic! At The Syslog - Docker Compose Runbook

This runbook describes the Tier 1 local stack defined in:

- `deploy/compose/docker-compose.tier1.yml`

## Tier 1 scope

The Tier 1 compose stack includes:

- Kafka (message bus)
- Postgres (API storage)
- Ollama (local LLM runtime)
- Ingress, Normalizer, Detector, Analyzer
- API and UI

Stack name is explicitly pinned to:

- `panic-at-the-syslog`

## Start / reconcile

Always use `--remove-orphans` when starting after compose edits. This prevents
stale containers from older service definitions remaining attached to the same
stack name.

```bash
docker compose -f deploy/compose/docker-compose.tier1.yml up -d --build --remove-orphans
```

## Verify runtime

```bash
docker compose -f deploy/compose/docker-compose.tier1.yml ps
docker compose -f deploy/compose/docker-compose.tier1.yml ps -a
docker compose -f deploy/compose/docker-compose.tier1.yml logs --tail=100 kafka
docker compose -f deploy/compose/docker-compose.tier1.yml logs --tail=100 api
```

Expected checkpoints:

- Kafka reaches running/unfenced state and listens on `:9092`
- Postgres healthcheck passes
- API healthcheck passes on `:8000/healthz`
- UI serves on `:3000`

## Endpoints and ports

- UI: `http://localhost:3000`
- API: `http://localhost:8000`
- Kafka: `localhost:9092`
- Postgres: `localhost:5432`
- Ollama: `http://localhost:11434`
- Syslog ingress: host `1514` mapped to container `514` (UDP and TCP)

## Kafka image stability note

Tier 1 uses `bitnamilegacy/kafka:3.7` because `bitnami/kafka:3.7` is no longer
published on Docker Hub.

## Troubleshooting

- If services from old revisions still appear in `docker ps`:
  - Re-run `up` with `--remove-orphans`.
- If Kafka fails startup:
  - Check port conflicts on `9092`.
  - Inspect Kafka logs for controller/broker readiness.
- If UI cannot reach API:
  - Verify API is healthy and UI `API_BASE_URL=http://api:8000` in compose.
