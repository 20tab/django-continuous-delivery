"""
WSGI config for {{ cookiecutter.project_name }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "{{ cookiecutter.django_settings_dirname }}.settings"
)
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

from configurations.wsgi import get_wsgi_application  # noqa isort:skip

application = get_wsgi_application()