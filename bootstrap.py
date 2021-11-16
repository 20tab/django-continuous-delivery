#!/usr/bin/env python
"""Initialize a web project Django service based on a template."""

import os
import secrets
import shutil
import subprocess
from functools import partial
from pathlib import Path
from time import time

import click
import validators
from cookiecutter.main import cookiecutter
from slugify import slugify

GITLAB_TOKEN_ENV_VAR = "GITLAB_PRIVATE_TOKEN"
MEDIA_STORAGE_CHOICES = ["local", "s3-digitalocean", "none"]
MEDIA_STORAGE_DEFAULT = "s3-digitalocean"
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

error = partial(click.style, fg="red")
highlight = partial(click.style, fg="cyan")
info = partial(click.style, dim=True)
warning = partial(click.style, fg="yellow")


def init_service(
    output_dir,
    project_name,
    project_slug,
    project_dirname,
    service_slug,
    internal_service_port,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    media_storage,
):
    """Initialize the service."""
    click.echo(info(info("...cookiecutting the service")))
    cookiecutter(
        ".",
        extra_context={
            "internal_service_port": internal_service_port,
            "media_storage": media_storage,
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


def create_env_file(service_dir):
    """Create env file from the template."""
    click.echo(info("...generating the .env file"))
    env_path = Path(service_dir) / ".env_template"
    env_text = env_path.read_text().replace("__SECRETKEY__", secrets.token_urlsafe(40))
    (Path(service_dir) / ".env").write_text(env_text)


def format_files(service_dir):
    """Format python code generated by cookiecutter."""
    click.echo(info("...formatting the cookiecut python code"))
    subprocess.run(["black", "-q", f"{service_dir}"])


def compile_requirements(service_dir):
    """Compile the requirements files."""
    click.echo(info("...compiling the requirements files"))
    requirements_path = Path(service_dir) / "requirements"
    PIP_COMPILE = ["pip-compile", "-q", "-U", "-o"]
    for in_file in requirements_path.glob("*.in"):
        output_filename = f"{in_file.stem}.txt"
        output_file = requirements_path / output_filename
        subprocess.run(PIP_COMPILE + [output_file, in_file])
        click.echo(info(f"\t- {output_filename}"))


def create_static_directory(service_dir):
    """Create the static directory."""
    click.echo(info("...creating the '/static' directory"))
    (Path(service_dir) / "static").mkdir(exist_ok=True)


def create_media_directory(service_dir):
    """Create the media directory."""
    click.echo(info("...creating the '/media' directory"))
    (Path(service_dir) / "media").mkdir(exist_ok=True)


def init_gitlab(
    gitlab_group_slug,
    gitlab_private_token,
    project_name,
    project_slug,
    service_slug,
    service_dir,
    gitlab_project_variables,
    gitlab_group_variables,
    terraform_dir,
    logs_dir,
):
    """Initialize the Gitlab repository and associated resources."""
    click.echo(info("...creating the Gitlab repository and associated resources"))
    terraform_dir = Path(terraform_dir) / service_slug
    os.makedirs(terraform_dir)
    env = dict(
        TF_DATA_DIR=(Path(terraform_dir) / "data").resolve(),
        TF_LOG="INFO",
        TF_VAR_gitlab_group_variables="{%s}"
        % ", ".join(f"{k} = {v}" for k, v in gitlab_group_variables.items()),
        TF_VAR_gitlab_group_slug=gitlab_group_slug,
        TF_VAR_gitlab_token=gitlab_private_token,
        TF_VAR_project_name=project_name,
        TF_VAR_project_slug=project_slug,
        TF_VAR_gitlab_project_variables="{%s}"
        % ", ".join(f"{k} = {v}" for k, v in gitlab_project_variables.items()),
        TF_VAR_service_dir=service_dir,
        TF_VAR_service_slug=service_slug,
    )
    state_path = Path(terraform_dir) / "state.tfstate"
    cwd = Path("terraform")
    logs_dir = Path(logs_dir) / service_slug / "terraform"
    os.makedirs(logs_dir)
    init_log_path = logs_dir / "init.log"
    init_output_path = logs_dir / "init-output.log"
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
        env=dict(**env, TF_LOG_PATH=init_log_path.resolve()),
        text=True,
    )
    init_output_path.write_text(init_process.stdout)
    if init_process.returncode == 0:
        apply_log_path = logs_dir / "apply.log"
        apply_output_path = logs_dir / "apply-output.log"
        apply_process = subprocess.run(
            ["terraform", "apply", "-auto-approve", "-input=false", "-no-color"],
            capture_output=True,
            cwd=cwd,
            env=dict(**env, TF_LOG_PATH=apply_log_path.resolve()),
            text=True,
        )
        if apply_process.returncode != 0:
            click.echo(
                error(
                    "Error applying Terraform Gitlab configuration "
                    f"(check {apply_output_path} and {apply_log_path})"
                )
            )
            destroy_log_path = logs_dir / "destroy.log"
            destroy_output_path = logs_dir / "destroy.log"
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
                env=dict(**env, TF_LOG_PATH=destroy_log_path.resolve()),
                text=True,
            )
            destroy_output_path.write_text(destroy_process.stdout)
            destroy_process.returncode != 0 and click.echo(
                error(
                    "Error performing Terraform destroy "
                    f"(check {destroy_output_path} and {destroy_log_path})"
                )
            )
            raise click.Abort()
    else:
        click.echo(
            error(
                "Error performing Terraform init "
                f"(check {init_output_path} and {init_log_path})"
            )
        )
        raise click.Abort()


def change_output_owner(service_dir, uid):
    """Change the owner of the output directory recursively."""
    uid is not None and subprocess.run(["chown", "-R", uid, service_dir])


