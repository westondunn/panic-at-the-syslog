PROJECT_NAME := Panic! At The Syslog
PROJECT_SLUG := panic-at-the-syslog

.PHONY: lint test contract-validate e2e-tier1

lint:
	@echo "lint: not implemented – wire this target to real lint tooling (e.g., ruff, eslint) before merging"
	@false

test:
	@echo "test: not implemented – wire this target to real test tooling (e.g., pytest, npm test) before merging"
	@false

contract-validate:
	@echo "contract-validate: not implemented – wire this target to contract validation tooling before merging"
	@false

e2e-tier1:
	@echo "e2e-tier1: not implemented – wire this target to Tier 1 e2e tests before merging"
	@false
