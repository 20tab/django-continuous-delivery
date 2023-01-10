#!/usr/bin/env bash

set -euo pipefail

python3 -m black --check .
python3 -m isort --check .
python3 -m flake8
python3 -m mypy --no-site-packages .
python3 -m bandit --quiet --recursive --exclude tests .
python3 -m pip_audit --require-hashes --requirement requirements/remote.txt
