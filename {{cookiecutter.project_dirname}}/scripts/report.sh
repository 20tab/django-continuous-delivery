#!/usr/bin/env bash

set -euo pipefail

uv run coverage combine
uv run coverage html
uv run coverage xml
uv run coverage report
