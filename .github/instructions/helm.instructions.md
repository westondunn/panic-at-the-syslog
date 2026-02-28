---
applyTo: "deploy/helm/**"
---

## Helm/chart rules
- Chart name: panic-at-the-syslog
- Component resource names should be short: panic-api, panic-ui, etc.
- No secrets in values.yaml; secrets must come from Kubernetes Secrets or external secret managers.
- Keep profiles as values overlays under `deploy/helm/charts/panic-at-the-syslog/profiles/`.