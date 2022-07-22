#!/bin/sh -e

# init.sh must be sourced to let it export env vars
. ${PROJECT_DIR}/scripts/deploy/init.sh

sh ${PROJECT_DIR}/scripts/deploy/terraform.sh validate

sh ${PROJECT_DIR}/scripts/deploy/terraform.sh plan-json

sh ${PROJECT_DIR}/scripts/deploy/terraform.sh apply -auto-approve
