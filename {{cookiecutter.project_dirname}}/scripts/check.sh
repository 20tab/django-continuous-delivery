#!/usr/bin/env bash

# Bash "strict mode", to help catch problems and bugs in the shell script
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

black -q --check .
isort -q --check .
flake8
mypy .
