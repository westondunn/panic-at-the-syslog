Analyze this security finding:

Category: {{category}}
Confidence: {{confidence}}
Details: {{details_json}}

Respond with a single JSON object containing:
- summary: one-line description of the finding
- risk_level: one of "low", "medium", "high", "critical"
- recommended_actions: array of actionable steps
- confidence: number between 0 and 1
- evidence: array of evidence strings supporting the analysis

JSON only. No other text.
