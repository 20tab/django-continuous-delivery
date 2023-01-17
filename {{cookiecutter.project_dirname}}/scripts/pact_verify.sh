#!/usr/bin/env bash

set -euo pipefail

python3 -m pytest --dc=Testing --disable-warnings \
  --pact-provider-name="$(PACT_PROVIDER_NAME)" \
"$@" pacts/verify_pacts.py
