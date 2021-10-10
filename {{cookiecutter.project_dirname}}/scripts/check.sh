#!/usr/bin/env bash

set -ex

black --check .
isort --check .
flake8
mypy .
bandit -r -q -x tests .
