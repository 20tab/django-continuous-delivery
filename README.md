# Talos - Django Continuous Delivery

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

> A [Django](https://docs.djangoproject.com) project template ready for continuous delivery.

## 🧩 Requirements

The Talos script can be run either using Docker or as a local shell command.

### 🐋 Docker

In order to run Talos via Docker, a working [Docker installation](https://docs.docker.com/get-docker/) is the only requirement.

### 👨‍💻 Shell command

In order to run Talos as a shell command, first clone the repository in a local projects directory
```console
cd ~/projects
git clone https://github.com/20tab/django-continuous-delivery.git talos-django
```
Then, install the following requirements
| Requirements | Instructions |
|--|--|
|🌎 Terraform  | [Install Guide](https://learn.hashicorp.com/tutorials/terraform/install-cli)  |
|🐍 Python Dependencies | `pip install -r talos-django/requirements/common.txt` |

## 🔑 Credentials

### 🦊 GitLab
If the GitLab integration is enabled, a Personal Access Token with _api_ permission is required.<br/>
It can be generated in the GitLab User Settings panel.

**Note:** the token can be generated in the Access Tokens section of the GitLab User Settings panel.<br/>
⚠️ Beware that the token is shown only once after creation.

## 🚀️ Quickstart

Change to the projects directory, for example
```console
cd ~/projects
```

### 🐋 Docker

```console
docker run --interactive --tty --rm --volume $PWD:/data 20tab/talos-django:latest
```

### 👨‍💻 Shell command

```console
./talos-django/setup.py
```

### Example
```console
Project name: My Project Name
Project slug [my-project-name]:
Service slug [backend]:
Project dirname (backend, myprojectname) [backend]: myprojectname
Development environment complete URL [https://dev.my-project-name.com/]:
Staging environment complete URL [https://stage.my-project-name.com/]:
Production environment complete URL [https://www.my-project-name.com/]:
Media storage (local, s3-digitalocean, none) [s3-digitalocean]:
Do you want to configure Redis? [y/N]: y
Do you want to configure Gitlab? [Y/n]: y
Gitlab group slug [my-project-name]:
Make sure the Gitlab "my-project-name" group exists before proceeding. Continue? [y/N]: y
Gitlab private token (with API scope enabled):
Sentry DSN (leave blank if unused) []:
Initializing the backend service:
...cookiecutting the service
...generating the .env file
...formatting the cookiecut python code
...compiling the requirements files
	- common.txt
	- test.txt
	- local.txt
	- remote.txt
	- base.txt
...creating the '/static' directory
...creating the GitLab repository and associated resources
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

#### Project Domain
If you don't want DigitalOcean DNS configuration the following args are required

`--project-url-dev=https://dev.project-domain.com`<br/>
`--project-url-stage=https://stage.project-domain.com`<br/>
`--project-url-prod=https://www.project-domain.com`

#### Media storage

Value  | Description | Argument
------------- | ------------- | -------------
local  | Docker Volume are used for store media | `--media-storage=local`
s3-digitalocean  | `--media-storage=s3-digitalocean`
none  | Project have no media | `--media-storage=none`

#### Redis
For enable redis integration the following arguments are needed:

`--use-redis`

Disabled args
`--no-redis`

### 🦊 GitLab
> **⚠️ Important:  Make sure the GitLab group exists before create.**
> https://gitlab.com/gitlab-org/gitlab/-/issues/244345

For enable gitlab integration the following arguments are needed:

`--use-gitlab`<br/>
`--gitlab-private-token={{gitlab-private-token}}`<br/>
`--gitlab-group-slug={{gitlab-group-slug}}`

Disabled args
`--no-gitlab`

Add user to repository using comma separeted arguments

`--gitlab-group-owners=user1, user@example.org`<br/>
`--gitlab-group-maintainers=user1, user@example.org`<br/>
`--gitlab-group-developers=user1, user@example.org`

#### 🪖 Sentry
For enable sentry integration the following arguments are needed:

`--sentry-dsn={{frontend-sentry-dsn}}`

#### 🔇 Silent
Is command for use default if no args are provided

`--silent`
