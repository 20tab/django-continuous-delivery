#!/usr/bin/env python
"""Define hooks to be run after project generation."""

from pathlib import Path


def create_env_file():
    """Create env file from the template."""
    Path(".env").write_text(Path(".env.tpl").read_text())


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
