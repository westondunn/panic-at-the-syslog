# Analyzer Prompt v1

You are analyzing normalized security findings.
Return strict JSON matching `analysis-output.schema.json`.

See `analyzer.v1/` for the versioned prompt components:
- `system.md` — system-level instructions
- `user_template.md` — per-finding template with {{category}}, {{confidence}}, {{details_json}}
- `output_schema.json` — JSON Schema that all outputs must conform to

Output must include confidence (0–1) and evidence strings supporting the analysis.