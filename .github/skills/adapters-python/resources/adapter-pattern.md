# Adapter pattern rules
- Interfaces in: /libs/adapters/<category>/interface.py
- Implementations in: /libs/adapters/<category>/<impl_name>/
- No service should import a specific impl directly.
- Selection via config (env vars / settings), wired in composition root.