"""Tests for prompt versioning and eval harness validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = ROOT / "contracts" / "prompts"
FIXTURES_DIR = ROOT / "contracts" / "eval" / "fixtures"


class TestAnalyzerV1PromptStructure:
    """Verify the analyzer.v1 prompt directory contains all required files."""

    version_dir = PROMPTS_DIR / "analyzer.v1"

    def test_system_md_exists(self) -> None:
        assert (self.version_dir / "system.md").exists()

    def test_user_template_md_exists(self) -> None:
        assert (self.version_dir / "user_template.md").exists()

    def test_output_schema_json_exists(self) -> None:
        assert (self.version_dir / "output_schema.json").exists()

    def test_output_schema_is_valid_json_schema(self) -> None:
        schema = json.loads((self.version_dir / "output_schema.json").read_text())
        Draft202012Validator.check_schema(schema)


def _prompt_fixture_paths() -> list[Path]:
    return sorted(FIXTURES_DIR.glob("analyzer.v*.*.valid.json"))


class TestAnalyzerV1EvalFixtures:
    """Validate each prompt eval fixture against the versioned output schema."""

    @pytest.fixture()
    def schema(self) -> dict:
        schema_path = PROMPTS_DIR / "analyzer.v1" / "output_schema.json"
        return json.loads(schema_path.read_text())

    @pytest.mark.parametrize(
        "fixture_path",
        _prompt_fixture_paths(),
        ids=[p.name for p in _prompt_fixture_paths()],
    )
    def test_fixture_validates_against_schema(
        self, schema: dict, fixture_path: Path
    ) -> None:
        payload = json.loads(fixture_path.read_text())
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(payload))
        assert errors == [], f"{fixture_path.name}: {errors}"

    @pytest.mark.parametrize(
        "fixture_path",
        _prompt_fixture_paths(),
        ids=[p.name for p in _prompt_fixture_paths()],
    )
    def test_fixture_has_required_fields(self, fixture_path: Path) -> None:
        payload = json.loads(fixture_path.read_text())
        assert "summary" in payload
        assert "risk_level" in payload
        assert "recommended_actions" in payload
        assert len(payload["recommended_actions"]) >= 1
