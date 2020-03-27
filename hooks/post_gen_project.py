"""Define hooks to be run after project generation."""

import os
import subprocess


def init():
    """Execute intialization script."""
    subprocess.run("./scripts/init.sh")

def set_media_volumes():
    use_media_volume = "{{ cookiecutter.use_media_volume }}" == "Yes"

    if not use_media_volume:
        os.remove("k8s/development/1_volumes.yaml")
        os.remove("k8s/integration/1_volumes.yaml")
        os.remove("k8s/production/1_volumes.yaml")


init()
set_media_volumes()
