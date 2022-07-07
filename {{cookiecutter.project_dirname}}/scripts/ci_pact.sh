#!/bin/sh -e

if [ "${VAULT_ADDR}" != "" ]; then
  apk update 1> /dev/null

  apk add jq 1> /dev/null

  export VAULT_TOKEN="$(./vault write -field=token auth/gitlab-jwt-${VAULT_PROJECT_PATH}/login role=gitlab-jwt-${VAULT_PROJECT_PATH}-envs-${ENV_SLUG} jwt=${CI_JOB_JWT_V2})"

  pact_secrets=`vault kv get -format='json' -field=data ${VAULT_PROJECT_PATH}/envs/${ENV_SLUG}/pact`

  export PACT_BROKER_BASE_URL=`echo ${pact_secrets} | jq -r .pact_broker_url`
  export PACT_BROKER_PASSWORD=`echo ${pact_secrets} | jq -r .pact_broker_password`
  export PACT_BROKER_USERNAME=`echo ${pact_secrets} | jq -r .pact_broker_username`
fi

case "${1}" in
  "get-secret")
    echo ${pact_secrets} | jq -r .pact_broker_auth_url
  ;;
  *)
    docker-entrypoint.sh pact-broker ${@}
  ;;
esac
