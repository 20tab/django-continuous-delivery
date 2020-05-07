#!/usr/bin/env python
"""Define hooks to be run before project generation."""

import sys

from slugify import slugify

project_slug = "{{ cookiecutter.project_slug }}"
project_dirname = "{{ cookiecutter.project_dirname }}"


def check_identifiers():
    """Check if project_slug and project_dirname are valid Python identifiers."""
    if not project_slug.isidentifier():
        sys.exit(f"project_slug='{project_slug}' is not a valid Python identifier.")
    if not project_dirname.isidentifier():
        sys.exit(
            f"project_dirname='{project_dirname}' is not a valid Python identifier."
        )


def check_slugs():
    """Check if project_slug and project_dirname are a valid slugs."""
    _project_slug = slugify(project_slug, separator="")
    if project_slug != _project_slug:
        sys.exit(
            f"project_slug='{project_slug}' is not a valid slug (e.g. {_project_slug})."
        )
    _project_dirname = slugify(project_dirname, separator="")
    if project_dirname != _project_dirname:
        sys.exit(
            f"project_dirname='{project_dirname}' is not a valid slug "
            "(e.g. {_project_dirname})."
        )


def main():
    """Execute intialization checks before project generation."""
    check_slugs()
    check_identifiers()


if __name__ == "__main__":
    main()
