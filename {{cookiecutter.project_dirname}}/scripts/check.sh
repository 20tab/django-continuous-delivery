#!/usr/bin/env bash

set -euo pipefail

uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run bandit -c pyproject.toml --quiet --recursive .
uvx uv-secure --no-check-uv-tool --ignore-unfixed uv.lock
