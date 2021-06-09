#!/usr/bin/env bash

set -e

./scripts/check.sh
./scripts/coverage.sh $@
./scripts/behave.sh
./scripts/report.sh
