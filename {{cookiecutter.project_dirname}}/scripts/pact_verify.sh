#!/usr/bin/env bash

set -euo pipefail

if [ -n "${VAULT_ID_TOKEN:-}" ]; then
  vault_token=$(curl --silent --request POST \
    --data "role=pact" \
    --data "jwt=${VAULT_ID_TOKEN}" \
    "${VAULT_ADDR%/}/v1/auth/gitlab-jwt/login" | \
    jq -r .auth.client_token)

  PACT_BROKER_URL=$(curl --silent \
    --header "X-Vault-Token: ${vault_token}" \
    "${VAULT_ADDR%/}/v1/${PROJECT_SLUG}/pact" | \
    jq -r .data.pact_broker_auth_url)

  export PACT_BROKER_URL
fi

uv run pytest --disable-warnings \
  --pact-provider-name="${PACT_PROVIDER_NAME}" \
  "${@}" pacts/verify_pacts.py
