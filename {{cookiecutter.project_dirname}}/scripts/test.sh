#!/usr/bin/env bash

# Bash "strict mode", to help catch problems and bugs in the shell script
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

./scripts/check.sh
./scripts/coverage.sh
./scripts/behave.sh
./scripts/report.sh
