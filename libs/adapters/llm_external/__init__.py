"""External LLM provider plugin — disabled by default.

This package provides a governed, opt-in adapter for external (non-local) LLM
providers such as OpenAI.  It is intentionally kept as a separate plugin
boundary so that:

* It is never imported or activated by Tier 1 or Tier 2 deploy profiles.
* All external calls are subject to policy hooks (redaction, audit,
  budgets, circuit breaker) defined in ``policy.py``.
* Operators must explicitly enable and configure the plugin.
"""
