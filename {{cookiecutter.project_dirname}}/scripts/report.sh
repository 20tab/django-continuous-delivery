#!/usr/bin/env bash

set -euo pipefail

python3 -m coverage combine
python3 -m coverage html
python3 -m coverage report --fail-under=100
