#!/usr/bin/env python
"""Initialize a web project Django service based on a template."""

import base64
import os
import secrets
import subprocess
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from time import time

import click
from cookiecutter.main import cookiecutter

from bootstrap.constants import (
    DEPLOYMENT_TYPE_OTHER,
    MEDIA_STORAGE_AWS_S3,
    MEDIA_STORAGE_DIGITALOCEAN_S3,
    TERRAFORM_BACKEND_GITLAB,
    TERRAFORM_BACKEND_TFC,
)
from bootstrap.helpers import format_tfvar

error = partial(click.style, fg="red")

highlight = partial(click.style, fg="cyan")

info = partial(click.style, dim=True)

warning = partial(click.style, fg="yellow")


@dataclass(kw_only=True)
class Runner:
    """The bootstrap runner."""

    uid: int
    gid: int
    output_dir: str
    project_name: str
    project_slug: str
    project_dirname: str
    service_dir: str
    service_slug: str
    internal_service_port: int
    deployment_type: str
    environment_distribution: str
    project_url_dev: str
    project_url_stage: str
    project_url_prod: str
    terraform_backend: str
    terraform_cloud_hostname: str
    terraform_cloud_token: str
    terraform_cloud_organization: str
    terraform_cloud_organization_create: bool
    terraform_cloud_admin_email: str
    sentry_dsn: str
    media_storage: str
    use_redis: str
    gitlab_private_token: str
    gitlab_group_slug: str
    terraform_dir: Path
    logs_dir: Path
    run_id: str = field(init=False)
    stacks_environments: dict = field(init=False, default_factory=dict)
    tfvars: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        """Finalize initialization."""
        self.run_id = f"{time():.0f}"
        self.terraform_dir = self.terraform_dir or Path(f".terraform/{self.run_id}")
        self.logs_dir = self.logs_dir or Path(f".logs/{self.run_id}")
        self.stacks_environments = self.get_stacks_environments()
        self.set_tfvars()

    def get_stacks_environments(self):
        """Return a dict with the environments distribution per stack."""
        dev_env = {
            "name": "Development",
            "url": self.project_url_dev,
        }
        stage_env = {
            "name": "Staging",
            "url": self.project_url_stage,
        }
        prod_env = {
            "name": "Production",
            "url": self.project_url_prod,
        }
        if self.environment_distribution == "1":
            self.stacks_environments = {
                "main": {"dev": dev_env, "stage": stage_env, "prod": prod_env}
            }
        elif self.environment_distribution == "2":
            self.stacks_environments = {
                "dev": {"dev": dev_env, "stage": stage_env},
                "main": {"prod": prod_env},
            }
        elif self.environment_distribution == "3":
            self.stacks_environments = {
                "dev": {"dev": dev_env},
                "stage": {"stage": stage_env},
                "main": {"prod": prod_env},
            }

    def add_tfvar(self, tf_stage, var_name, var_value=None, var_type=None):
        """Add a Terraform value to the given .tfvars file."""
        vars_list = self.tfvars.setdefault(tf_stage, [])
        if var_value is None:
            var_value = getattr(self, var_name)
        vars_list.append("=".join((var_name, format_tfvar(var_value, var_type))))

    def add_tfvars(self, tf_stage, *vars):
        """Add one or more Terraform variables to the given stage."""
        [self.add_tfvar(tf_stage, *((i,) if isinstance(i, str) else i)) for i in vars]

    def add_base_tfvars(self, *vars, stack_slug=None):
        """Add one or more base Terraform variables."""
        tf_stage = "base" + (stack_slug and f"_{stack_slug}" or "")
        self.add_tfvars(tf_stage, *vars)

    def add_cluster_tfvars(self, *vars, stack_slug=None):
        """Add one or more cluster Terraform variables."""
        tf_stage = "cluster" + (stack_slug and f"_{stack_slug}" or "")
        self.add_tfvars(tf_stage, *vars)

    def add_environment_tfvars(self, *vars, env_slug=None):
        """Add one or more environment Terraform variables."""
        tf_stage = "environment" + (env_slug and f"_{env_slug}" or "")
        self.add_tfvars(tf_stage, *vars)

    def set_tfvars(self):
        """Set Terraform variables lists."""
        self.project_domain and self.add_cluster_tfvars("project_domain")
        self.letsencrypt_certificate_email and self.add_cluster_tfvars(
            "letsencrypt_certificate_email",
            ("ssl_enabled", True, "bool"),
        )
        if self.use_redis:
            self.add_base_tfvars(("use_redis", True, "bool"))
            self.add_environment_tfvars(("use_redis", True, "bool"))
        if self.project_url_monitoring:
            self.add_cluster_tfvars(
                ("monitoring_url", self.project_url_monitoring),
            )
            self.domain_prefix_monitoring and self.add_cluster_tfvars(
                ("monitoring_domain_prefix", self.domain_prefix_monitoring),
            )
        if "digitalocean" in self.deployment_type:
            self.project_domain and self.add_cluster_tfvars(
                ("create_domain", self.digitalocean_create_domain, "bool")
            )
            self.add_base_tfvars(
                ("k8s_cluster_region", self.digitalocean_k8s_cluster_region),
                ("database_cluster_region", self.digitalocean_database_cluster_region),
                (
                    "database_cluster_node_size",
                    self.digitalocean_database_cluster_node_size,
                ),
            )
            self.use_redis and self.add_base_tfvars(
                ("redis_cluster_region", self.digitalocean_redis_cluster_region),
                ("redis_cluster_node_size", self.digitalocean_redis_cluster_node_size),
            )
        elif self.deployment_type == DEPLOYMENT_TYPE_OTHER:
            self.add_environment_tfvars(
                "postgres_image",
                "postgres_persistent_volume_capacity",
                "postgres_persistent_volume_claim_capacity",
                "postgres_persistent_volume_host_path",
            )
            self.use_redis and self.add_environment_tfvars("redis_image")
        if self.media_storage == MEDIA_STORAGE_DIGITALOCEAN_S3:
            self.add_base_tfvars(("create_s3_bucket", True, "bool"))
            self.add_environment_tfvars(
                ("digitalocean_spaces_bucket_available", True, "bool")
            )
        for stack_slug, stack_envs in self.stacks_environments.items():
            domain_prefixes = []
            for env_slug, env_data in stack_envs.items():
                self.add_environment_tfvars(
                    ("basic_auth_enabled", env_slug != "prod", "bool"),
                    ("project_url", env_data["url"]),
                    ("stack_slug", stack_slug),
                    env_slug=env_slug,
                )
                if env_prefix := env_data["prefix"]:
                    domain_prefixes.append(env_prefix)
                    self.add_environment_tfvars(
                        ("domain_prefix", env_prefix), env_slug=env_slug
                    )
            domain_prefixes and self.add_cluster_tfvars(
                ("domain_prefixes", domain_prefixes, "list"), stack_slug=stack_slug
            )

    def init_service(self):
        """Initialize the service."""
        click.echo(info("...cookiecutting the service"))
        cookiecutter(
            os.path.dirname(os.path.dirname(__file__)),
            extra_context={
                "deployment_type": self.deployment_type,
                "internal_service_port": self.internal_service_port,
                "media_storage": self.media_storage,
                "project_dirname": self.project_dirname,
                "project_name": self.project_name,
                "project_slug": self.project_slug,
                "project_url_dev": self.project_url_dev,
                "project_url_prod": self.project_url_prod,
                "project_url_stage": self.project_url_stage,
                "service_slug": self.service_slug,
                "terraform_backend": self.terraform_backend,
                "terraform_cloud_organization": self.terraform_cloud_organization,
                "use_redis": f"{self.use_redis}",
            },
            output_dir=self.output_dir,
            no_input=True,
        )

    def create_env_file(self):
        """Create the final env file from its template."""
        click.echo(info("...generating the .env file"))
        env_path = Path(self.service_dir) / ".env_template"
        env_text = (
            env_path.read_text()
            .replace("__SECRETKEY__", secrets.token_urlsafe(40))
            .replace("__PASSWORD__", secrets.token_urlsafe(8))
        )
        (Path(self.service_dir) / ".env").write_text(env_text)

    def format_files(service_dir):
        """Format python code generated by cookiecutter."""
        click.echo(info("...formatting the cookiecut python code"))
        subprocess.run(["black", "-q", f"{service_dir}"])

    def compile_requirements(self):
        """Compile the requirements files."""
        click.echo(info("...compiling the requirements files"))
        requirements_path = Path(self.service_dir) / "requirements"
        PIP_COMPILE = ["pip-compile", "-q", "-U", "-o"]
        for in_file in requirements_path.glob("*.in"):
            output_filename = f"{in_file.stem}.txt"
            output_file = requirements_path / output_filename
            subprocess.run(PIP_COMPILE + [output_file, in_file])
            click.echo(info(f"\t- {output_filename}"))

    def create_static_directory(self):
        """Create the static directory."""
        click.echo(info("...creating the '/static' directory"))
        (Path(self.service_dir) / "static").mkdir(exist_ok=True)

    def create_media_directory(self):
        """Create the media directory."""
        click.echo(info("...creating the '/media' directory"))
        (Path(self.service_dir) / "media").mkdir(exist_ok=True)

    def change_output_owner(self):
        """Change the owner of the output directory recursively."""
        if self.uid:
            subprocess.run(
                [
                    "chown",
                    "-R",
                    ":".join(map(str, filter(None, (self.uid, self.gid)))),
                    self.service_dir,
                ]
            )

    def get_gitlab_variables(self):
        """Return the GitLab group and project variables."""
        gitlab_group_variables = {}
        gitlab_project_variables = {}
        self.sentry_dsn and gitlab_project_variables.update(
            SENTRY_DSN='{value = "%s", masked = true}' % self.sentry_dsn
        )
        if self.terraform_backend == TERRAFORM_BACKEND_TFC:
            gitlab_group_variables.update(
                TFC_TOKEN='{value = "%s", masked = true}' % self.terraform_cloud_token,
            )
        elif self.terraform_backend == TERRAFORM_BACKEND_GITLAB:
            self.service_slug and gitlab_project_variables.update(
                BACKEND_SERVICE_SLUG=f'{{value = "{self.service_slug}"}}'
            )
            gitlab_group_variables = {
                f"STACK_SLUG_{i.upper()}": f'{{value = "{k}"}}'
                for k, v in self.stacks_environments.items()
                for i in v
            }
            self.backend_service_slug and gitlab_project_variables.update(
                BACKEND_SERVICE_PORT=f'{{value = "{self.backend_service_port}"}}'
            )
            self.frontend_service_slug and gitlab_project_variables.update(
                FRONTEND_SERVICE_PORT=f'{{value = "{self.frontend_service_port}"}}'
            )
            self.project_domain and gitlab_group_variables.update(
                DOMAIN='{value = "%s"}' % self.project_domain
            )
            self.backend_service_slug and self.frontend_service_slug and (
                gitlab_group_variables.update(
                    INTERNAL_BACKEND_URL='{value = "http://%s:%s"}'
                    % (self.backend_service_slug, self.backend_service_port)
                )
            )
            self.letsencrypt_certificate_email and gitlab_project_variables.update(
                LETSENCRYPT_CERTIFICATE_EMAIL=(
                    f'{{value = "{self.letsencrypt_certificate_email}"}}'
                ),
                SSL_ENABLED='{{value = "true"}}',
            )

            self.use_redis and gitlab_project_variables.update(
                USE_REDIS='{value = "true"}'
            )
            if self.project_url_monitoring:
                gitlab_project_variables.update(
                    MONITORING_URL='{value = "%s"}' % self.project_url_monitoring,
                    GRAFANA_PASSWORD='{value = "%s", masked = true}'
                    % secrets.token_urlsafe(12),
                )
                self.domain_prefix_monitoring and gitlab_project_variables.update(
                    MONITORING_DOMAIN_PREFIX='{value = "%s"}'
                    % self.domain_prefix_monitoring
                )
            self.digitalocean_token and gitlab_group_variables.update(
                DIGITALOCEAN_TOKEN='{value = "%s", masked = true}'
                % self.digitalocean_token
            )
            if "digitalocean" in self.deployment_type:
                gitlab_project_variables.update(
                    CREATE_DOMAIN='{value = "%s"}'
                    % (self.digitalocean_create_domain and "true" or "false"),
                    DIGITALOCEAN_K8S_CLUSTER_REGION='{value = "%s"}'
                    % self.digitalocean_k8s_cluster_region,
                    DIGITALOCEAN_DATABASE_CLUSTER_REGION='{value = "%s"}'
                    % self.digitalocean_database_cluster_region,
                    DIGITALOCEAN_DATABASE_CLUSTER_NODE_SIZE='{value = "%s"}'
                    % self.digitalocean_database_cluster_node_size,
                )
                self.use_redis and gitlab_project_variables.update(
                    DIGITALOCEAN_REDIS_CLUSTER_REGION='{value = "%s"}'
                    % self.digitalocean_redis_cluster_region,
                    DIGITALOCEAN_REDIS_CLUSTER_NODE_SIZE='{value = "%s"}'
                    % self.digitalocean_redis_cluster_node_size,
                )
            elif self.deployment_type == DEPLOYMENT_TYPE_OTHER:
                gitlab_group_variables.update(
                    KUBERNETES_CLUSTER_CA_CERTIFICATE='{value = "%s", masked = true}'
                    % base64.b64encode(
                        Path(self.kubernetes_cluster_ca_certificate).read_bytes()
                    ).decode(),
                    KUBERNETES_HOST='{value = "%s"}' % self.kubernetes_host,
                    KUBERNETES_TOKEN='{value = "%s", masked = true}'
                    % self.kubernetes_token,
                )
                gitlab_project_variables.update(
                    POSTGRES_IMAGE='{value = "%s"}' % self.postgres_image,
                    POSTGRES_PERSISTENT_VOLUME_CAPACITY='{value = "%s"}'
                    % self.postgres_persistent_volume_capacity,
                    POSTGRES_PERSISTENT_VOLUME_CLAIM_CAPACITY='{value = "%s"}'
                    % self.postgres_persistent_volume_claim_capacity,
                    POSTGRES_PERSISTENT_VOLUME_HOST_PATH='{value = "%s"}'
                    % self.postgres_persistent_volume_host_path,
                )
                self.use_redis and gitlab_project_variables.update(
                    REDIS_IMAGE='{value = "%s"}' % self.redis_image,
                )
            "s3" in self.media_storage and gitlab_group_variables.update(
                S3_ACCESS_ID='{value = "%s", masked = true}' % self.s3_access_id,
                S3_SECRET_KEY='{value = "%s", masked = true}' % self.s3_secret_key,
                S3_REGION='{value = "%s"}' % self.s3_region,
                S3_HOST='{value = "%s"}' % self.s3_host,
            )
            if self.media_storage == MEDIA_STORAGE_DIGITALOCEAN_S3:
                gitlab_group_variables.update(
                    S3_HOST='{value = "%s"}' % self.s3_host,
                )
            elif self.media_storage == MEDIA_STORAGE_AWS_S3:
                gitlab_group_variables.update(
                    S3_BUCKET_NAME='{value = "%s"}' % self.s3_bucket_name,
                )
        return gitlab_group_variables, gitlab_project_variables

    def init_terraform_cloud(self):
        """Initialize Terraform Cloud workspace."""

    def init_gitlab(self):
        """Initialize the GitLab repository and associated resources."""
        click.echo(info("...creating the GitLab repository and associated resources"))
        group_variables, project_variables = self.get_gitlab_variables()
        terraform_dir = self.terraform_dir / self.service_slug
        os.makedirs(terraform_dir, exist_ok=True)
        # TODO check vars
        env = dict(
            PATH=os.environ.get("PATH"),
            TF_DATA_DIR=str((terraform_dir / "data").resolve()),
            TF_LOG="INFO",
            TF_VAR_gitlab_group_variables="{%s}"
            % ", ".join(f"{k} = {v}" for k, v in group_variables.items()),
            TF_VAR_gitlab_group_slug=self.gitlab_group_slug,
            TF_VAR_gitlab_token=self.gitlab_private_token,
            TF_VAR_project_name=self.project_name,
            TF_VAR_project_slug=self.project_slug,
            TF_VAR_gitlab_project_variables="{%s}"
            % ", ".join(f"{k} = {v}" for k, v in project_variables.items()),
            TF_VAR_service_dir=self.service_dir,
            TF_VAR_service_slug=self.service_slug,
        )
        state_path = terraform_dir / "state.tfstate"
        logs_dir = self.logs_dir / self.service_slug / "terraform"
        os.makedirs(logs_dir)
        init_log_path = logs_dir / "init.log"
        init_stdout_path = logs_dir / "init-stdout.log"
        init_stderr_path = logs_dir / "init-stderr.log"
        cwd = Path(__file__).parent.parent / "terraform"
        init_process = subprocess.run(
            [
                "terraform",
                "init",
                "-backend-config",
                f"path={state_path.resolve()}",
                "-input=false",
                "-no-color",
            ],
            capture_output=True,
            cwd=cwd,
            env=dict(**env, TF_LOG_PATH=str(init_log_path.resolve())),
            text=True,
        )
        init_stdout_path.write_text(init_process.stdout)
        if init_process.returncode == 0:
            apply_log_path = logs_dir / "apply.log"
            apply_stdout_path = logs_dir / "apply-stdout.log"
            apply_stderr_path = logs_dir / "apply-stderr.log"
            apply_process = subprocess.run(
                ["terraform", "apply", "-auto-approve", "-input=false", "-no-color"],
                capture_output=True,
                cwd=cwd,
                env=dict(**env, TF_LOG_PATH=str(apply_log_path.resolve())),
                text=True,
            )
            apply_stdout_path.write_text(apply_process.stdout)
            if apply_process.returncode != 0:
                apply_stderr_path.write_text(apply_process.stderr)
                click.echo(
                    error(
                        "Error applying Terraform GitLab configuration "
                        f"(check {apply_stderr_path} and {apply_log_path})"
                    )
                )
                destroy_log_path = logs_dir / "destroy.log"
                destroy_stdout_path = logs_dir / "destroy-stdout.log"
                destroy_stderr_path = logs_dir / "destroy-stderr.log"
                destroy_process = subprocess.run(
                    [
                        "terraform",
                        "destroy",
                        "-auto-approve",
                        "-input=false",
                        "-no-color",
                    ],
                    capture_output=True,
                    cwd=cwd,
                    env=dict(**env, TF_LOG_PATH=str(destroy_log_path.resolve())),
                    text=True,
                )
                destroy_stdout_path.write_text(destroy_process.stdout)
                if destroy_process.returncode != 0:
                    destroy_stderr_path.write_text(destroy_process.stderr)
                    click.echo(
                        error(
                            "Error performing Terraform destroy "
                            f"(check {destroy_stderr_path} and {destroy_log_path})"
                        )
                    )
                raise click.Abort()
        else:
            init_stderr_path.write_text(init_process.stderr)
            click.echo(
                error(
                    "Error performing Terraform init "
                    f"(check {init_stderr_path} and {init_log_path})"
                )
            )
            raise click.Abort()

    def run(self):
        """Run the bootstrap."""
        click.echo(highlight(f"Initializing the {self.service_slug} service:"))
        self.init_service()
        self.create_env_file()
        self.format_files()
        self.compile_requirements()
        self.create_static_directory()
        self.media_storage == "local" and self.create_media_directory()
        if self.gitlab_group_slug:
            self.init_gitlab()
        if self.terraform_backend == TERRAFORM_BACKEND_TFC:
            self.init_terraform_cloud()
        self.change_output_owner()
