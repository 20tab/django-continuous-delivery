#!/usr/bin/env bash

set -e

black -q --check .
isort -q --check .
flake8
mypy .
