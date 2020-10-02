#!/usr/bin/env python
"""Define hooks to be run after project generation."""

import secrets
import subprocess
import venv
from pathlib import Path

PROJECT_SLUG = "{{cookiecutter.project_slug}}"
VENV = ".venv"


def create_env_file():
    """Create env file from the template."""
    env_text = Path(".env.tpl").read_text()
    env_text = (
        env_text.replace("__NAME__", PROJECT_SLUG)
        .replace("__PASSWORD__", "postgres")
        .replace("__USERNAME__", "postgres")
        .replace("__HOST__", "postgres")
        .replace("__PORT__", "5432")
        .replace("__SECRETKEY__", secrets.token_urlsafe(40))
    )
    Path(".env").write_text(env_text)


def create_venv_directory():
    """Create the venv dirctory."""
    venv.create(VENV, clear=True, with_pip=True)


def install_requirements():
    """Install requirements in venv directory."""
    subprocess.run([f"{VENV}/bin/pip3", "install", "-q", "black", "pip-tools"])


def format_files():
    """Reformat generated python code."""
    subprocess.run([f"{VENV}/bin/black", "-q", "."])


def generate_requirements():
    """Generate requirements files."""
    PIP_COMPILE = [f"{VENV}/bin/pip-compile", "-q", "-U", "-o"]
    subprocess.run(PIP_COMPILE + ["requirements/common.txt", "requirements/common.ini"])
    subprocess.run(PIP_COMPILE + ["requirements/dev.txt", "requirements/dev.ini"])
    subprocess.run(PIP_COMPILE + ["requirements/prod.txt", "requirements/prod.ini"])
    subprocess.run(PIP_COMPILE + ["requirements/tests.txt", "requirements/tests.ini"])


def create_static_directory():
    """Create the static dirctory."""
    Path("static").mkdir(exist_ok=True)


def create_media_directory():
    """Create the media dirctory."""
    Path("media").mkdir(exist_ok=True)


def main():
    """Execute intialization steps after project generation."""
    create_env_file()
    create_venv_directory()
    install_requirements()
    format_files()
    generate_requirements()
    create_static_directory()
    if "{{cookiecutter.use_media_volume}}" == "Yes":
        create_media_directory()


if __name__ == "__main__":
    main()
