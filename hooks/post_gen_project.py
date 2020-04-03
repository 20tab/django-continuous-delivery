"""Define hooks to be run after project generation."""

from pathlib import Path
from shutil import copyfile


def init():
    """Execute intialization steps."""
    copyfile(Path(".env.tpl"), Path(".env"))
    use_media_volume = "{{ cookiecutter.use_media_volume }}" == "Yes"
    if not use_media_volume:
        for f in Path("k8s").glob("*/1_volumes.yaml"):
            try:
                f.unlink()
            except FileNotFoundError:
                pass


init()
