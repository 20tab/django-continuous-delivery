#!/usr/bin/env python
"""Boostrap a web project based on templates."""

import os
import shutil
import subprocess
from pathlib import Path

import click
from cookiecutter.main import cookiecutter
from slugify import slugify

GITLAB_TOKEN_ENV_VAR = "GITLAB_PRIVATE_TOKEN"
OUTPUT_BASE_DIR = os.getenv("OUTPUT_BASE_DIR")


def create_env_file(service_dir):
    """Create env file from the template."""
    env_path = Path(service_dir) / Path(".env_template")
    env_template = env_path.read_text()
    env_path.write_text(env_template)


def init_service(
    service_dir,
    project_dirname,
    project_name,
    project_slug,
    service_slug,
    output_dir,
):
    """Initialize the service."""
    if Path(service_dir).is_dir() and click.confirm(
        f'A directory "{service_dir}" already exists and ' "must be deleted. Continue?"
    ):
        shutil.rmtree(service_dir)
    """Initialize the backend service project."""
    cookiecutter(
        ".",
        extra_context={
            "project_dirname": project_dirname,
            "project_name": project_name,
            "project_slug": project_slug,
            "service_slug": service_slug,
        },
        output_dir=output_dir,
        no_input=True,
    )


def init_gitlab(
    gitlab_group_slug,
    gitlab_private_token,
    service_dir,
    project_name,
    project_slug,
):
    """Initialize the Gitlab repositories."""
    env = {
        "TF_VAR_gitlab_group_slug": gitlab_group_slug,
        "TF_VAR_gitlab_token": gitlab_private_token,
        "TF_VAR_service_dir": service_dir,
        "TF_VAR_project_name": project_name,
        "TF_VAR_project_slug": project_slug,
    }
    subprocess.run(
        ["terraform", "init", "-reconfigure", "-input=false"],
        cwd="terraform",
        env=env,
    )
    subprocess.run(
        [
            "terraform",
            "apply",
            "-auto-approve",
            "-input=false",
        ],
        cwd="terraform",
        env=env,
    )


def change_output_owner(service_dir, user_id):
    """Change the owner of the output directory recursively."""
    user_id is not None and subprocess.run(f"chown -R {user_id} {service_dir}")


def slugify_option(ctx, param, value):
    """Slugify an option value."""
    return value and slugify(value)


@click.command()
@click.option("--output-dir", default=".", required=OUTPUT_BASE_DIR is None)
@click.option("--project-name", prompt=True)
@click.option("--project-slug", callback=slugify_option)
@click.option("--service-slug", callback=slugify_option)
@click.option("--project-dirname")
@click.option("--use-gitlab/--no-gitlab", is_flag=True, default=None)
@click.option("--gitlab-private-token", envvar=GITLAB_TOKEN_ENV_VAR)
@click.option("--gitlab-group-slug")
def init_handler(
    output_dir,
    project_name,
    project_slug,
    service_slug,
    project_dirname,
    use_gitlab,
    gitlab_private_token,
    gitlab_group_slug,
):
    """Init the bootstrap handler."""
    project_slug = slugify(
        project_slug or click.prompt("Project slug", default=slugify(project_name)),
    )
    service_slug = slugify(
        service_slug or click.prompt("Service slug", default="django"),
    )
    project_dirname = project_dirname or click.prompt(
        "Project dirname",
        default=service_slug,
        type=click.Choice([service_slug, project_slug]),
    )
    output_dir = OUTPUT_BASE_DIR or output_dir
    service_dir = (Path(output_dir) / Path(project_dirname)).resolve()
    init_service(
        service_dir,
        project_dirname,
        project_name,
        project_slug,
        service_slug,
        output_dir,
    )
    create_env_file(service_dir)
    use_gitlab = (
        use_gitlab
        if use_gitlab is not None
        else click.confirm("Do you want to configure Gitlab?", default=True)
    )
    if use_gitlab:
        gitlab_group_slug = gitlab_group_slug or click.prompt(
            "Gitlab group slug", default=project_slug
        )
        click.confirm(
            f'Make sure the Gitlab "{gitlab_group_slug}" group exists '
            "before proceeding. Continue?",
            abort=True,
        )
        gitlab_private_token = gitlab_private_token or click.prompt(
            "Gitlab private token (with API scope enabled)", hide_input=True
        )
        init_gitlab(
            gitlab_group_slug,
            gitlab_private_token,
            service_dir,
            project_name,
            project_slug,
        )


if __name__ == "__main__":
    init_handler()
