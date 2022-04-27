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
from pydantic import validate_arguments

from bootstrap.constants import (
    DEPLOYMENT_TYPE_OTHER,
    MEDIA_STORAGE_AWS_S3,
    MEDIA_STORAGE_DIGITALOCEAN_S3,
    TERRAFORM_BACKEND_GITLAB,
    TERRAFORM_BACKEND_TFC,
)
from bootstrap.exceptions import BootstrapError
from bootstrap.helpers import format_tfvar

error = partial(click.style, fg="red")

highlight = partial(click.style, fg="cyan")

info = partial(click.style, dim=True)

warning = partial(click.style, fg="yellow")


@dataclass(kw_only=True)
@validate_arguments
class Runner:
    """The bootstrap runner."""

    uid: int
    gid: int
    output_dir: Path
    project_name: str
    project_slug: str
    project_dirname: str
    service_dir: Path
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
    use_redis: bool
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
        self.set_stacks_environments()
        self.set_tfvars()

    def set_stacks_environments(self):
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

    def add_environment_tfvars(self, *vars, env_slug=None):
        """Add one or more environment Terraform variables."""
        tf_stage = "environment" + (env_slug and f"_{env_slug}" or "")
        self.add_tfvars(tf_stage, *vars)

    def set_tfvars(self):
        """Set Terraform variables lists."""
        self.add_environment_tfvars(("media_storage", self.media_storage))
        self.add_environment_tfvars(("use_redis", self.use_redis, "bool"))
        for stack_slug, stack_envs in self.stacks_environments.items():
            for env_slug, env_data in stack_envs.items():
                self.add_environment_tfvars(
                    ("project_url", env_data["url"]),
                    ("stack_slug", stack_slug),
                    env_slug=env_slug,
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
                "use_redis": self.use_redis,
            },
            output_dir=self.output_dir,
            no_input=True,
        )

    def create_env_file(self):
        """Create the final env file from its template."""
        click.echo(info("...generating the .env file"))
        env_path = self.service_dir / ".env_template"
        env_text = (
            env_path.read_text()
            .replace("__SECRETKEY__", secrets.token_urlsafe(40))
            .replace("__PASSWORD__", secrets.token_urlsafe(8))
        )
        (self.service_dir / ".env").write_text(env_text)

    def format_files(self):
        """Format python code generated by cookiecutter."""
        click.echo(info("...formatting the cookiecut python code"))
        subprocess.run(["black", "-q", f"{self.service_dir.resolve()}"])

    def compile_requirements(self):
        """Compile the requirements files."""
        click.echo(info("...compiling the requirements files"))
        requirements_path = self.service_dir / "requirements"
        PIP_COMPILE = ["pip-compile", "-q", "-U", "-o"]
        for in_file in requirements_path.glob("*.in"):
            output_filename = f"{in_file.stem}.txt"
            output_file = requirements_path / output_filename
            subprocess.run(PIP_COMPILE + [output_file, in_file])
            click.echo(info(f"\t- {output_filename}"))

    def create_static_directory(self):
        """Create the static directory."""
        click.echo(info("...creating the '/static' directory"))
        (self.service_dir / "static").mkdir(exist_ok=True)

    def create_media_directory(self):
        """Create the media directory."""
        click.echo(info("...creating the '/media' directory"))
        (self.service_dir / "media").mkdir(exist_ok=True)

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
        return gitlab_group_variables, gitlab_project_variables

    def init_terraform_cloud(self):
        """Initialize the Terraform Cloud resources."""
        click.echo(info("...creating the Terraform Cloud resources"))
        env = dict(
            TF_VAR_admin_email=self.terraform_cloud_admin_email,
            TF_VAR_create_organization=self.terraform_cloud_organization_create
            and "true"
            or "false",
            TF_VAR_hostname=self.terraform_cloud_hostname,
            TF_VAR_organization_name=self.terraform_cloud_organization,
            TF_VAR_project_name=self.project_name,
            TF_VAR_project_slug=self.project_slug,
            TF_VAR_service_slug=self.service_slug,
            TF_VAR_stacks="[]",
            TF_VAR_terraform_cloud_token=self.terraform_cloud_token,
        )
        self.run_terraform("terraform-cloud", env)

    def init_gitlab(self):
        """Initialize the GitLab resources."""
        click.echo(info("...creating the GitLab resources"))
        group_variables, project_variables = self.get_gitlab_variables()
        env = dict(
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
        self.run_terraform("gitlab", env)

    def run_terraform(self, module_name, env):
        """Initialize the Terraform controlled resources."""
        cwd = Path(__file__).parent.parent / "terraform" / module_name
        terraform_dir = self.terraform_dir / self.service_slug / module_name
        os.makedirs(terraform_dir, exist_ok=True)
        env.update(
            PATH=os.environ.get("PATH"),
            TF_DATA_DIR=str((terraform_dir / "data").resolve()),
            TF_LOG="INFO",
        )
        state_path = terraform_dir / "state.tfstate"
        logs_dir = self.logs_dir / self.service_slug / "terraform" / module_name
        os.makedirs(logs_dir)
        init_log_path = logs_dir / "init.log"
        init_stdout_path = logs_dir / "init-stdout.log"
        init_stderr_path = logs_dir / "init-stderr.log"
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
                        f"Error applying {module_name} Terraform configuration "
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
                            f"Error performing {module_name} Terraform destroy "
                            f"(check {destroy_stderr_path} and {destroy_log_path})"
                        )
                    )
                raise BootstrapError
        else:
            init_stderr_path.write_text(init_process.stderr)
            click.echo(
                error(
                    f"Error performing {module_name} Terraform init "
                    f"(check {init_stderr_path} and {init_log_path})"
                )
            )
            raise BootstrapError

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
