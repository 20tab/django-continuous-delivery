#!/usr/bin/env python
"""Define hooks to be run after project generation."""

import sys
from pathlib import Path
from shutil import copyfile


def create_env_file():
    """Create env file from the template."""
    env_file = Path(".env")
    env_template = Path(".env.tpl")
    try:
        copyfile(env_template, env_file)
    except FileNotFoundError:
        sys.exit(f"File {env_template} not found.")


def remove_media_volumes():
    """Remove volumes files in all kubernetes sub-directories."""
    for path in Path("k8s").glob("*/1_volumes.yaml"):
        try:
            path.unlink()
        except FileNotFoundError:
            sys.exit(f"File '{path}' not found.")


def main():
    """Execute intialization steps after project generation."""
    create_env_file()
    if "{{cookiecutter.use_media_volume}}" == "No":
        remove_media_volumes()


if __name__ == "__main__":
    main()
