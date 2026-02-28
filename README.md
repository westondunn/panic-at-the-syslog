# Panic! At The Syslog

<p align="center">
  <img src="docs/panic_logo.png" alt="Panic! At The Syslog" width="500" />
</p>

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

```bash
cp .env.example .env
# Edit .env and set PANIC_JWT_SECRET (use: openssl rand -hex 32)
docker compose -f deploy/compose/docker-compose.tier1.yml up --build -d
```

For detailed instructions, see [docs/runbooks/quickstart.md](docs/runbooks/quickstart.md).

## Documentation

See `docs/README.md`.

## Contributing

See `CONTRIBUTING.md`.
