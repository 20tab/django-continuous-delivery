#!/usr/bin/env sh

set -e

apk update && apk add git

git config --global --add safe.directory "${PROJECT_DIR}"

if [ "${VAULT_ADDR}" != "" ]; then
  apk add curl jq

  vault_token=$(curl --silent --request POST \
    --data "role=${VAULT_ROLE}" \
    --data "jwt=${VAULT_ID_TOKEN}" \
    "${VAULT_ADDR%/}"/v1/auth/gitlab-jwt/login | \
    jq -r .auth.client_token)

  vault_base_secrets_addr="${VAULT_ADDR%/}/v1/${PROJECT_SLUG}/envs/${ENV_NAME}"

  SENTRY_AUTH_TOKEN=$(curl --silent \
    --header "X-Vault-Token: ${vault_token}" \
    "${vault_base_secrets_addr}/sentry" | \
    jq -r .data.sentry_auth_token)

  SENTRY_DSN=$(curl --silent \
    --header "X-Vault-Token: ${vault_token}" \
    "${vault_base_secrets_addr}/${SERVICE_SLUG}/sentry" | \
    jq -r .data.sentry_dsn)

  export SENTRY_AUTH_TOKEN
  export SENTRY_DSN
fi
