# {{ cookiecutter.project_name }}

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A [Django](https://docs.djangoproject.com) project using [uvicorn](https://www.uvicorn.org/#running-with-gunicorn) ASGI server.

## Index

-   [Conventions](#conventions)
-   [Initialization](#initialization)
-   [Git](#git)
    -   [Git clone](#git-clone)
    -   [Git hooks](#git-hooks)
-   [Commands](#commands)
    -   [List available commands](#list-available-commands)
    -   [List outdated dependencies](#list-outdated-dependencies)
    -   [Upgrade dependencies](#upgrade-dependencies)
-   [Testing](#testing)
-   [Static files](#static-files)
-   [Continuous Integration](#continuous-integration)
    -   [GitLab CI](#gitlab-ci)

## Conventions

-   replace `projects` with your actual projects directory
-   replace `git_repository_url` with your actual git repository URL

## Initialization

This project uses [uv](https://docs.astral.sh/uv/) for Python and dependency management. `uv sync` will install the locked dependencies and provision the virtual environment automatically.

```shell
$ uv sync --group local --group test
```

Local development tasks are exposed via [just](https://github.com/casey/just) (installed in the `local` dependency group).

## Git

### Git clone

To get the existing project, change the directory, clone the project repository and enter the newly created `{{ cookiecutter.project_slug }}` directory.

### Git hooks

To install [prek](https://github.com/j178/prek) (pre-commit-compatible) into your git hooks run:

```shell
$ just prek_install
```

## Commands

### List available commands

To show the available `just` recipes:

```shell
$ just
```

### List outdated dependencies

To list outdated dependencies tracked by `uv`:

```shell
$ just showoutdated
```

### Upgrade dependencies

To upgrade all dependencies to the latest versions matching `pyproject.toml` constraints (and refresh `uv.lock`):

```shell
$ just upgrade
```

## Testing

To run the full test suite with coverage:

```shell
$ just test
```

To run debugging tests with `pytest` directly (verbose output, no coverage gating):

```shell
$ just pytest
```

Pytest accepts arguments after the recipe name, e.g.:

```shell
$ just pytest path/to/test_module.py::TestClass::test_case
```

## Static files

To collect static files locally:

```shell
$ just collectstatic
```

## Continuous Integration

Depending on the CI tool, you might need to configure Django environment variables.

### GitLab CI

The configuration file `.gitlab-ci.yml` should work as it is, needing no further customization.

### The Kubernetes resource limits

The Kubernetes deployment service limits should be adapted to the expected load of the other services and the size of the available nodes.

By default, the `s-1vcpu-1gb-amd` DigitalOcean droplet is used (https://slugs.do-api.dev/), which allocates 900.00m of CPU capacity and 1.54Gi of memory capacity.

The following default values are calculated assuming 2 deployments and 2 stacks on a single node.

| tfvars name             | default value |
| ----------------------- | ------------- |
| service_limits_cpu      | 550m          |
| service_limits_memory   | 512Mi         |
| service_requests_cpu    | 25m           |
| service_requests_memory | 115Mi         |
