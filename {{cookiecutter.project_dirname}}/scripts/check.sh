#!/usr/bin/env bash

set -ex

bandit -r -q -x tests .
black --check .
isort --check .
flake8
mypy .
