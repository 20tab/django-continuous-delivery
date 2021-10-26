#!/bin/sh

set -euo pipefail

cd ${TF_ROOT}
gitlab-terraform init
gitlab-terraform validate
gitlab-terraform plan
gitlab-terraform plan-json
gitlab-terraform apply
