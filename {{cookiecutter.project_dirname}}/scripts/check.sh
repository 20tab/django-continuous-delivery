#!/usr/bin/env bash

set -euo pipefail

python3 -m manage check
python3 -m manage makemigrations --dry-run --check
python3 -m black --check .
ruff .
python3 -m bandit --quiet --recursive --exclude tests .
python3 -m pip_audit --require-hashes --requirement requirements/remote.txt
