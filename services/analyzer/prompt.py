"""Prompt loading, rendering, and LLM output validation for the analyzer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


CONTRACTS_DIR = Path(__file__).resolve().parents[2] / "contracts" / "prompts"


class AnalyzerOutputError(Exception):
    """Raised when LLM output is not valid JSON or fails schema validation."""


def load_prompt_template(version: str = "v1") -> tuple[str, str]:
    """Return ``(system_prompt, user_template)`` for the given prompt version."""
    version_dir = CONTRACTS_DIR / f"analyzer.{version}"
    system_path = version_dir / "system.md"
    user_path = version_dir / "user_template.md"
    return system_path.read_text(encoding="utf-8"), user_path.read_text(encoding="utf-8")


def load_output_schema(version: str = "v1") -> dict[str, Any]:
    """Load the JSON Schema for prompt output validation."""
    schema_path = CONTRACTS_DIR / f"analyzer.{version}" / "output_schema.json"
    with schema_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def render_prompt(
    category: str,
    confidence: float,
    details: dict[str, Any],
    version: str = "v1",
) -> str:
    """Build a full prompt string from a finding's fields."""
    system_text, user_template = load_prompt_template(version)
    user_text = (
        user_template
        .replace("{{category}}", category)
        .replace("{{confidence}}", str(confidence))
        .replace("{{details_json}}", json.dumps(details))
    )
    return f"{system_text}\n\n{user_text}"


def validate_llm_output(raw: str, version: str = "v1") -> dict[str, Any]:
    """Parse *raw* as JSON and validate against the prompt output schema.

    Raises :class:`AnalyzerOutputError` if the text is not valid JSON or does
    not conform to the schema.
    """
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise AnalyzerOutputError(f"LLM output is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise AnalyzerOutputError(
            f"LLM output must be a JSON object, got {type(data).__name__}"
        )

    schema = load_output_schema(version)
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        messages = "; ".join(e.message for e in errors)
        raise AnalyzerOutputError(f"LLM output schema validation failed: {messages}")

    return data
