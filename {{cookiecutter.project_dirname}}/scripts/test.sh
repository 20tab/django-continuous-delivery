#!/usr/bin/env bash

set -ex

./scripts/check.sh
./scripts/coverage.sh $@
./scripts/behave.sh
./scripts/report.sh
