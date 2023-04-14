#!/usr/bin/env bash

set -uo pipefail

python3 -m coverage combine
python3 -m coverage html
python3 -m coverage report
