"""Web project initialization CLI constants."""

# Stacks

# BEWARE: stack names must be suitable for inclusion in Vault paths

DEV_STACK_NAME = "development"

DEV_STACK_SLUG = "dev"

STAGE_STACK_NAME = "staging"

STAGE_STACK_SLUG = "stage"

MAIN_STACK_NAME = "main"

MAIN_STACK_SLUG = "main"

STACKS_CHOICES = {
    "1": [{"name": MAIN_STACK_NAME, "slug": MAIN_STACK_SLUG}],
    "2": [
        {"name": DEV_STACK_NAME, "slug": DEV_STACK_SLUG},
        {"name": MAIN_STACK_NAME, "slug": MAIN_STACK_SLUG},
    ],
    "3": [
        {"name": DEV_STACK_NAME, "slug": DEV_STACK_SLUG},
        {"name": STAGE_STACK_NAME, "slug": STAGE_STACK_SLUG},
        {"name": MAIN_STACK_NAME, "slug": MAIN_STACK_SLUG},
    ],
}

# Environments

# BEWARE: environment names must be suitable for inclusion in Vault paths

DEV_ENV_NAME = "development"

DEV_ENV_SLUG = "dev"

DEV_ENV_STACK_CHOICES: dict[str, str] = {
    "1": MAIN_STACK_SLUG,
}

STAGE_ENV_NAME = "staging"

STAGE_ENV_SLUG = "stage"

STAGE_ENV_STACK_CHOICES: dict[str, str] = {
    "1": MAIN_STACK_SLUG,
    "2": DEV_STACK_SLUG,
}

PROD_ENV_NAME = "production"

PROD_ENV_SLUG = "prod"

PROD_ENV_STACK_CHOICES: dict[str, str] = {}

# Env vars

GITLAB_TOKEN_ENV_VAR = "GITLAB_PRIVATE_TOKEN"  # nosec B105

VAULT_TOKEN_ENV_VAR = "VAULT_TOKEN"  # nosec B105

# Deployment type

DEPLOYMENT_TYPE_DIGITALOCEAN = "digitalocean-k8s"

DEPLOYMENT_TYPE_OTHER = "other-k8s"

DEPLOYMENT_TYPE_CHOICES = [DEPLOYMENT_TYPE_DIGITALOCEAN, DEPLOYMENT_TYPE_OTHER]

# Environments distribution

ENVIRONMENTS_DISTRIBUTION_DEFAULT = "1"

ENVIRONMENTS_DISTRIBUTION_CHOICES = [ENVIRONMENTS_DISTRIBUTION_DEFAULT, "2", "3"]

ENVIRONMENTS_DISTRIBUTION_PROMPT = """Choose the environments distribution:
  1 - All environments share the same stack (Default)
  2 - Dev and Stage environments share the same stack, Prod has its own
  3 - Each environment has its own stack
"""

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

# Clusters — declared here (service-side) so env→cluster mapping has a stable vocabulary

CLUSTER_DEV_SLUG = "dev"

CLUSTER_MAIN_SLUG = "main"

# Environments — BEWARE: environment names must be suitable for inclusion in Vault paths

ENV_NAMES = ["development", "staging", "production"]

ENV_TO_CLUSTER_DEFAULT: dict[str, str] = {
    "development": CLUSTER_DEV_SLUG,
    "staging": CLUSTER_DEV_SLUG,
    "production": CLUSTER_MAIN_SLUG,
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