def run(
    uid,
    output_dir,
    project_name,
    project_slug,
    project_dirname,
    service_slug,
    internal_service_port,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    sentry_dsn=None,
    media_storage=None,
    use_gitlab=None,
    gitlab_private_token=None,
    gitlab_group_slug=None,
    terraform_dir=None,
    logs_dir=None,
):
    """Run the bootstrap."""
    service_dir = str((Path(output_dir) / project_dirname).resolve())
    if Path(service_dir).is_dir() and click.confirm(
        warning(
            f'A directory "{service_dir}" already exists and '
            "must be deleted. Continue?",
        ),
        abort=True,
    ):
        shutil.rmtree(service_dir)
    media_storage = (
        media_storage in MEDIA_STORAGE_CHOICES
        and media_storage
        or click.prompt(
            "Media storage",
            default=MEDIA_STORAGE_DEFAULT,
            type=click.Choice(MEDIA_STORAGE_CHOICES, case_sensitive=False),
        )
    ).lower()
    run_id = f"{time():.0f}"
    terraform_dir = terraform_dir or Path(f".terraform/{run_id}").resolve()
    logs_dir = logs_dir or Path(f".logs/{run_id}").resolve()
    click.echo(highlight(f"Initializing the {service_slug} service:"))
    init_service(
        output_dir,
        project_name,
        project_slug,
        project_dirname,
        service_slug,
        internal_service_port,
        project_url_dev,
        project_url_stage,
        project_url_prod,
        media_storage,
    )
    create_env_file(service_dir)
    format_files(service_dir)
    compile_requirements(service_dir)
    create_static_directory(service_dir)
    media_storage == "local" and create_media_directory()
    change_output_owner(service_dir, uid)
    use_gitlab = (
        use_gitlab
        if use_gitlab is not None
        else click.confirm(warning("Do you want to configure Gitlab?"), default=True)
    )
    if use_gitlab:
        gitlab_group_variables = {}
        if not gitlab_group_slug:
            gitlab_group_slug = click.prompt("Gitlab group slug", default=project_slug)
            click.confirm(
                warning(
                    f'Make sure the Gitlab "{gitlab_group_slug}" group exists '
                    "before proceeding. Continue?"
                ),
                abort=True,
            )
        gitlab_private_token = validate_or_prompt_password(
            gitlab_private_token,
            "Gitlab private token (with API scope enabled)",
            required=True,
        )
        sentry_dsn = validate_or_prompt_url(
            sentry_dsn, "Sentry DSN (leave blank if unused)", default=""
        )
        gitlab_project_variables = {}
        sentry_dsn and gitlab_project_variables.update(
            SENTRY_DSN='{value = "%s"}' % sentry_dsn
        )
        init_gitlab(
            gitlab_group_slug,
            gitlab_private_token,
            project_name,
            project_slug,
            service_slug,
            service_dir,
            gitlab_project_variables,
            gitlab_group_variables,
            terraform_dir,
            logs_dir,
        )


def slugify_option(ctx, param, value):
    """Slugify an option value."""
    return value and slugify(value)


def validate_or_prompt_url(value, message, default=None, required=False):
    """Validate the given URL or prompt until a valid value is provided."""
    if value is not None:
        if not required and value == "" or validators.url(value):
            return value
        else:
            click.echo("Please type a valid URL!")
    new_value = click.prompt(message, default=default)
    return validate_or_prompt_url(new_value, message, default, required)


def validate_or_prompt_password(value, message, default=None, required=False):
    """Validate the given password or prompt until a valid value is provided."""
    if value is not None:
        if not required and value == "" or validators.length(value, min=8):
            return value
        else:
            click.echo("Please type at least 8 chars!")
    new_value = click.prompt(message, default=default, hide_input=True)
    return validate_or_prompt_password(new_value, message, default, required)


@click.command()
@click.option("--uid", type=int)
@click.option("--output-dir", default=".", required=OUTPUT_DIR is None)
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
@click.option("--use-gitlab/--no-gitlab", is_flag=True, default=None)
@click.option("--gitlab-private-token", envvar=GITLAB_TOKEN_ENV_VAR)
@click.option("--gitlab-group-slug")
@click.option("--terraform-dir")
@click.option("--logs-dir")
def init_command(
    uid,
    output_dir,
    project_name,
    project_slug,
    project_dirname,
    service_slug,
    internal_service_port,
    project_url_dev,
    project_url_stage,
    project_url_prod,
    sentry_dsn,
    media_storage,
    use_gitlab,
    gitlab_private_token,
    gitlab_group_slug,
    terraform_dir,
    logs_dir,
):
    """Collect options and run the bootstrap."""
    output_dir = OUTPUT_DIR or output_dir
    project_slug = slugify(
        project_slug or click.prompt("Project slug", default=slugify(project_name)),
    )
    service_slug = slugify(
        service_slug or click.prompt("Service slug", default="backend"),
        separator="",
    )
    project_dirname_choices = [service_slug, slugify(project_slug, separator="")]
    project_dirname = project_dirname or click.prompt(
        "Project dirname",
        default=project_dirname_choices[0],
        type=click.Choice(project_dirname_choices),
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
    run(
        uid,
        output_dir,
        project_name,
        project_slug,
        project_dirname,
        service_slug,
        internal_service_port,
        project_url_dev,
        project_url_stage,
        project_url_prod,
        sentry_dsn,
        media_storage,
        use_gitlab,
        gitlab_private_token,
        gitlab_group_slug,
        terraform_dir,
        logs_dir,
    )


if __name__ == "__main__":
    init_command()
