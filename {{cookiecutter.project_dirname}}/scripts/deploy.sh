#!/bin/sh

set -euo pipefail

cmd=${CI_PROJECT_DIR}/scripts/terraform.sh

cd ${TF_ROOT}
${cmd} init
${cmd} validate
${cmd} plan
${cmd} plan-json
${cmd} apply -auto-approve
