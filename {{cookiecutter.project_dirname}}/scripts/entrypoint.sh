#!/usr/bin/env bash

set -euo pipefail

uv run -m manage migrate --noinput

exec uv run "$@"
