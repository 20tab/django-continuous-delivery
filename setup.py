#!/usr/bin/env python
"""Initialize a web project Django service based on a template."""

import os

import click

from bootstrap.collector import collect
from bootstrap.constants import GITLAB_TOKEN_ENV_VAR, MEDIA_STORAGE_CHOICES
from bootstrap.exceptions import BootstrapError
from bootstrap.helpers import slugify_option
from bootstrap.runner import run

OUTPUT_DIR = os.getenv("OUTPUT_BASE_DIR") or "."


@click.command()
@click.option("--uid", type=int)
@click.option("--gid", type=int)
@click.option("--output-dir", default=OUTPUT_DIR)
@click.option("--project-name", prompt=True)
@click.option("--project-slug", callback=slugify_option)
@click.option("--project-dirname")
@click.option("--service-slug", callback=slugify_option)
@click.option("--internal-service-port", default=8000, type=int)
@click.option("--project-url-dev")
@click.option("--project-url-stage")
@click.option("--project-url-prod")
@click.option("--sentry-dsn")
@click.option(
    "--media-storage",
    type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
)
@click.option("--use-redis/--no-redis", is_flag=True, default=None)
@click.option("--gitlab-private-token", envvar=GITLAB_TOKEN_ENV_VAR)
@click.option("--gitlab-group-slug")
@click.option("--terraform-dir")
@click.option("--logs-dir")
@click.option("--quiet", is_flag=True)
def main(**options):
    """Run the setup."""
    try:
        run(**collect(**options))
    except BootstrapError as e:
        raise click.Abort() from e


if __name__ == "__main__":
    main()
