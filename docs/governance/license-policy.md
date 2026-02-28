# License Policy (OSI-only Core)

## Core rules
- Tier 1 defaults must be OSI-approved components.
- Proprietary integrations are allowed only as optional plugins.
- Proprietary plugins must be disabled by default.
- Tier 1 CI must never require proprietary services.

## Adapter contribution requirements
- Document license class in `docs/support-matrix.md`.
- Keep proprietary providers outside Tier 1.
- Provide tests that run without proprietary credentials.