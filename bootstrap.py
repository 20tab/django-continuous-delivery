#!/usr/bin/env python
"""Boostrap a web project based on templates."""

import os
import secrets
import shutil
import subprocess
from pathlib import Path

import click
from cookiecutter.main import cookiecutter
from slugify import slugify

GITLAB_TOKEN_ENV_VAR = "GITLAB_PRIVATE_TOKEN"
MEDIA_STORAGE_CHOICES = ["local", "s3", "none"]
MEDIA_STORAGE_DEFAULT = "s3"
DO_SPACES_REGION_DEFAULT = "fra1"
OUTPUT_BASE_DIR = os.getenv("OUTPUT_BASE_DIR")


def init_service(
    project_dirname,
    project_name,
    project_slug,
    service_slug,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    output_dir,
):
    """Initialize the service."""
    cookiecutter(
        ".",
        extra_context={
            "project_dirname": project_dirname,
            "project_name": project_name,
            "project_slug": project_slug,
            "project_url_dev": project_url_dev,
            "project_url_prod": project_url_prod,
            "project_url_stage": project_url_stage,
            "service_slug": service_slug,
        },
        output_dir=output_dir,
        no_input=True,
    )
    click.echo("...code generated with cookiecutter.")


def create_env_file(service_dir):
    """Create env file from the template."""
    env_path = Path(service_dir) / ".env_template"
    env_text = env_path.read_text().replace("__SECRETKEY__", secrets.token_urlsafe(40))
    env_path.write_text(env_text)
    click.echo("...generated env file.")


def format_files(service_dir):
    """Format python code generated by cookiecutter."""
    subprocess.run(["black", "-q", f"{service_dir}"])
    click.echo("...formatted cookiecutter generated python files.")


def compile_requirements(service_dir):
    """Compile the requirements files."""
    requirements_path = Path(f"{service_dir}/requirements")
    PIP_COMPILE = ["pip-compile", "-q", "-U", "-o"]
    for in_file in requirements_path.glob("*.in"):
        output_filename = f"{in_file.stem}.txt"
        output_file = requirements_path / output_filename
        subprocess.run(PIP_COMPILE + [output_file, in_file])
        click.echo(f"...generated the '{output_filename}' requirements file.")


def create_static_directory(service_dir):
    """Create the static directory."""
    (Path(service_dir) / "static").mkdir(exist_ok=True)
    click.echo("...generated the '/static' directory.")


def create_media_directory(service_dir):
    """Create the media directory."""
    (Path(service_dir) / "media").mkdir(exist_ok=True)
    click.echo("...generated the '/media' directory.")


