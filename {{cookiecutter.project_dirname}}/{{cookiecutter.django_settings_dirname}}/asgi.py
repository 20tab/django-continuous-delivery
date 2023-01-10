"""
ASGI config for {{ cookiecutter.project_name }} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "{{ cookiecutter.django_settings_dirname }}.settings"
)

from configurations.asgi import get_asgi_application

application = get_asgi_application()
