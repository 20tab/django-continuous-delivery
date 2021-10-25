#!/usr/bin/env bash

set -euo pipefail

{% if cookiecutter.deploy_type == "digitalocean" %}cd ${TF_ROOT}
gitlab-terraform init
gitlab-terraform validate
gitlab-terraform plan
gitlab-terraform plan-json
gitlab-terraform apply{% endif %}
