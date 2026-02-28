---
applyTo: "**"
---

## Agent instruction precedence
Use this precedence order when instructions overlap:

1. Explicit task instructions in the current PR/issue/prompt.
2. Repository guardrails in `/AGENTS.md`.
3. Repository-wide Copilot guidance in `/.github/copilot-instructions.md`.
4. Path-specific rules in `/.github/instructions/*.instructions.md`.

## Conflict resolution
- If two rules conflict, follow the higher-precedence source.
- If two path-specific rules conflict, the more specific `applyTo` pattern wins.
- If ambiguity remains, choose the safest option that preserves:
  - Contracts-first boundaries (`/contracts/**`)
  - Adapter-first integration (`/libs/adapters/**`)
  - OSI-only Tier 1 defaults
  - Disabled-by-default proprietary plugins
