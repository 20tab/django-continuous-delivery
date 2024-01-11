# {{ cookiecutter.project_name }}

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A [Django](https://docs.djangoproject.com) project using [uvicorn](https://www.uvicorn.org/#running-with-gunicorn) ASGI server.

## Index

-   [Conventions](#conventions)
-   [Initialization](#initialization)
    -   [Virtual environment](#virtual-environment)
    -   [Requirements](#requirements)
-   [Git](#git)
    -   [Git clone](#git-clone)
    -   [Git hooks](#git-hooks)
-   [Libraries](#libraries)
    -   [List outdated libraries](#list-outdated-libraries)
    -   [Update libraries](#update-libraries)
    -   [Install libraries](#install-libraries)
-   [Testing](#testing)
-   [Static files](#static-files)
-   [Continuous Integration](#continuous-integration)
    -   [GitLab CI](#gitlab-ci)

## Conventions

-   replace `projects` with your actual projects directory
-   replace `git_repository_url` with your actual git repository URL

## Initialization

We suggest updating pip to the latest version and using a virtual environment to wrap all your libraries.

### Virtual environment

**IMPORTANT**: Please, create an empty virtual environment, with the right Python version, and activate it.
To install and use a virtual environment, please, visit the official [Python tutorial](https://docs.python.org/3/tutorial/venv.html)

## Git

### Git clone

To get the existing project, change the directory, clone the project repository and enter the newly created `{{ cookiecutter.project_slug }}` directory.

### Git hooks

To install pre-commit into your git hooks run the below command. Pre-commit will now run on every commit. Every time you clone a project using pre-commit, running `pre-commit` install should always be the first thing you do.

```shell
$ make precommit_install
```

## Libraries

### Self-documentation of Makefile commands

To show the Makefile self-documentation help:

```shell
$ make
```

### List outdated libraries

To list all outdated installed libraries:

```shell
$ make outdated
```

### Update libraries

Edit the appropriate requirements file `*.in`, to add/remove pinned libraries or modify their versions.

To update the compiled requirements files (`requirements/*.txt`), execute:

```shell
$ make pip
```

### Install libraries

To install the just updated requirements (e.g. `requirements/local.txt`), execute:

```shell
$ make local
```

## Testing

To run the full test suite, with coverage calculation, execute:

```shell
$ make test
```

To run the full test suite, without coverage calculation, execute:

```shell
$ make simpletest
```

To run a single test suite, without coverage calculation, execute:

```shell
$ make simpletest app.tests.single.Test.to_execute
```

The `simpletest` command accepts dashed arguments with a particular syntax, such as:

```shell
$ make simpletest app.tests.single.Test.to_execute -- --keepdb
```

## Static files

To collect static files, execute:

```shell
$ make collectstatic
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
