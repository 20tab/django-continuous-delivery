#!/usr/bin/env bash

set -euo pipefail

uv run -m manage migrate --noinput
uv run -m manage collectstatic --clear --link --noinput

exec uv run "$@"
