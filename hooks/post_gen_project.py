#!/usr/bin/env python
"""Define hooks to be run after project generation."""

from pathlib import Path
from shutil import copyfile


def main():
    """Execute intialization steps."""
    copyfile(Path(".env.tpl"), Path(".env"))
    if "{{cookiecutter.use_media_volume}}" == "No":
        for f in Path("k8s").glob("*/1_volumes.yaml"):
            try:
                f.unlink()
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    main()
