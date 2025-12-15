#!/usr/bin/env bash

set -euo pipefail

python3 -m manage migrate --noinput
exec python3 -m manage runserver "0.0.0.0:${INTERNAL_SERVICE_PORT:-8000}"
