#!/bin/sh -e

if [ "${VAULT_ADDR}" != "" ]; then
  apk update && apk add curl jq

  vault_token=$(curl --silent --request POST --data "role=pact" --data "jwt=${CI_JOB_JWT_V2}" "${VAULT_ADDR%/}"/v1/auth/gitlab-jwt/login | jq -r .auth.client_token)

  pact_secrets=$(curl --silent --header "X-Vault-Token: ${vault_token}" "${VAULT_ADDR%/}"/v1/"${PROJECT_SLUG}"/pact | jq -r .data)

  PACT_BROKER_BASE_URL=$(echo "${pact_secrets}" | jq -r .pact_broker_base_url)
  PACT_BROKER_PASSWORD=$(echo "${pact_secrets}" | jq -r .pact_broker_password)
  PACT_BROKER_USERNAME=$(echo "${pact_secrets}" | jq -r .pact_broker_username)

  export PACT_BROKER_BASE_URL
  export PACT_BROKER_PASSWORD
  export PACT_BROKER_USERNAME
fi

docker-entrypoint.sh pact-broker "${@}"
