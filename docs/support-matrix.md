# Panic! At The Syslog — Support Matrix

This project supports multiple infrastructure options via adapters.
To avoid a combinatorial explosion, we define support tiers.

## Tier definitions
- **Tier 1:** CI + end-to-end tests guaranteed on every PR.
- **Tier 2:** Integration tested (periodic or targeted CI), but not full e2e across all combinations.
- **Tier 3:** Adapter exists; community-supported; may require additional wiring.

## OSI-only core policy
The **core distribution** is OSI-approved open source only.
Non-OSI/proprietary integrations must be shipped as optional plugins and disabled by default.

## Tier 1 (default, OSI-only)
| Category | Implementation | Notes |
|---|---|---|
| Bus | Apache Kafka | Primary CI/e2e baseline |
| Storage | PostgreSQL | Source of truth |
| Auth | Built-in JWT | Local users/roles |
| LLM | Ollama adapter | Local-first endpoint |
| Observability | OpenTelemetry + Prometheus | Metrics + tracing hooks |

## Tier 2 (OSI-only, integration-tested)
| Category | Implementation | Notes |
|---|---|---|
| Bus | NATS JetStream | Keep watch on ecosystem governance |
| Auth | Keycloak (OIDC) | Enterprise-friendly |
| Search | OpenSearch | Full-text search; heavier |

## Tier 3 (varies)
| Category | Implementation | Notes |
|---|---|---|
| Bus | RabbitMQ | Viable, different semantics |
| Analytics | ClickHouse | High-volume analytical queries |
| Auth | authentik | OIDC alternative |
| LLM fallback | External provider plugin | Proprietary; disabled by default |

## Guidance for contributors
- New adapters must:
  - Implement the appropriate interface in `/libs/adapters/**`
  - Include tests (unit + contract conformance)
  - Update this matrix and the licensing policy
- Anything that threatens OSI-only core must be isolated behind a plugin boundary.