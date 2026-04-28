"""Web project initialization CLI constants."""

# Environments

# BEWARE: environment names must be suitable for inclusion in Vault paths

DEV_ENV_NAME = "development"

DEV_ENV_SLUG = "dev"

STAGE_ENV_NAME = "staging"

STAGE_ENV_SLUG = "stage"

PROD_ENV_NAME = "production"

PROD_ENV_SLUG = "prod"

ENV_NAMES = [DEV_ENV_NAME, STAGE_ENV_NAME, PROD_ENV_NAME]

# Env vars

GITLAB_TOKEN_ENV_VAR = "GITLAB_PRIVATE_TOKEN"  # nosec B105

VAULT_TOKEN_ENV_VAR = "VAULT_TOKEN"  # nosec B105

# Media storage

MEDIA_STORAGE_DIGITALOCEAN_S3 = "digitalocean-s3"

MEDIA_STORAGE_AWS_S3 = "aws-s3"

MEDIA_STORAGE_CHOICES = [
    MEDIA_STORAGE_DIGITALOCEAN_S3,
    MEDIA_STORAGE_AWS_S3,
    "local",
    "none",
]

# Terraform backend

TERRAFORM_BACKEND_GITLAB = "gitlab"

TERRAFORM_BACKEND_TFC = "terraform-cloud"

TERRAFORM_BACKEND_CHOICES = [TERRAFORM_BACKEND_GITLAB, TERRAFORM_BACKEND_TFC]

# GitLab

GITLAB_URL_DEFAULT = "https://gitlab.com"

# Clusters

CLUSTER_DEV_SLUG = "dev"

CLUSTER_MAIN_SLUG = "main"

ENV_TO_CLUSTER_DEFAULT: dict[str, str] = {
    DEV_ENV_NAME: CLUSTER_DEV_SLUG,
    STAGE_ENV_NAME: CLUSTER_DEV_SLUG,
    PROD_ENV_NAME: CLUSTER_MAIN_SLUG,
}

# Vault

VAULT_SERVICE_ROLE = "service-gitlab-job"

# Minos

MINOS_SERVICE_IMAGE = "registry.gitlab.com/20tab-open/minos/service:latest"

# OpenTofu

OPENTOFU_COMPONENT_VERSION = "3.11.0"

OPENTOFU_VERSION = "1.10.6"

# Python

PYTHON_VERSION_DEFAULT = "3.14"
