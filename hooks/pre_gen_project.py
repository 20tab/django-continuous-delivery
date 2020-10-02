#!/usr/bin/env python
"""Define hooks to be run before project generation."""

import sys

from slugify import slugify

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PROJECT_DIRNAME = "{{ cookiecutter.project_dirname }}"


def check_identifiers():
    """Check if project_slug and project_dirname are valid Python identifiers."""
    if not PROJECT_SLUG.isidentifier():
        sys.exit(f"project_slug='{PROJECT_SLUG}' is not a valid Python identifier.")
    if not PROJECT_DIRNAME.isidentifier():
        sys.exit(
            f"project_dirname='{PROJECT_DIRNAME}' is not a valid Python identifier."
        )


def check_slugs():
    """Check if project_slug and project_dirname are a valid slugs."""
    _project_slug = slugify(PROJECT_SLUG, separator="")
    if PROJECT_SLUG != _project_slug:
        sys.exit(
            f"project_slug='{PROJECT_SLUG}' is not a valid slug (e.g. {_project_slug})."
        )
    _project_dirname = slugify(PROJECT_DIRNAME, separator="")
    if PROJECT_DIRNAME != _project_dirname:
        sys.exit(
            f"project_dirname='{PROJECT_DIRNAME}' is not a valid slug "
            "(e.g. {_project_dirname})."
        )


def main():
    """Execute intialization checks before project generation."""
    check_slugs()
    check_identifiers()


if __name__ == "__main__":
    main()
