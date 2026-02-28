# Contributing to Panic! At The Syslog

## Ground rules
- Be kind. Follow the Code of Conduct.
- Keep the core OSI-only (see `docs/governance/licensing.md`).
- Contracts-first: update `/contracts/**` before changing producers/consumers.
- Adapters-first: infrastructure dependencies must be behind `/libs/adapters/**`.

## How to contribute
1. Fork + branch from `main`
2. Make changes with tests
3. Run:
   - `make lint`
   - `make test`
   - `make contract-validate` (if contracts changed)
4. Open a PR and fill out the template

## Adding a new adapter
- Add interface conformance tests that run without proprietary services.
- Update `docs/support-matrix.md`.
- Document licensing implications in `docs/governance/licensing.md` (or adapter README).

## Reporting security issues
See `.github/SECURITY.md`.