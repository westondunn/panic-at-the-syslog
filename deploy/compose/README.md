# Docker Compose Files

- `docker-compose.tier1.yml`: Tier 1 local stack for `panic-at-the-syslog` with
  Kafka, Postgres, core pipeline services, API, UI, and Ollama.

## Recommended workflow

Use deterministic reconciliation to avoid stale/orphaned containers from prior
edits to the same stack:

```bash
docker compose -f deploy/compose/docker-compose.tier1.yml up -d --build --remove-orphans
```

## Kafka image note

The `bitnami/kafka:3.7` tag is no longer published. Tier 1 uses
`bitnamilegacy/kafka:3.7` to keep rebuilds stable.
