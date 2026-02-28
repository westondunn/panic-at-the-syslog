# Values/profiles
- Base values.yaml must run Tier 1 with OSI-only deps.
- Profiles are overlays:
  - tier1-kafka.yaml
  - tier2-nats.yaml
  - keycloak.yaml
- Any non-OSI/proprietary integration must not be present in core chart defaults.