.DEFAULT_GOAL := help

.PHONY: check
check:  ## Check code formatting and import sorting
	black --check .
	isort --check .
	flake8
	mypy .
	bandit -r -q -x tests .

.PHONY: dev
dev: pip_update  ## Install development requirements
	pip-sync requirements.txt

.PHONY: fix
fix:  ## Fix code formatting, linting and sorting imports
	black .
	isort .
	flake8
	mypy .
	bandit -r -q -x tests .

.PHONY: outdated
outdated:  ## Check outdated requirements and dependencies
	python3 -m pip list --outdated

.PHONY: pip
pip: pip_update  ## Compile requirements
	pip-compile -q -U -o requirements.txt requirements.in

.PHONY: pip_update
pip_update:  ## Update requirements and dependencies
	python3 -m pip install -q -U pip~=21.2.0 pip-tools~=6.3.0 setuptools~=58.2.0 wheel~=0.37.0


.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
