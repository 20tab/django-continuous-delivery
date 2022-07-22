#!/bin/sh -e

if [ "${VAULT_ADDR}" != "" ]; then
  apk update
  apk add curl jq

  curl https://releases.hashicorp.com/vault/${VAULT_VERSION:=1.11.0}/vault_${VAULT_VERSION}_linux_386.zip --output vault.zip
  unzip vault.zip

  export VAULT_TOKEN=`./vault write -field=token auth/gitlab-jwt-${VAULT_PROJECT_PATH}/login role=gitlab-jwt-${VAULT_PROJECT_PATH}-pact jwt=${CI_JOB_JWT_V2}`

  pact_secrets=`./vault kv get -format='json' -field=data ${VAULT_PROJECT_PATH}/pact`

  export PACT_BROKER_BASE_URL=`echo ${pact_secrets} | jq -r .pact_broker_base_url`
  export PACT_BROKER_PASSWORD=`echo ${pact_secrets} | jq -r .pact_broker_password`
  export PACT_BROKER_USERNAME=`echo ${pact_secrets} | jq -r .pact_broker_username`
fi

docker-entrypoint.sh pact-broker ${@}
