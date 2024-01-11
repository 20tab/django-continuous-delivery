#!/usr/bin/env python
"""Initialize a web project Django service based on a template."""

from pathlib import Path

import click

from bootstrap.collector import Collector
from bootstrap.constants import (
    DEPLOYMENT_TYPE_CHOICES,
    ENVIRONMENTS_DISTRIBUTION_CHOICES,
    GITLAB_TOKEN_ENV_VAR,
    MEDIA_STORAGE_CHOICES,
    VAULT_TOKEN_ENV_VAR,
)
from bootstrap.exceptions import BootstrapError
from bootstrap.helpers import slugify_option


@click.command()
@click.option("--uid", type=int)
@click.option("--gid", type=int)
@click.option(
    "--output-dir",
    default=".",
    envvar="OUTPUT_BASE_DIR",
    type=click.Path(
        exists=True, path_type=Path, file_okay=False, readable=True, writable=True
    ),
)
@click.option("--project-name", prompt=True)
@click.option("--project-slug", callback=slugify_option)
@click.option("--project-dirname")
@click.option("--service-slug", callback=slugify_option)
@click.option("--internal-service-port", default=8000, type=int)
@click.option(
    "--deployment-type",
    type=click.Choice(DEPLOYMENT_TYPE_CHOICES, case_sensitive=False),
)
@click.option("--terraform-backend")
@click.option("--terraform-cloud-hostname")
@click.option("--terraform-cloud-token")
@click.option("--terraform-cloud-organization")
@click.option(
    "--terraform-cloud-organization-create/--terraform-cloud-organization-create-skip",
    is_flag=True,
    default=None,
)
@click.option("--terraform-cloud-admin-email")
@click.option("--vault-token", envvar=VAULT_TOKEN_ENV_VAR)
@click.option("--vault-url")
@click.option(
    "--environments-distribution", type=click.Choice(ENVIRONMENTS_DISTRIBUTION_CHOICES)
)
@click.option("--project-url-dev")
@click.option("--project-url-stage")
@click.option("--project-url-prod")
@click.option("--sentry-dsn")
@click.option("--sentry-org")
@click.option("--sentry-url")
@click.option(
    "--media-storage",
    type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
)
@click.option("--local-s3-storage/--no-local-s3-storage", is_flag=True, default=None)
@click.option("--use-redis/--no-redis", is_flag=True, default=None)
@click.option("--gitlab-url")
@click.option("--gitlab-token", envvar=GITLAB_TOKEN_ENV_VAR)
@click.option("--gitlab-namespace-path")
@click.option("--terraform-dir")
@click.option("--logs-dir")
@click.option("--quiet", is_flag=True)
def main(**options):
    """Run the setup."""
    try:
        collector = Collector(**options)
        collector.collect()
        collector.launch_runner()
    except BootstrapError as e:
        raise click.Abort() from e


if __name__ == "__main__":
    main()
