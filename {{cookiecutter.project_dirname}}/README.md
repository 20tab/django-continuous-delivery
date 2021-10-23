# {{ cookiecutter.project_name }}

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

A [Django](https://docs.djangoproject.com) project using [uWSGI](https://uwsgi-docs.readthedocs.io) as application server.

## Index

- [Conventions](#conventions)
- [Initialization](#initialization)
  - [Virtual environment](#virtual-environment)
  - [Requirements](#requirements)
- [Git](#git)
  - [Git clone](#git-clone)
  - [Git hooks](#git-hooks)
- [Libraries](#libraries)
  - [List outdated libraries](#list-outdated-libraries)
  - [Update libraries](#update-libraries)
  - [Install libraries](#install-libraries)
- [Testing](#testing)
- [Static files](#static-files)
- [Continuous Integration](#continuous-integration)
  - [Gitlab CI](#gitlab-ci)

## Conventions

- replace `projects` with your actual projects directory
- replace `git_repository_url` with your actual git repository url

## Initialization

We suggest updating pip to the latest version and using a virtual environment to wrap all your libraries.

### Virtual environment

**IMPORTANT**: Please, create an empty virtual environment, with the right python version, and activate it.
To install and use virtualenv, please, visit the official [Python tutorial](https://docs.python.org/3/tutorial/venv.html)

## Git

### Git clone

To get the existing project, change directory, clone the project repository and enter the newly created **{{ cookiecutter.project_slug }}** directory:

```shell
$ cd ~/projects/
$ git clone GIT_REPOSITORY_URL {{ cookiecutter.project_slug }}
$ cd {{ cookiecutter.project_slug }}
```

**NOTE** : Make sure you switch to the correct branch (e.g. `git checkout develop`)

### Git hooks

To install pre-commit into your git hooks run the below command. pre-commit will now run on every commit. Every time you clone a project using pre-commit running pre-commit install should always be the first thing you do.

```shell
$ pre-commit install
```

## Libraries

### Self documentation of Makefile commands

To show the Makefile self documentation help:

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

To install the just updated requirements (e.g. `requirements/dev.txt`), execute:

```shell
$ make dev
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

The _simpletest_ command accept dashed arguments with a particular syntax, such as:

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

### Gitlab CI

The configuration file `.gitlab-ci.yml` should work as is, needing no further customization.
