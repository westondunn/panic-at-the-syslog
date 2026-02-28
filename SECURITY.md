# Security Policy

## Reporting a Vulnerability

Please do not file public issues for security vulnerabilities.

**Preferred method:** [GitHub private security advisory](https://github.com/westondunn/panic-at-the-syslog/security/advisories/new)

**Fallback contact:** security@panic-at-the-syslog.local.dev

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

For detailed threat model and security controls, see [`docs/governance/security.md`](docs/governance/security.md).

## Privacy Notice

This project processes network logs which may contain sensitive information (internal IPs, hostnames, identifiers). Operators are responsible for:

- Implementing access controls to restrict who can view logs and insights.
- Following local data retention and privacy regulations.
- Redacting or anonymizing logs before sharing publicly.

See [`docs/governance/data-retention.md`](docs/governance/data-retention.md) for guidance on retention policies.
