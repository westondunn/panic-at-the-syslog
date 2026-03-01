# Panic! At The Syslog - Docker Images

This directory contains Dockerfiles for all services in the platform.

## Structure

- **base.Dockerfile**: Base image template (not currently used by compose, kept for reference)
- **ingress.Dockerfile**: Syslog receiver (UDP/TCP)
- **normalizer.Dockerfile**: Event parser (Kafka consumer - TODO: implement consumer loop)
- **detector.Dockerfile**: Rule-based detection (Kafka consumer - TODO: implement consumer loop)
- **analyzer.Dockerfile**: LLM insights (Kafka consumer - TODO: implement consumer loop)
- **api.Dockerfile**: REST API (FastAPI/Uvicorn)
- **ui.Dockerfile**: Web dashboard (Next.js)

## Build context

All Dockerfiles use the repository root (`../..`) as the build context to access:

- `/libs/` - Shared adapters and utilities
- `/services/` - Service implementations
- `/contracts/` - Event schemas
- `requirements-dev.txt` - Python dependencies

## Local development

Build and run via docker-compose:

```bash
cd deploy/compose
docker compose -f docker-compose.tier1.yml up --build -d
```

Or build individual images:

```bash
# From repository root
docker build -f deploy/docker/api.Dockerfile -t panic-api:local .
```

## Consumer services (TODO)

The normalizer, detector, and analyzer services currently have placeholder commands. To activate them:

1. Create consumer runner scripts: `services/{service}/__main__.py`
2. Implement Kafka consumer loops using `libs/adapters/bus/kafka_stub.py` (replace with real implementation)
3. Update `CMD` in respective Dockerfiles

Example consumer pattern:

```python
# services/normalizer/__main__.py
from libs.adapters.bus.kafka import KafkaBus
from services.normalizer.app import NormalizerService

def main():
    bus = KafkaBus(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    service = NormalizerService(bus)

    # Consume from raw.syslog.v1, publish to events.normalized.v1
    for message in bus.consume("raw.syslog.v1", group_id="normalizer-cg"):
        service.process(message)

if __name__ == "__main__":
    main()
```

## Production considerations

- Use multi-stage builds to reduce image size
- Pin exact dependency versions in `requirements-dev.txt`
- Run security scans: `docker scan <image>`
- Use non-root users (already configured for most services)
- Set resource limits in Kubernetes/compose

## Related documentation

- [quickstart.md](../../docs/runbooks/quickstart.md) - Local setup guide
- [docker-compose.md](../../docs/runbooks/docker-compose.md) - Compose profiles
- [kubernetes.md](../../docs/runbooks/kubernetes.md) - Production deployment
