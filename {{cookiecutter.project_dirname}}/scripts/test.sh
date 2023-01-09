#!/usr/bin/env bash

set -euo pipefail

./scripts/check.sh
./scripts/coverage.sh
./scripts/behave.sh
./scripts/report.sh
