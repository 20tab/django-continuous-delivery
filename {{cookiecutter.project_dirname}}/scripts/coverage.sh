#!/usr/bin/env bash

set -euo pipefail

uv run coverage run -m pytest --no-migrations "$@"
