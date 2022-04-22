#!/usr/bin/env python
"""Initialize a web project Django service based on a template."""

import shutil
from functools import partial
from pathlib import Path

import click
import validators
from slugify import slugify

from bootstrap.constants import (
    DEPLOYMENT_TYPE_CHOICES,
    DEPLOYMENT_TYPE_DIGITALOCEAN,
    DEPLOYMENT_TYPE_OTHER,
    ENVIRONMENT_DISTRIBUTION_CHOICES,
    ENVIRONMENT_DISTRIBUTION_DEFAULT,
    ENVIRONMENT_DISTRIBUTION_PROMPT,
    MEDIA_STORAGE_CHOICES,
    MEDIA_STORAGE_DIGITALOCEAN_S3,
    TERRAFORM_BACKEND_CHOICES,
    TERRAFORM_BACKEND_GITLAB,
    TERRAFORM_BACKEND_TFC,
)

error = partial(click.style, fg="red")

warning = partial(click.style, fg="yellow")


def collect(
    uid,
    gid,
    output_dir,
    project_name,
    project_slug,
    project_dirname,
    service_slug,
    internal_service_port,
    deployment_type,
    environment_distribution,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    sentry_dsn,
    terraform_backend,
    media_storage,
    use_redis,
    gitlab_private_token,
    gitlab_group_slug,
    terraform_dir,
    logs_dir,
    quiet,
):
    """Collect options and run the setup."""
    project_slug = clean_project_slug(project_name, project_slug)
    service_slug = clean_service_slug(service_slug)
    project_dirname = clean_project_dirname(project_dirname, project_slug, service_slug)
    deployment_type = clean_deployment_type(deployment_type)
    environment_distribution = clean_environment_distribution(
        environment_distribution, deployment_type
    )
    project_url_dev = validate_or_prompt_url(
        project_url_dev,
        "Development environment complete URL",
        default=f"https://dev.{project_slug}.com/",
    )
    project_url_stage = validate_or_prompt_url(
        project_url_stage,
        "Staging environment complete URL",
        default=f"https://stage.{project_slug}.com/",
    )
    project_url_prod = validate_or_prompt_url(
        project_url_prod,
        "Production environment complete URL",
        default=f"https://www.{project_slug}.com/",
    )
    service_dir = clean_service_dir(output_dir, project_dirname)
    terraform_backend = clean_terraform_backend(terraform_backend)
    media_storage = clean_media_storage(media_storage)
    use_redis = clean_use_redis(use_redis)
    gitlab_group_slug, gitlab_private_token = clean_gitlab_group_data(
        project_slug,
        gitlab_group_slug,
        gitlab_private_token,
        quiet,
    )
    if gitlab_group_slug:
        sentry_dsn = validate_or_prompt_url(
            sentry_dsn, "Sentry DSN (leave blank if unused)", default=""
        )
    return {
        "uid": uid,
        "gid": gid,
        "output_dir": output_dir,
        "project_name": project_name,
        "project_slug": project_slug,
        "project_dirname": project_dirname,
        "service_dir": service_dir,
        "service_slug": service_slug,
        "internal_service_port": internal_service_port,
        "deployment_type": deployment_type,
        "environment_distribution": environment_distribution,
        "project_url_dev": project_url_dev,
        "project_url_stage": project_url_stage,
        "project_url_prod": project_url_prod,
        "terraform_backend": terraform_backend,
        "sentry_dsn": sentry_dsn,
        "media_storage": media_storage,
        "use_redis": use_redis,
        "gitlab_private_token": gitlab_private_token,
        "gitlab_group_slug": gitlab_group_slug,
        "terraform_dir": terraform_dir,
        "logs_dir": logs_dir,
    }


def validate_or_prompt_url(value, message, default=None, required=False):
    """Validate the given URL or prompt until a valid value is provided."""
    if value is not None:
        if not required and value == "" or validators.url(value):
            return value.strip("/")
        else:
            click.echo(error("Please type a valid URL!"))
    new_value = click.prompt(message, default=default)
    return validate_or_prompt_url(new_value, message, default, required)


