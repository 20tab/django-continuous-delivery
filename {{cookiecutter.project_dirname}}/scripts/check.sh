#!/usr/bin/env bash

set -ex

python3 -m black --check .
python3 -m isort --check .
python3 -m flake8
python3 -m mypy .
python3 -m bandit -r -q -x tests .
python3 -m jake ddt -q -r requirements/remote.txt
