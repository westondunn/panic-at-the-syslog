# Panic! At The Syslog

An open-source, event-driven syslog insights platform:
**Ingress → Normalize → Detect → Analyze → API → UI**

Local-first LLM analysis via Ollama, with governed optional external provider plugins.

## Status
Scaffold phase. Contracts-first, adapter-first.

Detector service implements baseline detections (brute-force, WAN flaps, firewall denies, DHCP churn) with severity, evidence pointers, and idempotent finding IDs.

## Key principles
- OSI-only core distribution
- Contracts-first boundaries (`/contracts/**`)
- Swappable infrastructure via adapters (`/libs/adapters/**`)
- Docker Compose + Kubernetes (Helm) first-class

## Quick start (dev)
See `docs/runbooks/docker-compose.md`.

## Documentation
See `docs/README.md`.

## Contributing
See `CONTRIBUTING.md`.