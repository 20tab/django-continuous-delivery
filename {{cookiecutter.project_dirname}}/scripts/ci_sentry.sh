#!/bin/sh -e

apk update && apk add git

git config --global --add safe.directory "${PROJECT_DIR}"

if [ "${VAULT_ADDR}" != "" ]; then
  apk add curl jq

  vault_token=$(curl --silent --request POST --data "role=${VAULT_ROLE}" --data "jwt=${CI_JOB_JWT_V2}" "${VAULT_ADDR%/}"/v1/auth/gitlab-jwt/login | jq -r .auth.client_token)

  SENTRY_AUTH_TOKEN=$(curl --silent --header "X-Vault-Token: ${vault_token}" "${VAULT_ADDR%/}"/v1/"${PROJECT_SLUG}"/envs/"${ENV_NAME}"/sentry | jq -r .data.sentry_auth_token)
  SENTRY_DSN=$(curl --silent --header "X-Vault-Token: ${vault_token}" "${VAULT_ADDR%/}"/v1/"${PROJECT_SLUG}"/envs/"${ENV_NAME}"/"${SERVICE_SLUG}"/sentry | jq -r .data.sentry_dsn)
  export SENTRY_AUTH_TOKEN
  export SENTRY_DSN
fi

case "${1}" in
  "release")
    sentry-cli releases new "${VERSION_REF}" -p "${SENTRY_PROJECT_NAME}" --log-level=debug;
    sentry-cli releases set-commits "${VERSION_REF}" --auto --ignore-missing;
    sentry-cli releases finalize "${VERSION_REF}";
  ;;
  "success")
    sentry-cli releases deploys "${VERSION_REF}" new -e "${CI_ENVIRONMENT_NAME}" -t $((RELEASE_END-RELEASE_START));
  ;;
  "failure")
    sentry-cli send-event -m "Deploy to ${CI_ENVIRONMENT_NAME} failed.";
  ;;
esac
