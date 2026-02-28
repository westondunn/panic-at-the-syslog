"""Tests for prompt versioning structure and eval harness (Issue #27)."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


CONTRACTS_DIR = Path(__file__).resolve().parents[2] / "contracts" / "prompts"
FIXTURES_DIR = Path(__file__).resolve().parents[2] / "contracts" / "eval" / "fixtures"


def test_prompt_v1_directory_structure() -> None:
    """Versioned prompt directory must contain required files."""
    version_dir = CONTRACTS_DIR / "analyzer.v1"
    assert version_dir.is_dir(), "contracts/prompts/analyzer.v1/ must exist"
    for required in ("system.md", "user_template.md", "output_schema.json"):
        assert (version_dir / required).exists(), f"Missing {required} in analyzer.v1/"


def test_output_schema_is_valid_jsonschema() -> None:
    """output_schema.json must be a valid JSON Schema."""
    schema_path = CONTRACTS_DIR / "analyzer.v1" / "output_schema.json"
    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    Draft202012Validator.check_schema(schema)


def test_valid_fixture_passes_schema() -> None:
    """The eval fixture must validate against the output schema."""
    schema_path = CONTRACTS_DIR / "analyzer.v1" / "output_schema.json"
    fixture_path = FIXTURES_DIR / "analyzer.v1.valid.json"

    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    with fixture_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(payload))
    assert errors == [], f"Fixture validation errors: {errors}"


def test_invalid_fixture_rejected() -> None:
    """A fixture missing required fields must be rejected by the schema."""
    schema_path = CONTRACTS_DIR / "analyzer.v1" / "output_schema.json"
    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)

    bad_payload = {"summary": "missing fields"}
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(bad_payload))
    assert len(errors) > 0, "Schema should reject payload missing required fields"


def test_render_prompt_template() -> None:
    """Rendered prompt should contain the finding's category and confidence."""
    from services.analyzer.prompt import render_prompt

    rendered = render_prompt(
        category="brute-force-suspected",
        confidence=0.82,
        details={"source_ip": "192.0.2.10", "attempts": 14},
    )
    assert "brute-force-suspected" in rendered
    assert "0.82" in rendered
    assert "192.0.2.10" in rendered