def init_gitlab(
    gitlab_group_slug,
    gitlab_private_token,
    project_name,
    project_slug,
    service_dir,
    service_slug,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    digitalocean_token,
    sentry_dsn,
    digitalocean_spaces_access_id,
    digitalocean_spaces_bucket_region,
    digitalocean_spaces_secret_key,
    create_group_variables,
):
    """Initialize the Gitlab repositories."""
    env = {
        "TF_VAR_create_group_variables": create_group_variables,
        "TF_VAR_digitalocean_spaces_access_id": digitalocean_spaces_access_id,
        "TF_VAR_digitalocean_spaces_bucket_region": digitalocean_spaces_bucket_region,
        "TF_VAR_digitalocean_spaces_secret_key": digitalocean_spaces_secret_key,
        "TF_VAR_digitalocean_token": digitalocean_token,
        "TF_VAR_gitlab_group_slug": gitlab_group_slug,
        "TF_VAR_gitlab_token": gitlab_private_token,
        "TF_VAR_project_name": project_name,
        "TF_VAR_project_slug": project_slug,
        "TF_VAR_project_url_dev": project_url_dev,
        "TF_VAR_project_url_prod": project_url_prod,
        "TF_VAR_project_url_stage": project_url_stage,
        "TF_VAR_sentry_dsn": sentry_dsn,
        "TF_VAR_service_dir": service_dir,
        "TF_VAR_service_slug": service_slug,
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
@click.option("--project-url-dev")
@click.option("--project-url-stage")
@click.option("--project-url-prod")
@click.option("--digitalocean-token")
@click.option("--sentry-dsn")
@click.option(
    "--media-storage",
    default=MEDIA_STORAGE_DEFAULT,
    type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
)
@click.option("--digitalocean-spaces-access-id")
@click.option("--digitalocean-spaces-bucket-region")
@click.option("--digitalocean-spaces-secret-key")
@click.option("--use-gitlab/--no-gitlab", is_flag=True, default=None)
@click.option("--create-group-variables", is_flag=True, default=None)
@click.option("--gitlab-private-token", envvar=GITLAB_TOKEN_ENV_VAR)
@click.option("--gitlab-group-slug")
def init_handler(
    output_dir,
    project_name,
    project_slug,
    service_slug,
    project_dirname,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    digitalocean_token,
    sentry_dsn,
    media_storage,
    digitalocean_spaces_access_id,
    digitalocean_spaces_bucket_region,
    digitalocean_spaces_secret_key,
    use_gitlab,
    create_group_variables,
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
    project_url_dev = project_url_dev or click.prompt(
        "Development environment complete URL",
        default=f"dev.{project_slug}.com",
        type=str,
    )
    project_url_stage = project_url_stage or click.prompt(
        "Staging environment complete URL",
        default=f"stage.{project_slug}.com",
        type=str,
    )
    project_url_prod = project_url_prod or click.prompt(
        "Production environment complete URL",
        default=f"www.{project_slug}.com",
        type=str,
    )
    digitalocean_token = digitalocean_token or click.prompt(
        "DigitalOcean token", hide_input=True
    )
    sentry_dsn = sentry_dsn or click.prompt(
        "Sentry DSN (leave blank if unused)", hide_input=True, default=""
    )
    output_dir = OUTPUT_BASE_DIR or output_dir
    service_dir = (Path(output_dir) / project_dirname).resolve()
    if Path(service_dir).is_dir() and click.confirm(
        f'A directory "{service_dir}" already exists and ' "must be deleted. Continue?"
    ):
        shutil.rmtree(service_dir)
    click.echo("Processing:")
    init_service(
        service_dir,
        project_dirname,
        project_name,
        project_slug,
        service_slug,
        project_url_dev,
        project_url_stage,
        project_url_prod,
        output_dir,
    )
    create_env_file(service_dir)
    format_files(service_dir)
    compile_requirements(service_dir)
    create_static_directory(service_dir)
    media_storage = (
        media_storage
        or click.prompt(
            "Media storage",
            default=MEDIA_STORAGE_DEFAULT,
            type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
        )
    ).lower()
    if media_storage == "local":
        create_media_directory()
    elif media_storage == "s3":
        digitalocean_spaces_bucket_region = (
            digitalocean_spaces_bucket_region
            or click.prompt(
                "DigitalOcean Spaces region", default=DO_SPACES_REGION_DEFAULT
            )
        )
        digitalocean_spaces_access_id = digitalocean_spaces_access_id or click.prompt(
            "DigitalOcean Spaces Access Key ID", hide_input=True
        )
        digitalocean_spaces_secret_key = digitalocean_spaces_secret_key or click.prompt(
            "DigitalOcean Spaces Secret Access Key", hide_input=True
        )
    use_gitlab = (
        use_gitlab
        if use_gitlab is not None
        else click.confirm(
            click.style("Do you want to configure Gitlab?", fg="yellow"), default=True
        )
    )
    if use_gitlab:
        gitlab_group_slug = gitlab_group_slug or click.prompt(
            "Gitlab group slug", default=project_slug
        )
        click.confirm(
            click.style(
                f'Make sure the Gitlab "{gitlab_group_slug}" group exists '
                "before proceeding. Continue?",
                fg="yellow",
            ),
            abort=True,
        )
        gitlab_private_token = gitlab_private_token or click.prompt(
            "Gitlab private token (with API scope enabled)", hide_input=True
        )
        create_group_variables = (
            create_group_variables
            if create_group_variables is not None
            else click.confirm(
                "Do you want to create Gitlab group variables?", default=False
            )
        )
        init_gitlab(
            gitlab_group_slug,
            gitlab_private_token,
            project_name,
            project_slug,
            service_dir,
            service_slug,
            project_url_dev,
            project_url_stage,
            project_url_prod,
            digitalocean_token,
            sentry_dsn,
            digitalocean_spaces_access_id,
            digitalocean_spaces_bucket_region,
            digitalocean_spaces_secret_key,
            create_group_variables,
        )


if __name__ == "__main__":
    init_handler()
