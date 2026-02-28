from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "events"
FIXTURES_DIR = ROOT / "contracts" / "eval" / "fixtures"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_fixtures() -> list[str]:
    errors: list[str] = []
    for fixture_path in sorted(FIXTURES_DIR.glob("*.valid.json")):
        # Prompt eval fixtures are validated separately by validate_prompt_fixtures()
        if fixture_path.name.startswith("analyzer."):
            continue
        schema_name = fixture_path.name.replace(".valid.json", ".schema.json")
        schema_path = SCHEMAS_DIR / schema_name
        if not schema_path.exists():
            errors.append(f"missing schema for fixture: {fixture_path.name} -> {schema_name}")
            continue

        schema = _load_json(schema_path)
        payload = _load_json(fixture_path)
        validator = Draft202012Validator(schema)
        validation_errors = list(validator.iter_errors(payload))
        for validation_error in validation_errors:
            message = f"{fixture_path.name}: {validation_error.message}"
            errors.append(message)
    return errors


def validate_api_stub() -> list[str]:
    api_spec = ROOT / "contracts" / "api" / "openapi.yaml"
    if not api_spec.exists():
        return ["missing OpenAPI stub: contracts/api/openapi.yaml"]
    return []


def validate_prompt_contract() -> list[str]:
    output_schema = ROOT / "contracts" / "prompts" / "analysis-output.schema.json"
    prompt_file = ROOT / "contracts" / "prompts" / "analysis.prompt.md"
    missing: list[str] = []
    if not output_schema.exists():
        missing.append("missing prompt output schema: contracts/prompts/analysis-output.schema.json")
    if not prompt_file.exists():
        missing.append("missing prompt template: contracts/prompts/analysis.prompt.md")
    return missing


def validate_prompt_versions() -> list[str]:
    """Validate versioned prompt directories under contracts/prompts/."""
    errors: list[str] = []
    prompts_dir = ROOT / "contracts" / "prompts"
    required_files = ["system.md", "user_template.md", "output_schema.json"]

    for version_dir in sorted(prompts_dir.iterdir()):
        if not version_dir.is_dir():
            continue
        for required in required_files:
            if not (version_dir / required).exists():
                errors.append(f"missing {required} in {version_dir.relative_to(ROOT)}")

        schema_path = version_dir / "output_schema.json"
        if schema_path.exists():
            try:
                schema = _load_json(schema_path)
                Draft202012Validator.check_schema(schema)
            except Exception as exc:
                errors.append(f"invalid output_schema.json in {version_dir.relative_to(ROOT)}: {exc}")

    return errors


def validate_prompt_fixtures() -> list[str]:
    """Validate prompt eval fixtures against their versioned output schemas."""
    errors: list[str] = []
    prompts_dir = ROOT / "contracts" / "prompts"

    for fixture_path in sorted(FIXTURES_DIR.glob("analyzer.v*.*.valid.json")):
        # Extract version tag, e.g. "analyzer.v1" from "analyzer.v1.brute-force.valid.json"
        parts = fixture_path.stem.replace(".valid", "").split(".", 2)
        if len(parts) < 2:
            continue
        version_tag = f"{parts[0]}.{parts[1]}"  # e.g. "analyzer.v1"
        schema_path = prompts_dir / version_tag / "output_schema.json"

        if not schema_path.exists():
            errors.append(
                f"missing prompt output schema for fixture {fixture_path.name}: "
                f"{schema_path.relative_to(ROOT)}"
            )
            continue

        schema = _load_json(schema_path)
        payload = _load_json(fixture_path)
        validator = Draft202012Validator(schema)
        for validation_error in validator.iter_errors(payload):
            errors.append(f"{fixture_path.name}: {validation_error.message}")

    return errors


def main() -> int:
    errors = []
    errors.extend(validate_fixtures())
    errors.extend(validate_api_stub())
    errors.extend(validate_prompt_contract())
    errors.extend(validate_prompt_versions())
    errors.extend(validate_prompt_fixtures())

    if errors:
        for error in errors:
            print(f"contract validation error: {error}")
        return 1

    print("contract validation ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())