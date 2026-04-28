#!/usr/bin/env bash

set -euo pipefail

if [ -n "${TEST_ENV_FILE:-}" ] && [ -f "${TEST_ENV_FILE}" ]; then
  set -a && source "${TEST_ENV_FILE}" && set +a
fi

uv sync --frozen --group remote --group test

./scripts/entrypoint.sh "$@"
