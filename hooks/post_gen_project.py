#!/usr/bin/env python
"""Define hooks to be run after project generation."""

import secrets
import shutil
import subprocess
import venv
from pathlib import Path

VENV = ".venv"


def create_env_file():
    """Create env file from the template."""
    env_text = Path(".env_template").read_text()
    env_text = env_text.replace("__SECRETKEY__", secrets.token_urlsafe(40))
    Path(".env").write_text(env_text)
    print("Generated '.env' file.")


def create_venv_directory():
    """Create the venv directory."""
    venv.create(VENV, clear=True, with_pip=True)


def remove_venv_directory():
    """Remove the venv directory."""
    shutil.rmtree(VENV, ignore_errors=True)


def install_requirements():
    """Install requirements in venv directory."""
    subprocess.run([f"{VENV}/bin/pip3", "install", "-q", "black", "pip-tools"])


def format_files():
    """Reformat generated python code."""
    subprocess.run([f"{VENV}/bin/black", "-q", "."])


def generate_requirements():
    """Generate requirements files."""
    requirements_path = Path("requirements")
    PIP_COMPILE = [f"{VENV}/bin/pip-compile", "-q", "-U", "-o"]
    for in_file in requirements_path.glob("*.in"):
        output_file = requirements_path / f"{in_file.stem}.txt"
        subprocess.run(PIP_COMPILE + [output_file, in_file])
        print(f"Generated '/{output_file}' file.")


def create_static_directory():
    """Create the static directory."""
    Path("static").mkdir(exist_ok=True)
    print("Generated '/static' directory.")


def create_media_directory():
    """Create the media directory."""
    Path("media").mkdir(exist_ok=True)
    print("Generated '/media' directory.")


def main():
    """Execute intialization steps after project generation."""
    create_env_file()
    create_venv_directory()
    install_requirements()
    format_files()
    generate_requirements()
    remove_venv_directory()
    create_static_directory()
    if "{{cookiecutter.use_media}}" == "Yes":
        create_media_directory()


if __name__ == "__main__":
    main()
