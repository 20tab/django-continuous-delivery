#!/bin/sh -e

# init.sh must be sourced to let it export env vars
. ${PROJECT_DIR}/scripts/deploy/init.sh

sh deploy/terraform.sh validate

sh deploy/terraform.sh plan ${var_files} -input=false -out="${plan_cache}"

sh deploy/terraform.sh show -json "${plan_cache}" | jq -r "${JQ_PLAN}" > "${plan_json}"

sh deploy/terraform.sh apply -input=false "${plan_cache}"
