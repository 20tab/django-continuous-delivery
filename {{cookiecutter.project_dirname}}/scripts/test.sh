#!/usr/bin/env bash

./scripts/check.sh
./scripts/coverage.sh $@
./scripts/behave.sh
./scripts/report.sh
