# Panic! At The Syslog - Support Matrix

## Tier definitions
- Tier 1: Required for CI, OSS-only defaults.
- Tier 2: Optional integrations with periodic validation.
- Tier 3: Community or proprietary plugin paths.

## Tier 1 (default, OSI-only)
| Category | Adapter | License class | Default |
|---|---|---|---|
| Bus | Kafka adapter stub | Apache-2.0 ecosystem | yes |
| Storage | PostgreSQL profile | PostgreSQL License | yes |
| Auth | Local JWT stub | Project code (MIT) | yes |
| LLM | Ollama adapter stub | MIT ecosystem | yes |
| Scheduler | Inline scheduler | Project code (MIT) | yes |
| Search | In-memory search stub | Project code (MIT) | yes |
| Ingress | Direct asyncio receiver | Project code (MIT) | yes |

## Tier 2 (optional, OSI-only)
| Category | Adapter | License class | Default |
|---|---|---|---|
| Bus | NATS adapter stub | Apache-2.0 ecosystem | no |
| Auth | OIDC via Keycloak profile | Apache-2.0 | no |
| Search | OpenSearch profile | Apache-2.0 | no |

## Tier 3 (optional plugins)
| Category | Adapter | License class | Default |
|---|---|---|---|
| LLM | OpenAI plugin stub | proprietary service | disabled |

## Policy alignment
- The default stack remains OSI-only.
- Proprietary services are isolated behind adapter plugins and disabled by default.
- Changes to tiers require updates to this matrix and `docs/governance/license-policy.md`.