def validate_or_prompt_password(value, message, default=None, required=False):
    """Validate the given password or prompt until a valid value is provided."""
    if value is not None:
        if not required and value == "" or validators.length(value, min=8):
            return value
        else:
            click.echo(error("Please type at least 8 chars!"))
    new_value = click.prompt(message, default=default, hide_input=True)
    return validate_or_prompt_password(new_value, message, default, required)


def clean_project_slug(project_name, project_slug):
    """Return the project slug."""
    return slugify(
        project_slug or click.prompt("Project slug", default=slugify(project_name))
    )


def clean_service_slug(service_slug):
    """Return the service slug."""
    return slugify(
        service_slug or click.prompt("Service slug", default="backend"),
        separator="",
    )


def clean_project_dirname(project_dirname, project_slug, service_slug):
    """Return the project directory name."""
    project_dirname_choices = [service_slug, slugify(project_slug, separator="")]
    return project_dirname or click.prompt(
        "Project dirname",
        default=project_dirname_choices[0],
        type=click.Choice(project_dirname_choices),
    )


def clean_service_dir(output_dir, project_dirname):
    """Return the service directory."""
    service_dir = str((Path(output_dir) / project_dirname).resolve())
    if Path(service_dir).is_dir() and click.confirm(
        warning(
            f'A directory "{service_dir}" already exists and '
            "must be deleted. Continue?",
        ),
        abort=True,
    ):
        shutil.rmtree(service_dir)
    return service_dir


def clean_terraform_backend(terraform_backend):
    """Return the terraform backend."""
    return (
        terraform_backend
        if terraform_backend in TERRAFORM_BACKEND_CHOICES
        else click.prompt(
            "Terraform backend",
            default=TERRAFORM_BACKEND_TFC,
            type=click.Choice(TERRAFORM_BACKEND_CHOICES, case_sensitive=False),
        )
    ).lower()


def clean_deployment_type(deployment_type):
    """Return the deployment type."""
    return (
        deployment_type
        if deployment_type in DEPLOYMENT_TYPE_CHOICES
        else click.prompt(
            "Deploy type",
            default=DEPLOYMENT_TYPE_DIGITALOCEAN,
            type=click.Choice(DEPLOYMENT_TYPE_CHOICES, case_sensitive=False),
        )
    ).lower()


def clean_environment_distribution(environment_distribution, deployment_type):
    """Return the environment distribution."""
    if deployment_type == DEPLOYMENT_TYPE_OTHER:
        return "1"
    return (
        environment_distribution
        if environment_distribution in ENVIRONMENT_DISTRIBUTION_CHOICES
        else click.prompt(
            ENVIRONMENT_DISTRIBUTION_PROMPT,
            default=ENVIRONMENT_DISTRIBUTION_DEFAULT,
            type=click.Choice(ENVIRONMENT_DISTRIBUTION_CHOICES),
        )
    )


def clean_media_storage(media_storage):
    """Return the media storage."""
    return (
        media_storage
        or click.prompt(
            "Media storage",
            default=MEDIA_STORAGE_DIGITALOCEAN_S3,
            type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
        ).lower()
    )


def clean_use_redis(use_redis):
    """Tell whether Redis should be used."""
    if use_redis is None:
        return click.confirm(warning("Do you want to configure Redis?"), default=False)
    return use_redis


def clean_gitlab_group_data(
    project_slug,
    gitlab_group_slug,
    gitlab_private_token,
    quiet=False,
):
    """Return GitLab group data."""
    if gitlab_group_slug or (
        gitlab_group_slug is None
        and click.confirm(warning("Do you want to use GitLab?"), default=True)
    ):
        gitlab_group_slug = slugify(
            gitlab_group_slug or click.prompt("GitLab group slug", default=project_slug)
        )
        quiet or click.confirm(
            warning(
                f'Make sure the GitLab "{gitlab_group_slug}" group exists '
                "before proceeding. Continue?"
            ),
            abort=True,
        )
        gitlab_private_token = gitlab_private_token or click.prompt(
            "GitLab private token (with API scope enabled)", hide_input=True
        )
    else:
        gitlab_group_slug = ""
        gitlab_private_token = ""
    return (gitlab_group_slug, gitlab_private_token)
