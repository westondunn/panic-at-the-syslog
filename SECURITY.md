# Security Policy

## Reporting a Vulnerability

Please do not file public issues for security vulnerabilities.

**Preferred method:** [GitHub private security advisory](https://github.com/westondunn/panic-at-the-syslog/security/advisories/new)

**Fallback contact:** If you cannot use the private advisory channel, open a new GitHub issue clearly labeled "SECURITY" so maintainers can triage it promptly.

Please include:

- Description of the vulnerability and its impact
- Steps to reproduce or a proof of concept (if applicable)
- Affected versions or commits
- Suggested fix (optional)

## Supported Versions

We provide security updates for:

- The latest release
- The `main` branch

## Security Best Practices

When deploying Panic! At The Syslog:

1. **Network isolation:** Restrict syslog ingress (UDP/TCP) to known senders.
2. **Secrets management:** Use environment variables or secret stores; never commit secrets.
3. **Authentication:** Enable auth on the UI/API before exposing beyond localhost.
4. **Audit logging:** Monitor and retain logs of review decisions and retention actions.
5. **Data sensitivity:** This project processes network logs. Treat logs as sensitive; avoid posting unredacted samples publicly.
6. **AI safeguards:** If external LLM fallback is enabled, ensure redaction and audit are active by default.

## Threat Model

Panic! At The Syslog is an event-driven pipeline for ingesting, normalizing, and analyzing syslog data, then exposing insights via APIs and a UI.
The primary assets to protect are:

- **Log data:** Syslog messages and derived signals, which may contain sensitive infrastructure details.
- **Control plane:** Configuration, detection rules, pipelines, and recommendation logic.
- **User accounts and access tokens:** Credentials for operators and automation.

We assume:

- Consult your organization's data retention policy and local regulations for guidance on retention periods and deletion procedures.
- The underlying infrastructure (Kubernetes/VMs, network, host OS) is patched and hardened by the deployer.
- Deployers control network boundaries and can restrict ingress/egress.
- Tier 1 baseline uses open-source components (Kafka, Postgres, built-in JWT auth, Ollama, Prometheus).

Key threats include:

- **Unauthorized access to logs or UI/API** via weak auth, misconfiguration, or exposed admin endpoints.
- **Data exfiltration** of sensitive logs or detections from storage or message bus.
- **Log tampering or deletion** to hide malicious activity or alter recommendations.
- **Abuse of automation and recommendations** to perform unintended actions if integrated with external systems.
- **Supply-chain risks** via vulnerable dependencies, container images, or plugins.
- **LLM misuse and data leakage** when optional external LLM providers are enabled.

This project does **not** attempt to defend against:

- Compromise of the underlying host, Kubernetes cluster, or hypervisor.
- Physical attacks on hardware running the system.
- Attackers with full administrative control over your infrastructure.

## Security Controls

The project supports and/or expects the following controls in typical deployments:

- **Authentication and authorization**
  - Built-in JWT-based auth for local users/roles.
  - Role-based access to APIs and UI features; operators should restrict admin roles to trusted users.
- **Network isolation**
  - Restrict syslog ingress ports to known senders only.
  - Limit UI/API exposure to trusted networks or behind VPN/SSO where possible.
- **Least privilege and separation of services**
  - Services communicate via message bus topics and public APIs; they do not share DB tables directly.
  - Consumers are designed to be idempotent to support at-least-once delivery.
- **Data protection**
  - Use transport-layer encryption (e.g., TLS) for UI/API, message bus, and database connections where supported.
  - Apply database access controls and backups for Postgres.
- **Audit and observability**
  - OpenTelemetry hooks and Prometheus metrics provide visibility into service health and behavior.
  - Operators should enable and retain audit logs for access, configuration changes, and retention actions.
- **Configuration and secrets management**
  - Use environment variables or external secret stores; do not commit secrets to version control.
  - Treat configuration for external integrations (e.g., LLM providers) as sensitive.
- **LLM-specific safeguards**
  - External LLM providers are optional plugins and disabled by default.
  - When enabling external LLMs, ensure input redaction, access controls, and auditing are configured.
- **Dependency and supply-chain hygiene**
  - Regularly run `make lint`, `make test`, `make contract-validate`, and `make e2e-tier1`.
  - Keep dependencies and container images updated and monitor for published vulnerabilities.

## Privacy Notice

This project processes network logs which may contain sensitive information (internal IPs, hostnames, identifiers). Operators are responsible for:

- Implementing access controls to restrict who can view logs and insights.
- Following local data retention and privacy regulations.
- Redacting or anonymizing logs before sharing publicly.

See [`docs/governance/data-retention.md`](docs/governance/data-retention.md) for guidance on retention policies.
