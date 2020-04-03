"""Define hooks to be run after project generation."""

import subprocess
from pathlib import Path


def init():
    """Execute intialization script."""
    subprocess.run("./scripts/init.sh")


def set_media_volumes():
    """Set media volumes if requested."""
    use_media_volume = "{{ cookiecutter.use_media_volume }}" == "Yes"

    if not use_media_volume:
        for f in Path("k8s").glob("*/1_volumes.yaml"):
            try:
                f.unlink()
            except FileNotFoundError:
                pass


init()
set_media_volumes()
