#!/usr/bin/env python
"""Define hooks to be run after project generation."""

from pathlib import Path
from shutil import copyfile


def create_env_file():
    """Create env file from the template."""
    copyfile(Path(".env.tpl"), Path(".env"))


def remove_media_volumes():
    """Remove volumes files in all kubernetes sub-directories."""
    for path in Path("k8s").glob("*/1_volumes.yaml"):
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def main():
    """Execute intialization steps after project generation."""
    create_env_file()
    if "{{cookiecutter.use_media_volume}}" == "No":
        remove_media_volumes()


if __name__ == "__main__":
    main()
