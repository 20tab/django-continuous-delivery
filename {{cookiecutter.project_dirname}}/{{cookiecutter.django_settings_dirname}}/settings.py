"""
Django settings for {{ cookiecutter.project_name }} project.

Generated by 'django-admin startproject' using Django.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import string
from pathlib import Path

from configurations import Configuration, values


class ProjectDefault(Configuration):
    """
    The default settings from the Django project template.

    Django Configurations
    https://django-configurations.readthedocs.io
    """

    # Build paths inside the project like this: BASE_DIR / "subdir".
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "{{ cookiecutter.django_settings_dirname }}.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "{{ cookiecutter.django_settings_dirname }}.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/stable/ref/settings/#databases

    DATABASES = values.DatabaseURLValue()

    # Password validation
    # https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
    # fmt: off
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]
    # fmt: on
    # Internationalization
    # https://docs.djangoproject.com/en/stable/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/stable/howto/static-files/

    STATIC_URL = "/static/"

    STATIC_ROOT = BASE_DIR / "static"

    # Stored files
    # https://docs.djangoproject.com/en/stable/topics/files/{% if cookiecutter.media_storage == "local" %}  # noqa

    MEDIA_URL = "/media/"

    MEDIA_ROOT = BASE_DIR / "media"  # noqa{% else %}

    # Uncomment when using local media

    # MEDIA_URL = "/media/"

    # MEDIA_ROOT = BASE_DIR / "media"{% endif %}

    # Email Settings
    # https://docs.djangoproject.com/en/stable/topics/email/

    ADMINS = values.SingleNestedTupleValue(
        (("admin", "errors@{{ cookiecutter.project_slug }}.com"),)
    )

    DEFAULT_FROM_EMAIL = values.EmailValue("info@{{ cookiecutter.project_slug }}.com")

    EMAIL_SUBJECT_PREFIX = "[{{ cookiecutter.project_name }}] "

    EMAIL_USE_LOCALTIME = True

    SERVER_EMAIL = values.EmailValue("server@{{ cookiecutter.project_slug }}.com")

    # Email URL
    # https://django-configurations.readthedocs.io/en/stable/values.html

    EMAIL = values.EmailURLValue("console://")

    # Cache URL
    # https://django-configurations.readthedocs.io/en/stable/values.html

    CACHES = values.CacheURLValue("locmem://")

    # Translation
    # https://docs.djangoproject.com/en/stable/topics/i18n/translation/

    # LANGUAGES = (("en", "English"), ("it", "Italiano"))

    # Clickjacking Protection
    # https://docs.djangoproject.com/en/stable/ref/clickjacking/

    X_FRAME_OPTIONS = "SAMEORIGIN"  # Default: 'SAMEORIGIN'

    # Default primary key field type
    # https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Session auth
    # https://docs.djangoproject.com/en/stable/ref/settings/#sessions

    SESSION_COOKIE_DOMAIN = values.Value()

    # Secure Proxy SSL Header
    # https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


class Local(ProjectDefault):
    """The local settings."""

    # Application definition

    INSTALLED_APPS = ProjectDefault.INSTALLED_APPS.copy()

    MIDDLEWARE = ProjectDefault.MIDDLEWARE.copy()

    # Django Debug Toolbar
    # https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

    try:
        import debug_toolbar  # noqa
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        INTERNAL_IPS = values.ListValue(["127.0.0.1"])
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
        DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

    # Django Extensions
    # https://django-extensions.readthedocs.io/en/stable/graph_models.html

    try:
        import django_extensions  # noqa
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        INSTALLED_APPS.append("django_extensions")
        SHELL_PLUS_PRINT_SQL = True
        SHELL_PLUS_PRINT_SQL_TRUNCATE = None
        GRAPH_MODELS = {
            "all_applications": True,
            "arrow_shape": "diamond",
            "disable_abstract_fields": False,
            "disable_fields": False,
            "exclude_columns": [
                "date_joined",
                "is_active",
                "is_staff",
                "is_superuser",
                "last_login",
            ],
            "exclude_models": ",".join(
                (
                    "AbstractBaseSession",
                    "AbstractBaseUser",
                    "AbstractUser",
                    "ContentType",
                    "Group",
                    "LogEntry",
                    "Permission",
                    "PermissionsMixin",
                    "Session",
                    "UserGroup",
                )
            ),
            "group_models": True,
            "hide_edge_labels": True,
            "inheritance": False,
            "language": "it",
            "layout": "dot",
            "relations_as_fields": True,
            "theme": "django2018",
            "verbose_names": True,
        }


class Testing(ProjectDefault):
    """The testing settings."""

    SECRET_KEY = string.ascii_letters

    # Debug
    # https://docs.djangoproject.com/en/stable/ref/settings/#debug

    DEBUG = False

    # Application definition

    INSTALLED_APPS = ProjectDefault.INSTALLED_APPS.copy()

    # Email URL
    # https://django-configurations.readthedocs.io/en/stable/values/

    EMAIL = "dummy://"

    # Cache URL
    # https://django-configurations.readthedocs.io/en/stable/values/

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

    # During testing, ensure that the STATICFILES_STORAGE setting is set to the default.
    # https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/

    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    # The MD5 based password hasher is much less secure but faster
    # https://docs.djangoproject.com/en/stable/topics/auth/passwords/

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]

    # Behave
    # https://behave-django.readthedocs.io/en/latest/installation.html

    try:
        import behave_django  # noqa
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        INSTALLED_APPS.append("behave_django")

    # Stored files
    # https://docs.djangoproject.com/en/stable/topics/files/{% if cookiecutter.media_storage != "none" %}  # noqa

    MEDIA_ROOT = ProjectDefault.BASE_DIR / "media_test"  # noqa{% else %}

    # Uncomment when using media

    # MEDIA_ROOT = ProjectDefault.BASE_DIR / "media_test"{% endif %}


class Remote(ProjectDefault):
    """The remote settings."""

    # Debug
    # https://docs.djangoproject.com/en/stable/ref/settings/#debug

    DEBUG = False

    MIDDLEWARE = ProjectDefault.MIDDLEWARE.copy()

    # Email URL
    # https://django-configurations.readthedocs.io/en/stable/values/

    EMAIL = values.EmailURLValue()

    # Security
    # https://docs.djangoproject.com/en/stable/topics/security/

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_HSTS_SECONDS = 60

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_SSL_REDIRECT = False

    SECURE_HSTS_PRELOAD = True

    X_FRAME_OPTIONS = "DENY"

    # Persistent connections
    # https://docs.djangoproject.com/en/stable/ref/databases/#general-notes

    CONN_MAX_AGE = None

    # Session auth
    # https://docs.djangoproject.com/en/stable/ref/settings/#sessions

    SESSION_COOKIE_SECURE = True

    # WhiteNoise
    # http://whitenoise.evans.io/en/stable/django.html

    try:
        import whitenoise  # noqa
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # Sentry
    # https://sentry.io/for/django/

    try:
        import sentry_sdk  # noqa
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        from sentry_sdk.integrations.django import DjangoIntegration  # noqa{% if cookiecutter.use_redis == "True" %}
        from sentry_sdk.integrations.redis import RedisIntegration  # noqa{% endif %}

        sentry_sdk.init(
            integrations=[
                DjangoIntegration(),{% if cookiecutter.use_redis == "True" %}
                RedisIntegration(),{% endif %}
            ],
            send_default_pii=True,
        ){% if "s3" in cookiecutter.media_storage %}
    # Django Storages
    # https://django-storages.readthedocs.io/en/stable/

    AWS_LOCATION = values.Value("")

    AWS_S3_ENDPOINT_URL = values.Value()

    AWS_S3_FILE_OVERWRITE = values.BooleanValue(False)

    AWS_STORAGE_BUCKET_NAME = values.Value()

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"  # noqa {% endif %}
