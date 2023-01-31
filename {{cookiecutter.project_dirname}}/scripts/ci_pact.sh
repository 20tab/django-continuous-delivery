#!/bin/sh -e

if [ "${VAULT_ADDR}" != "" ]; then
  apk update && apk add curl jq

  export VAULT_TOKEN=`curl --silent --request POST --data "role=pact" --data "jwt=${CI_JOB_JWT_V2}" ${VAULT_ADDR%/}/v1/auth/gitlab-jwt/login | jq -r .auth.client_token`

  pact_secrets=`curl --silent --header "X-Vault-Token: ${VAULT_TOKEN}" ${VAULT_ADDR%/}/v1/${PROJECT_SLUG}/pact | jq -r .data`

  export PACT_BROKER_BASE_URL=`echo ${pact_secrets} | jq -r .pact_broker_base_url`
  export PACT_BROKER_PASSWORD=`echo ${pact_secrets} | jq -r .pact_broker_password`
  export PACT_BROKER_USERNAME=`echo ${pact_secrets} | jq -r .pact_broker_username`
fi

docker-entrypoint.sh pact-broker ${@}
