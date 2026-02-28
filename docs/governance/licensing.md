# Panic! At The Syslog — Licensing Policy (OSI-only Core)

## Goal
Ensure the **default distribution** of Panic! At The Syslog is composed only of **OSI-approved open source** components.

## Scope
This policy covers:
- Runtime dependencies (containers, libraries, services)
- Build tools (where relevant)
- Optional adapters and plugins

## Rules
1. **Core must be OSI-only**
   - Tier 1 dependencies must be OSI-approved.
2. **Optional non-OSI/proprietary integrations must be plugins**
   - They must be disabled by default.
   - They must not be required for Tier 1 operation.
3. **Model weights are a licensing surface**
   - The platform software can be OSI, while model weights might not be.
   - Default configurations should reference OSI-compatible weights when possible.
   - Users can supply their own models, but documentation must clearly call out the licensing responsibility.
4. **License clarity**
   - Every adapter must document its dependency license class in `docs/support-matrix.md`.
   - If there is any ambiguity, treat it as non-core until resolved.

## Contribution requirements
- New adapters must include:
  - A license note in the adapter README or docstring
  - An entry in `docs/support-matrix.md`
  - Tests that do not require proprietary services

## Practical guidance
- Prefer permissive OSI licenses (Apache-2.0/MIT/BSD) for wide adoption.
- Copyleft components are allowed if OSI-approved, but must be disclosed clearly.