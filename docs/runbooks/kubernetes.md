# Panic! At The Syslog — Kubernetes Runbook

This runbook describes deploying with Helm.

## Chart structure
The chart supports multiple profiles via `values.yaml` toggles:
- bus: kafka | nats | rabbitmq
- storage: postgres
- auth: builtin | keycloak | authentik
- search: none | opensearch | clickhouse
- scheduler: inproc | celery | cronjobs
- llm.primary: ollama
- llm.fallback: none | external-plugin (disabled by default)

## Recommended baseline (Tier 1)
- Kafka + Postgres + built-in JWT + Ollama

## Installation outline
1. Create namespace:
   - `kubectl create namespace panic-syslog`
2. Create required secrets:
   - `kubectl create secret generic panic-postgres-dsn --from-literal=DATABASE_URL=<dsn> -n panic-syslog`
   - `kubectl create secret generic panic-jwt --from-literal=JWT_SECRET=<secret> -n panic-syslog`
3. Install chart with a profile overlay:
   - Tier 1 (Kafka, default): `helm install panic-syslog deploy/helm/charts/panic-at-the-syslog -f deploy/helm/charts/panic-at-the-syslog/profiles/tier1-kafka.yaml -n panic-syslog`
   - Tier 2 (NATS): `helm install panic-syslog deploy/helm/charts/panic-at-the-syslog -f deploy/helm/charts/panic-at-the-syslog/profiles/tier2-nats.yaml -n panic-syslog`
   - Keycloak auth: append `-f deploy/helm/charts/panic-at-the-syslog/profiles/keycloak.yaml` to either install command above
4. Configure ingress/networking according to your environment.
5. Confirm:
   - API health
   - UI loads
   - Consumers are running and subscribed

## Profile overlays
Profile overlay files live at `deploy/helm/charts/panic-at-the-syslog/profiles/` and are applied with `helm install -f <profile>`:

| Profile file      | Description                        |
|-------------------|------------------------------------|
| tier1-kafka.yaml  | Tier 1 baseline: Kafka message bus |
| tier2-nats.yaml   | Tier 2: NATS message bus           |
| keycloak.yaml     | Keycloak OIDC authentication       |

Multiple profiles can be combined, e.g.:
```
helm install panic-syslog deploy/helm/charts/panic-at-the-syslog \
  -f deploy/helm/charts/panic-at-the-syslog/profiles/tier1-kafka.yaml \
  -f deploy/helm/charts/panic-at-the-syslog/profiles/keycloak.yaml \
  -n panic-syslog
```

## Notes on dependencies
You may choose to:
- Bundle Kafka/Postgres as subcharts (heavier but single install), or
- Use external managed Kafka/Postgres and point values to them (preferred in many clusters)

## Security guidance
- Restrict syslog ingress to trusted network paths.
- Use Kubernetes Secrets for credentials.
- Consider NetworkPolicies to isolate services.
- External LLM providers should remain disabled unless you meet governance requirements.