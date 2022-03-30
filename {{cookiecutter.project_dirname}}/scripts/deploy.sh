#!/bin/sh

set -euo pipefail

cd ${TF_ROOT}
${TERRAFORM_CMD} init
${TERRAFORM_CMD} validate
${TERRAFORM_CMD} plan
${TERRAFORM_CMD} plan-json
${TERRAFORM_CMD} apply -auto-approve
