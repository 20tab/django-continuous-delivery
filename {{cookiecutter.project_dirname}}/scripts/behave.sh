#!/usr/bin/env bash

set -euo pipefail

python3 -m manage behave --configuration=Testing --noinput --simple "$@"
