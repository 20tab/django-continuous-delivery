#!/usr/bin/env python
"""Initialize a web project Django service based on a template."""

from dataclasses import dataclass
from pathlib import Path
from shutil import rmtree

from bootstrap.runner import Runner
import click
from pydantic import validate_arguments
from slugify import slugify

from bootstrap.constants import (
    DEPLOYMENT_TYPE_CHOICES,
    DEPLOYMENT_TYPE_DIGITALOCEAN,
    DEPLOYMENT_TYPE_OTHER,
    ENVIRONMENTS_DISTRIBUTION_CHOICES,
    ENVIRONMENTS_DISTRIBUTION_DEFAULT,
    ENVIRONMENTS_DISTRIBUTION_PROMPT,
    GITLAB_URL_DEFAULT,
    MEDIA_STORAGE_CHOICES,
    MEDIA_STORAGE_DIGITALOCEAN_S3,
    TERRAFORM_BACKEND_CHOICES,
    TERRAFORM_BACKEND_TFC,
)
from bootstrap.helpers import (
    validate_or_prompt_domain,
    validate_or_prompt_email,
    validate_or_prompt_path,
    validate_or_prompt_secret,
    validate_or_prompt_url,
    warning,
)


@validate_arguments
@dataclass(kw_only=True)
class Collector:
    """The bootstrap CLI options collector."""

    output_dir: Path = Path(".")
    project_name: str | None = None
    project_slug: str | None = None
    project_dirname: str | None = None
    service_slug: str | None = None
    internal_service_port: int | None = None
    deployment_type: str | None = None
    terraform_backend: str | None = None
    terraform_cloud_hostname: str | None = None
    terraform_cloud_token: str | None = None
    terraform_cloud_organization: str | None = None
    terraform_cloud_organization_create: bool | None = None
    terraform_cloud_admin_email: str | None = None
    vault_token: str | None = None
    vault_url: str | None = None
    environments_distribution: str | None = None
    project_url_dev: str | None = None
    project_url_stage: str | None = None
    project_url_prod: str | None = None
    use_redis: bool | None = None
    sentry_dsn: str | None = None
    sentry_org: str | None = None
    sentry_url: str | None = None
    media_storage: str | None = None
    gitlab_url: str | None = None
    gitlab_token: str | None = None
    gitlab_namespace_path: str | None = None
    uid: int | None = None
    gid: int | None = None
    terraform_dir: Path | None = None
    logs_dir: Path | None = None
    quiet: bool = False

    def __post_init__(self):
        """Finalize initialization."""
        self._service_dir = None

    def collect(self):
        """Collect options."""
        self.set_project_slug()
        self.set_service_slug()
        self.set_project_dirname()
        self.set_service_dir()
        self.set_use_redis()
        self.set_terraform()
        self.set_vault()
        self.set_deployment_type()
        self.set_environments_distribution()
        self.set_project_urls()
        self.set_sentry()
        self.set_gitlab()
        self.set_media_storage()

    def set_project_slug(self):
        """Set the project slug option."""
        self.project_slug = slugify(
            self.project_slug
            or click.prompt("Project slug", default=slugify(self.project_name))
        )

    def set_service_slug(self):
        """Set the service slug option."""
        self.service_slug = slugify(
            self.service_slug or click.prompt("Service slug", default="backend")
        )

    def set_project_dirname(self):
        """Set the project dirname option."""
        self.project_dirname = self.project_dirname or click.prompt(
            "Project dirname",
            default=self.service_slug,
            type=click.Choice(
                [self.service_slug, slugify(self.project_slug, separator="")]
            ),
        )

    def set_service_dir(self):
        """Set the service dir option."""
        service_dir = self.output_dir / self.project_dirname
        if service_dir.is_dir() and click.confirm(
            warning(
                f'A directory "{service_dir.resolve()}" already exists and '
                "must be deleted. Continue?",
            ),
            abort=True,
        ):
            rmtree(service_dir)
        self._service_dir = service_dir

    def set_use_redis(self):
        """Set the use Redis option."""
        if self.use_redis is None:
            self.use_redis = click.confirm(
                warning("Do you want to use Redis?"), default=False
            )

    def set_terraform(self):
        """Set the Terraform options."""
        if self.terraform_backend not in TERRAFORM_BACKEND_CHOICES:
            self.terraform_backend = click.prompt(
                "Terraform backend",
                default=TERRAFORM_BACKEND_TFC,
                type=click.Choice(TERRAFORM_BACKEND_CHOICES, case_sensitive=False),
            ).lower()
        if self.terraform_backend == TERRAFORM_BACKEND_TFC:
            self.set_terraform_cloud()

    def set_terraform_cloud(self):
        """Set the Terraform Cloud options."""
        self.terraform_cloud_hostname = validate_or_prompt_domain(
            "Terraform host name",
            self.terraform_cloud_hostname,
            default="app.terraform.io",
        )
        self.terraform_cloud_token = validate_or_prompt_secret(
            "Terraform Cloud User token", self.terraform_cloud_token
        )
        self.terraform_cloud_organization = (
            self.terraform_cloud_organization or click.prompt("Terraform Organization")
        )
        if self.terraform_cloud_organization_create is None:
            self.terraform_cloud_organization_create = click.confirm(
                "Do you want to create Terraform Cloud Organization "
                f"'{self.terraform_cloud_organization}'?",
            )
        if self.terraform_cloud_organization_create:
            self.terraform_cloud_admin_email = validate_or_prompt_email(
                "Terraform Cloud Organization admin email (e.g. tech@20tab.com)",
                self.terraform_cloud_admin_email,
            )
        else:
            self.terraform_cloud_admin_email = ""

    def set_vault(self):
        """Set the Vault options."""
        if self.vault_url or (
            self.vault_url is None
            and click.confirm("Do you want to use Vault for secrets management?")
        ):
            self.vault_token = validate_or_prompt_secret(
                "Vault token "
                "(leave blank to perform a browser-based OIDC authentication)",
                self.vault_token,
                default="",
                required=False,
            )
            self.quiet or click.confirm(
                warning(
                    "Make sure your Vault permissions allow to enable the "
                    "project secrets backends and manage the project secrets. Continue?"
                ),
                abort=True,
            )
            self.vault_url = validate_or_prompt_url("Vault address", self.vault_url)

    def set_deployment_type(self):
        """Set the deployment type option."""
        if self.deployment_type not in DEPLOYMENT_TYPE_CHOICES:
            self.deployment_type = click.prompt(
                "Deploy type",
                default=DEPLOYMENT_TYPE_DIGITALOCEAN,
                type=click.Choice(DEPLOYMENT_TYPE_CHOICES, case_sensitive=False),
            ).lower()

    def set_environments_distribution(self):
        """Set the environments distribution option."""
        # TODO: forcing a single stack when deployment is `k8s-other` should be removed,
        #       and `set_deployment_type` merged with `set_deployment`
        if self.deployment_type == DEPLOYMENT_TYPE_OTHER:
            self.environments_distribution = "1"
        elif self.environments_distribution not in ENVIRONMENTS_DISTRIBUTION_CHOICES:
            self.environments_distribution = click.prompt(
                ENVIRONMENTS_DISTRIBUTION_PROMPT,
                default=ENVIRONMENTS_DISTRIBUTION_DEFAULT,
                type=click.Choice(ENVIRONMENTS_DISTRIBUTION_CHOICES),
            )

    def set_project_urls(self):
        """Set the project urls options."""
        self.project_url_dev = validate_or_prompt_url(
            "Development environment complete URL",
            self.project_url_dev or None,
            default=f"https://dev.{self.project_slug}.com",
        )
        self.project_url_stage = validate_or_prompt_url(
            "Staging environment complete URL",
            self.project_url_stage or None,
            default=f"https://stage.{self.project_slug}.com",
        )
        self.project_url_prod = validate_or_prompt_url(
            "Production environment complete URL",
            self.project_url_prod or None,
            default=f"https://www.{self.project_slug}.com",
        )

    def set_sentry(self):
        """Set the Sentry options."""
        if self.sentry_org or (
            self.sentry_org is None
            and click.confirm(warning("Do you want to use Sentry?"), default=False)
        ):
            self.sentry_org = self.sentry_org or click.prompt("Sentry organization")
            self.sentry_url = validate_or_prompt_url(
                "Sentry URL", self.sentry_url, default="https://sentry.io/"
            )
            self.sentry_dsn = validate_or_prompt_url(
                "Sentry DSN (leave blank if unused)",
                self.sentry_dsn,
                default="",
                required=False,
            )

    def set_gitlab(self):
        """Set the GitLab options."""
        if self.gitlab_url or (
            self.gitlab_url is None
            and click.confirm(warning("Do you want to use GitLab?"), default=True)
        ):
            self.gitlab_url = validate_or_prompt_url(
                "GitLab URL", self.gitlab_url, default=GITLAB_URL_DEFAULT
            )
            self.gitlab_token = self.gitlab_token or click.prompt(
                "GitLab access token (with API scope enabled)", hide_input=True
            )
            # TODO: extend support for root level projects (empty namespace)
            self.gitlab_namespace_path = validate_or_prompt_path(
                "GitLab parent group path", self.gitlab_namespace_path
            )
            self.quiet or (
                self.gitlab_namespace_path == ""
                and self.gitlab_url == GITLAB_URL_DEFAULT
                and click.confirm(
                    warning(
                        f'Make sure the GitLab "{self.gitlab_namespace_path}" group '
                        "exists before proceeding. Continue?"
                    ),
                    abort=True,
                )
            )

    def set_media_storage(self):
        """Set the media storage options."""
        if self.media_storage is None:
            self.media_storage = click.prompt(
                "Media storage",
                default=MEDIA_STORAGE_DIGITALOCEAN_S3,
                type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
            ).lower()

    def get_runner(self):
        """Get the bootstrap runner instance."""
        return Runner(
            uid=self.uid,
            gid=self.gid,
            output_dir=self.output_dir,
            project_name=self.project_name,
            project_slug=self.project_slug,
            project_dirname=self.project_dirname,
            service_dir=self._service_dir,
            service_slug=self.service_slug,
            internal_service_port=self.internal_service_port,
            deployment_type=self.deployment_type,
            terraform_backend=self.terraform_backend,
            terraform_cloud_hostname=self.terraform_cloud_hostname,
            terraform_cloud_token=self.terraform_cloud_token,
            terraform_cloud_organization=self.terraform_cloud_organization,
            terraform_cloud_organization_create=self.terraform_cloud_organization_create,
            terraform_cloud_admin_email=self.terraform_cloud_admin_email,
            vault_token=self.vault_token,
            vault_url=self.vault_url,
            environments_distribution=self.environments_distribution,
            project_url_dev=self.project_url_dev,
            project_url_stage=self.project_url_stage,
            project_url_prod=self.project_url_prod,
            sentry_dsn=self.sentry_dsn,
            sentry_org=self.sentry_org,
            sentry_url=self.sentry_url,
            media_storage=self.media_storage,
            use_redis=self.use_redis,
            gitlab_url=self.gitlab_url,
            gitlab_token=self.gitlab_token,
            gitlab_namespace_path=self.gitlab_namespace_path,
            terraform_dir=self.terraform_dir,
            logs_dir=self.logs_dir,
        )

    def launch_runner(self):
        """Launch a bootstrap runner with the collected options."""
        self.get_runner().run()
