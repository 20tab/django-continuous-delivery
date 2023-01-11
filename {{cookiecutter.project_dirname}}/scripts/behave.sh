#!/usr/bin/env bash

set -euo pipefail

python3 -m wait_for_it --service "${DATABASE_URL:-"postgres:5432"}"
python3 -m manage behave --configuration=Testing --noinput --simple "$@"
