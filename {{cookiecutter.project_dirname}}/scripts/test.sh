#!/usr/bin/env bash

set -uo pipefail

./scripts/check.sh
./scripts/coverage.sh "$@"
./scripts/report.sh
