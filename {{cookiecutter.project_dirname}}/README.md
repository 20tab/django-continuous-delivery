# {{cookiecutter.project_slug}}

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

This is a [Django](https://docs.djangoproject.com) project using [uWSGI](https://uwsgi-docs.readthedocs.io) as application server.

## Documentation

* [Conventions](#conventions)
* [Workspace initialization](#workspace-initialization)
    * [Virtual environment](#virtual-environment)
    * [Basic requirements](#basic-requirements)
* [Clone and start the existing project](#clone-and-start-the-existing-project)
    * [Clone Project](#clone-project)
    * [Initialization](#initialization)
* [Usage](#usage)
    * [Database reset](#database-reset)
    * [Superuser creation](#superuser-creation)
    * [Add or Update libraries](#add-or-update-libraries)
        * [List outdated libraries](#list-outdated-libraries)
        * [Edit and Compile requirements files](#edit-and-compile-requirements-files)
    * [Install libraries for development](#install-libraries-for-development)
* [Testing](#testing)
* [Static](#static)
* [Continuous Integration](#continuous-integration)
    * [Jenkins](#jenkins)
    * [Gitlab CI](#gitlab-ci)
    * [Bitbucket pipelines](#bitbucket-pipelines)
* [Git pre-commit hooks](#git-pre-commit-hooks)
* [Database](#database)
    * [Create](#create)
    * [Drop](#drop)
    * [Dump](#dump)
* [Deploy](#deploy)
    * [Initialize](#initialize)
    * [Deploy](#deploy)
    * [Restore](#restore)

## Conventions

- replace `projects` with your actual projects directory

## Workspace initialization

We suggest updating pip to the latest version and using a virtual environment to wrap all your libraries.

### Virtual environment

**IMPORTANT**: Please, create an empty virtual environment, with the right python version, and activate it.
To install and use virtualenv, please, visit [the official documentation](https://virtualenv.pypa.io)

### Basic requirements

**Django** and **Invoke** must be installed before initializing the project.

```shell
({{cookiecutter.project_slug}}) $ pip install -U django invoke python-dotenv dj-database-url
```

## Clone and start the existing project

This section explains the steps when you need to clone an existing project.

### Clone Project

Change directory and clone the project repository:

```shell
({{cookiecutter.project_slug}}) $ cd ~/projects/
({{cookiecutter.project_slug}}) $ git clone GIT_REPOSITORY_URL {{cookiecutter.project_slug}}
```

> **NOTE** : If you're cloning an existing project, make sure you go to the correct branch (e.g. `git checkout develop`)

### Initialization

Enter the newly created **project** directory:

```shell
({{cookiecutter.project_slug}}) $ cd ~/projects/{{cookiecutter.project_slug}}
```

Invoke init and follow instructions, to configure the project:

```shell
({{cookiecutter.project_slug}}) $ inv init
```

## Usage

### Database reset

To reset database execute (beware all data will be lost):

```shell
({{cookiecutter.project_slug}}) $ inv dropdb
({{cookiecutter.project_slug}}) $ inv createdb
({{cookiecutter.project_slug}}) $ python manage.py migrate
```

### Superuser creation

Create a user with full privileges (e.g. admin access):

```shell
({{cookiecutter.project_slug}}) $ python manage.py createsuperuser
```

### Add or Update libraries

#### List outdated libraries

To list all outdated installed libraries:

```shell
({{cookiecutter.project_slug}}) $ pip list -o
```

#### Edit and Compile requirements files

Edit the appropriate .ini requirements file, to add/remove pinned libraries or modify their versions.

To update the compiled requirements files (`requirements/*.txt`), execute:

```shell
({{cookiecutter.project_slug}}) $ make pip
```

Alternatively, in order to update specific dependent libraries to the latest version (e.g. urllib3), execute:
￼
```shell
({{cookiecutter.project_slug}}) $ make pip p='-P urllib3'
```

### Install libraries for development

To install the just updated requirements (e.g. `requirements/dev.txt`), execute:

```shell
({{cookiecutter.project_slug}}) $ make dev
```

## Testing

To run the full test suite, with coverage calculation, execute:

```shell
({{cookiecutter.project_slug}}) $ make test
```

> **NOTE**:  check [django-bdd-toolkit](https://github.com/20tab/django-bdd-toolkit) for instructions on how to write BDD tests

## Static

To collect static files, execute:

```shell
({{cookiecutter.project_slug}}) $ make collectstatic
```

## Continuous Integration

Depending on the CI tool, you might need to configure Django environment variables.

### Jenkins

Use the following command as a shortcut to configure the continuous integration.

```shell
pip install tox
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/{{cookiecutter.project_slug}}
export DJANGO_SECRET_KEY=<django_secret_key>
tox -e coverage,reportxml
```

### Gitlab CI

The configuration file `.gitlab-ci.yml` should work as is, needing no further customization.

### Bitbucket pipelines

The configuration file `bitbucket-pipelines.yml` should work as is, needing no further customization.

## Git pre-commit hooks

To install pre-commit into your git hooks run the below command. pre-commit will now run on every commit. Every time you clone a project using pre-commit running pre-commit install should always be the first thing you do.

```shell
({{cookiecutter.project_slug}}) $ pre-commit install
```

## Database

### Create

To create a local database (database settings from `.env`):

```shell
({{cookiecutter.project_slug}}) $ inv createdb
```

### Drop

To drop the local database (database settings from `.env`):

```shell
({{cookiecutter.project_slug}}) $ inv dropdb
```

### Dump

To dump the local database into `deploy/dump.sql.bz2` (database settings from `.env`):

```shell
({{cookiecutter.project_slug}}) $ inv dumpdb
```
