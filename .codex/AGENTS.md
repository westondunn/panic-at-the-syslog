# Panic! At The Syslog — Codex Working Agreements

## Mission
Build an open-source, modular syslog insights platform with:
- Pipeline architecture (Ingress → Normalize → Detect → Analyze → API → UI)
- Adapter-first design (bus, storage, auth, search, llm, scheduler)
- OSI-only defaults in the core distribution
- Deployable via Docker Compose OR Kubernetes (Helm)

## Golden rules
1. Contracts first: update `/contracts/**` before implementation.
2. No direct coupling between services via shared DB tables; services integrate via the message bus + public APIs.
3. Every external dependency must be behind an adapter interface in `/libs/adapters/**`.
4. Maintain Tier support policy:
   - Tier 1: Kafka + Postgres + JWT + Ollama (CI/e2e)
   - Tier 2/3: other adapters (integration/community)
5. Never enable proprietary integrations by default. Any OpenAI adapter must be a disabled plugin.
6. Treat model weights as a licensing surface: ship OSI-friendly defaults and document non-OSI models as user-supplied.

## Quality gates
- Run `make lint` and `make test` on changes.
- Validate schemas: `make contract-validate`
- If contracts changed, add/adjust fixtures under `/contracts/eval/fixtures`.

## Security
- No secrets committed, ever.
- External LLM calls (if present) MUST be redacted + audited + budgeted.

## Tone
Be precise, be boring, be correct. A little panic is allowed in the product name only.