"""Define hooks to be run after project generation."""

import subprocess


def init():
    """Execute intialization script."""
    subprocess.run("./scripts/init.sh")


init()
