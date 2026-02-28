---
name: Workflow Orchestrator (Panic)
description: Hidden coordinator for planner, implementer, and security review handoffs.
user-invokable: false
handoffs:
  - label: Plan Work
    agent: Planner (Panic)
    prompt: Build a concise implementation plan for this request, including contracts, adapters, tests, docs, and risks.
  - label: Implement Plan
    agent: Implementer (Panic)
    prompt: Implement the approved plan with minimal diffs and provide verification status.
  - label: Security Review
    agent: Security Review (Panic)
    prompt: Review the proposed or completed changes for security, workflow hardening, and supply-chain risks.
---

Use this agent as a non-interactive workflow coordinator.

It is hidden from the user picker and intended only for handoff-based transitions.
