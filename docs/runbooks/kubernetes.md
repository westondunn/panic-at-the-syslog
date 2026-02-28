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
2. Install chart:
   - `helm install panic-syslog deploy/helm/charts/panic-at-the-syslog -n panic-syslog`
3. Configure ingress/networking according to your environment.
4. Confirm:
   - API health
   - UI loads
   - Consumers are running and subscribed

## Notes on dependencies
You may choose to:
- Bundle Kafka/Postgres as subcharts (heavier but single install), or
- Use external managed Kafka/Postgres and point values to them (preferred in many clusters)

## Security guidance
- Restrict syslog ingress to trusted network paths.
- Use Kubernetes Secrets for credentials.
- Consider NetworkPolicies to isolate services.
- External LLM providers should remain disabled unless you meet governance requirements.