#!/bin/sh -e

if [ "${VAULT_ADDR}" != "" ]; then
  apk update && apk add curl jq

  curl https://releases.hashicorp.com/vault/${VAULT_VERSION:=1.11.0}/vault_${VAULT_VERSION}_linux_386.zip --output vault.zip
  unzip vault.zip

  export VAULT_TOKEN=`./vault write -field=token auth/gitlab-jwt-${PROJECT_SLUG}/login role=envs-${ENV_SLUG} jwt=${CI_JOB_JWT_V2}`

  export SENTRY_AUTH_TOKEN=`./vault kv get -format='json' -field=data ${PROJECT_SLUG}/envs/${ENV_SLUG}/sentry | jq -r .sentry_auth_token`

  export SENTRY_DSN=`./vault kv get -format='json' -field=data ${PROJECT_SLUG}/envs/${ENV_SLUG}/sentry_${SERVICE_SLUG} | jq -r .sentry_dsn`
fi

case "${1}" in
  "release")
    sentry-cli releases new ${VERSION_REF} -p ${SENTRY_PROJECT_NAME} --log-level=debug;
    sentry-cli releases set-commits ${VERSION_REF} --auto;
    sentry-cli releases finalize ${VERSION_REF};
  ;;
  "success")
    sentry-cli releases deploys ${VERSION_REF} new -e ${CI_ENVIRONMENT_NAME} -t $((RELEASE_END-RELEASE_START));
  ;;
  "failure")
    sentry-cli send-event -m "Deploy to ${CI_ENVIRONMENT_NAME} failed.";
  ;;
esac
