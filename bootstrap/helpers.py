"""Web project initialization helpers."""

import re
from functools import partial

import click
import validators
from slugify import slugify

error = partial(click.style, fg="red")

warning = partial(click.style, fg="yellow")


def format_gitlab_variable(value, masked=False, protected=True):
    """Format the given value to be used as a GitLab variable."""
    return (
        f'{{ value = "{value}"'
        + (masked and ", masked = true" or "")
        + (not protected and ", protected = false" or "")
        + " }"
    )


def format_tfvar(value, value_type=None):
    """Format the given value to be used as a Terraform variable."""
    if value_type == "list":
        return "[" + ", ".join(format_tfvar(i) for i in value) + "]"
    elif value_type == "bool":
        return value and "true" or "false"
    elif value_type == "num":
        return str(value)
    else:
        return f'"{value}"'


def slugify_option(ctx, param, value):
    """Slugify an option value."""
    return value and slugify(value)


def validate_or_prompt_domain(message, value=None, default=None, required=True):
    """Validate the given domain or prompt until a valid value is provided."""
    if value is None:
        value = click.prompt(message, default=default)
    if not required and value == "" or validators.domain(value):
        return value
    click.echo(error("Please type a valid domain!"))
    return validate_or_prompt_domain(message, None, default, required)


def validate_or_prompt_email(message, value=None, default=None, required=True):
    """Validate the given email address or prompt until a valid value is provided."""
    if value is None:
        value = click.prompt(message, default=default)
    if not required and value == "" or validators.email(value):
        return value
    click.echo(error("Please type a valid email!"))
    return validate_or_prompt_email(message, None, default, required)


def validate_or_prompt_secret(message, value=None, default=None, required=True):
    """Validate the given secret or prompt until a valid value is provided."""
    if value is None:
        value = click.prompt(message, default=default, hide_input=True)
    if not required and value == "" or validators.length(value, min=8):
        return value

    click.echo(error("Please type at least 8 chars!"))
    return validate_or_prompt_secret(message, None, default, required)


def validate_or_prompt_path(message, value=None, default=None, required=True):
    """Validate the given path or prompt until a valid path is provided."""
    if value is None:
        value = click.prompt(message, default=default)
    if (
        not required
        and value == ""
        or re.match(r"^(?:/?[\w_\-]+)(?:\/[\w_\-]+)*\/?$", value)
    ):
        return value
    click.echo(
        error(
            "Please type a valid slash-separated path containing letters, digits, "
            "dashes and underscores!"
        )
    )
    return validate_or_prompt_path(message, None, default, required)


def validate_or_prompt_url(message, value=None, default=None, required=True):
    """Validate the given URL or prompt until a valid value is provided."""
    if value is None:
        value = click.prompt(message, default=default)
    if not required and value == "" or validators.url(value):
        return value.rstrip("/")

    click.echo(error("Please type a valid URL!"))
    return validate_or_prompt_url(message, None, default, required)
