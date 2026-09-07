#!/usr/bin/env bash

set -uo pipefail

status=0

./scripts/coverage.sh "$@" || status=1
./scripts/report.sh || status=1

exit "${status}"
