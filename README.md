# Django continuous delivery

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

> A [Django](https://docs.djangoproject.com) project template ready for continuous delivery.

## 📝 Conventions

In the following instructions:

-   replace `projects` with your actual projects directory
-   replace `My project name` with your chosen project name

## Git

To get the existing project, change directory and clone the project repository.

```console
$ cd ~/projects/
$ git clone https://github.com/20tab/django-continuous-delivery.git
```

## 🧩 Requirements

A set of requirements must be installed before initializing the project.

```console
$ python3 -m pip install -r django-continuous-delivery/requirements/common.txt
```

## 🚀️ Quickstart

Change directory and create a new project as in this example:

```console
$ python3 django-continuous-delivery/setup.py
Project name: My project name
Project slug [my-project-name]:
Service slug [backend]:
Project dirname (backend, myprojectname) [backend]: myprojectname
Development environment complete URL [https://dev.my-project-name.com/]:
Staging environment complete URL [https://stage.my-project-name.com/]:
Production environment complete URL [https://www.my-project-name.com/]:
Media storage (local, s3-digitalocean, none) [s3-digitalocean]:
Initializing the backend service:
...cookiecutting the service
...generating the .env file
...formatting the cookiecut python code
...compiling the requirements files
...creating the '/static' directory
Do you want to configure Gitlab? [Y/n]: Y
Gitlab group slug [my-project-name]:
Make sure the Gitlab "my-project-name" group exists before proceeding. Continue? [y/N]: y
Gitlab private token (with API scope enabled):
Sentry DSN (leave blank if unused) []: https://sentry.io/mydsn
...creating the Gitlab repository and associated resources
Project successfully initialized.
$ cd myprojectname
```
