PROJECT_NAME := Panic! At The Syslog
PROJECT_SLUG := panic-at-the-syslog

.PHONY: lint test contract-validate e2e-tier1

lint:
	ruff check .

test:
	pytest

contract-validate:
	python -m tools.contract_validate

e2e-tier1:
	PYTHONPATH=$(CURDIR) pytest -q -m e2e tests/e2e/test_tier1_smoke.py
