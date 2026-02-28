# Panic! At The Syslog - Agent Instructions

## Prime directive

Make changes in a way that keeps the repo shippable, reviewable, and open-source friendly.

## Workflow

1. Update contracts first if behavior changes cross service boundaries.
2. Implement adapter interfaces before concrete integrations.
3. Add tests (unit first; integration/e2e only when needed).
4. Update docs/support matrix when adding adapters or changing tiers.

## Safety rails

- Do not enable proprietary integrations by default.
- Do not add non-OSI dependencies to Tier 1.
- Never commit secrets or real private logs.

## Where truth lives

- Contracts: `/contracts/**`
- Governance policies: `/docs/governance/**`
- Deploy manifests: `/deploy/**`
