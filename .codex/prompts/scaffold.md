You are acting as a Staff+ software architect and build engineer.

Goal: Scaffold ONLY the repository structure, CI, contracts, and adapter interfaces for “Panic! At The Syslog”.
Do NOT implement feature logic or application code beyond minimal bootstraps required for CI to run.

Requirements:
- Create monorepo layout:
  - /contracts (JSON Schemas for events + OpenAPI stub + prompt schema placeholder)
  - /libs/common (config/logging/tracing/errors/security helpers)
  - /libs/adapters (bus/storage/auth/llm/scheduler/search interfaces + kafka+nats stubs)
  - /services (ingress/normalizer/detector/analyzer/api with minimal placeholders)
  - /services/ui (Next.js skeleton placeholder)
  - /deploy (compose + helm charts skeleton)
  - /docs (architecture + governance + support matrix)
- Build Tier 1 CI to pass with placeholders:
  - lint, unit tests, contract validation, and a tiny e2e smoke test that publishes a sample event and asserts it’s consumable.
- Enforce OSI-only defaults in docs/support matrix and a license policy doc.
- Include Makefile targets used by workflows: lint, test, contract-validate, e2e-tier1.
- Ensure no proprietary services are required to run Tier 1.
- Ensure external LLM integrations (OpenAI) exist only as disabled-by-default plugins.

Output:
- Provide the complete directory tree and the contents of new files you create (no partials).
- Keep everything minimal but production-shaped (configs, placeholders, health checks, logging hooks).