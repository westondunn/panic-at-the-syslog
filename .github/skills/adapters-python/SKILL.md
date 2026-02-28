# Skill: Adapter Pattern (Python) — Panic! At The Syslog

## When to use
Use this skill when adding or modifying anything under /libs/adapters/**.

## Objectives
- Keep interfaces stable (Protocols/ABCs).
- Allow swapping implementations via config without touching business logic.
- Ensure at-least-once safety via idempotent consumer design.

## Requirements
- Provide an interface + at least one testable dev/in-memory implementation.
- Add a conformance test that runs without Kafka/Postgres.

## Resources
- resources/adapter-pattern.md
- resources/idempotency.md