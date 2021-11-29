# Django continuous delivery

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

> A [Django](https://docs.djangoproject.com) project cookiecutter ready for continuous delivery.

## 📝 Conventions

In the following instructions:

-   replace `projects` with your actual projects directory
-   replace `My project name` with your chosen project name

## 🧩 Requirements

[Cookiecutter](https://cookiecutter.readthedocs.io) must be installed before initializing the project.

```console
$ python3 -m pip install --user cookiecutter
```

## 🚀️ Quickstart

Change directory and create a new project as in this example:

```console
$ cd ~/projects/
$ cookiecutter https://github.com/20tab/django-continuous-delivery.git
project_name: My project name
project_slug [myprojectname]:
project_dirname [myprojectname]:
domain_url [myprojectname.com]:
gitlab_group_slug [myprojectname]:
Select use_media:
1 - Yes
2 - No
Choose from 1, 2 [1]:
Generated '.env' file.
Generated '/requirements/remote.txt' file.
Generated '/requirements/common.txt' file.
Generated '/requirements/test.txt' file.
Generated '/requirements/base.txt' file.
Generated '/requirements/local.txt' file.
Generated '/static' directory.
Generated '/media' directory.
$ cd myprojectname
```
