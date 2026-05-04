# Talos Submodule - Django Continuous Delivery

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

> A [Django](https://docs.djangoproject.com) service template aligned to the 20tab **Minos** platform model: per-env Vault-driven secrets, GitLab Components OpenTofu deploys, Terraform Cloud workspaces managed by the parent platform.

The generated service is meant to live as a sibling sub-repo of a platform produced by [talos](https://github.com/20tab/talos), and ships with:

-   `Dockerfile` multi-stage on `uv` + Python 3.14
-   `.gitlab-ci.yml` using `${CI_SERVER_FQDN}/components/opentofu/apply` and `registry.gitlab.com/20tab-open/minos/service:latest`
-   `minos/{development,staging,production}/this.tfvars` + `common.tfvars` per-env configs
-   Vault secret consumption at `{project}/envs/${CI_ENVIRONMENT_SLUG}/{service}/...`

## 🧩 Requirements

The Talos script can be run either using Docker or a Python virtual environment.

### 🐋 Docker

In order to run Talos via Docker, a working [Docker installation](https://docs.docker.com/get-docker/) is the only requirement.

### 🐍 Virtual environment

In order to run Talos in a virtual environment, first clone the repository in a local projects directory and ensure it is your current directory:

```console
cd ~/projects
git clone git@github.com:20tab/django-continuous-delivery.git talos-django
cd talos-django
```

Then, create and activate a virtual environment and install the requirements:

```console
python3.12 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools
python3 -m pip install -r requirements/common.txt
```

The `terraform` cli package is required, unless you want to generate a project only locally. To install it we suggest to use the official [install guide](https://learn.hashicorp.com/tutorials/terraform/install-cli).

## 🔑 Prerequisites

### 🗝️ Vault project (one-time, admin)

The Minos pipeline assumes a shared Vault auth backbone is already provisioned by the [vault-project](https://github.com/20tab/vault-project) admin repo: KV mount, GitLab JWT auth backend, JWT roles `service-gitlab-job` and `platform-gitlab-job`, identity entity, admin policy. Run that **once per Vault cluster, before** bootstrapping any platform/service.

This sub-bootstrapper only seeds **service-scoped** secrets at `{project_slug}/envs/{env}/{service_slug}/...`. Vault prompts are optional: skip them if Vault is not used for this project.

### 🦊 GitLab (optional)

If the GitLab integration is enabled, a Personal Access Token with _api_ scope is required.<br/>
It can be generated in the GitLab User Settings → Access Tokens panel.

⚠️ The token is shown only once after creation.

## 🚀️ Quickstart

Change to the projects directory, for example:

```console
cd ~/projects
```

### 🐋 Docker

```console
docker run --interactive --tty --rm --volume $PWD/.dumps:/app/.dumps --volume $PWD/.logs:/app/.logs --volume $PWD:/data 20tab/talos-django:latest
```

### 🐍 Virtual environment

```console
source talos-django/.venv/bin/activate
./talos-django/start.py
```

### Example

```console
Project name: My Project Name
Project slug [my-project-name]:
Service slug [backend]:
Project dirname (backend, myprojectname) [backend]:
Do you want to use Valkey? [y/N]:
Do you want to use Postgres? [Y/n]:
Create a database inside the Postgres cluster? [Y/n]:
Terraform Cloud organization: my-tfc-org
Do you want to use Vault for secrets management? [y/N]: y
Vault token (leave blank to perform a browser-based OIDC authentication):
Make sure your Vault permissions allow to enable the project secrets backends and manage the project secrets. Continue? [y/N]: y
Vault address: https://vault.example.com
Cluster slug hosting the 'development' environment [dev]:
Cluster slug hosting the 'staging' environment [dev]:
Cluster slug hosting the 'production' environment [main]:
Development environment complete URL [https://dev.my-project-name.com]:
Staging environment complete URL [https://stage.my-project-name.com]:
Production environment complete URL [https://www.my-project-name.com]:
Do you want to use Sentry? [y/N]:
Do you want to use GitLab? [Y/n]:
GitLab URL [https://gitlab.com]:
GitLab access token (with API scope enabled):
GitLab parent group path: 20tab/my-project-name
Media storage (digitalocean-s3, aws-s3, local, none) [digitalocean-s3]:
Initializing the backend service:
...cookiecutting the service
...generating the .env file
...formatting the cookiecut python code
...creating the '/static' directory
...creating the GitLab repository and associated resources
...creating the Vault resources with Terraform
```

## 🗒️ Arguments

The following arguments can be appended to the Docker and shell commands

#### User id

`--uid=$UID`

#### Group id

`--gid=1000`

#### Output directory

`--output-dir="~/projects"`

#### Project name

`--project-name="My project name"`

#### Project slug

`--project-slug="my-project-name"`

#### Project dirname

`--project-dirname="myprojectname"`

### 🎖️ Service

#### Service slug

`--service-slug=backend`

#### Service port

`--internal-service-port=8000`

### 📐 Architecture

#### Terraform Cloud organization

The TFC organization that owns the service workspaces. The workspaces themselves (`{project}_{service}_{env}`) are created by the parent platform via [talos](https://github.com/20tab/talos), not here.

`--terraform-cloud-organization=my-tfc-org`

#### Cluster mapping per environment

Each environment is deployed to one cluster. Cluster slugs are prompted interactively per env (defaults: `development → dev`, `staging → dev`, `production → main`). There is no CLI flag for this mapping; pass them via prompt or `--quiet` with the defaults.

#### 🗝️ Vault

`--vault-url=https://vault.example.com`<br/>
`--vault-token={{vault-token}}` (env var: `VAULT_TOKEN`; leave blank for browser-based OIDC)

Omit `--vault-url` to disable Vault integration (in that case GitLab CI vars are used as a fallback for sensitive values).

#### Project Domain

If you don't want DigitalOcean DNS configuration the following args are required

`--project-url-dev=https://dev.project-domain.com`<br/>
`--project-url-stage=https://stage.project-domain.com`<br/>
`--project-url-prod=https://www.project-domain.com`

#### Media storage

| Value           | Description                                 | Argument                          |
| --------------- | ------------------------------------------- | --------------------------------- |
| digitalocean-s3 | DigitalOcean Spaces are used to store media | `--media-storage=digitalocean-s3` |
| aws-s3          | AWS S3 are used to store media              | `--media-storage=aws-s3`          |
| local           | Docker Volume are used to store media       | `--media-storage=local`           |
| none            | Project have no media                       | `--media-storage=none`            |

#### Valkey

For enabling valkey integration the following arguments are needed:

`--use-valkey`

Disabled args
`--no-valkey`

### 🦊 GitLab

For enabling gitlab integration the following arguments are needed:

`--gitlab-url=https://gitlab.com`<br/>
`--gitlab-token={{gitlab-token}}` (env var: `GITLAB_PRIVATE_TOKEN`)<br/>
`--gitlab-namespace-path=20tab/my-project-name`

The namespace path can be nested (e.g. `20tab/my-project-name`). When invoked from talos, this is set automatically to `{parent-group}/{project-slug}`.

#### 🪖 Sentry

For enabling sentry integration the following arguments are needed:

`--sentry-org={{sentry-org}}`<br/>
`--sentry-url=https://sentry.io/`<br/>
`--sentry-dsn={{sentry-dsn}}`

#### 🔇 Quiet

No confirmations shown.

`--quiet`

### 🧰 Toolchain version overrides

The generated service pins specific versions of Python, OpenTofu and the Minos image. Defaults match the current 20tab platform; override only if needed.

| Field                        | Default                                                  | Where it lands                              |
| ---------------------------- | -------------------------------------------------------- | ------------------------------------------- |
| `python_version`             | `3.14`                                                   | `Dockerfile`, `pyproject.toml` (ruff/mypy)  |
| `minos_service_image`        | `registry.gitlab.com/20tab-open/minos/service:latest`    | `.gitlab-ci.yml` deploy image               |
| `opentofu_component_version` | `3.11.0`                                                 | GitLab Component pin in `.gitlab-ci.yml`    |
| `opentofu_version`           | `1.10.6`                                                 | OpenTofu binary version in `.gitlab-ci.yml` |

These are not exposed as CLI flags; pass them as kwargs when invoking the `Runner` directly (e.g. from talos).
