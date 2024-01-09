#!/usr/bin/env bash

set -euo pipefail

python3 -m manage check
python3 -m manage makemigrations --dry-run --check
python3 -m black --check .
python3 -m ruff check .
python3 -m mypy --no-site-packages .
python3 -m bandit --configfile pyproject.toml --quiet --recursive .
python3 -m pip_audit --require-hashes --disable-pip --requirement requirements/remote.txt
