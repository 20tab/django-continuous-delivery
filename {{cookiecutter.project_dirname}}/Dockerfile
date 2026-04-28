FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim AS base

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="{{ cookiecutter.service_slug }}" stage="base"

ARG DEBIAN_FRONTEND=noninteractive \
    GROUP_ID=1000 \
    USER_ID=1000 \
    USER=appuser

ENV APPUSER=$USER \
    INTERNAL_SERVICE_PORT={{ cookiecutter.internal_service_port }} \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WORKDIR=/app \
    UV_COMPILE_BYTECODE=1

ENV UV_PROJECT_ENVIRONMENT="/home/$APPUSER/.venv" \
    UV_PYTHON_INSTALL_DIR="/home/$APPUSER/.local/share/uv/python"

ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

WORKDIR $WORKDIR

RUN groupadd --gid "$GROUP_ID" "$APPUSER" && \
    useradd --uid "$USER_ID" --gid "$GROUP_ID" --create-home --skel /dev/null \
    "$APPUSER"

RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        ca-certificates \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=$APPUSER ./pyproject.toml ./uv.lock ./

RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
    && chown -R "$USER_ID":"$GROUP_ID" "$WORKDIR" \
    && su "$APPUSER" -c "uv sync --frozen" \
    && apt-get purge --assume-yes --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*


FROM base AS remote

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="{{ cookiecutter.service_slug }}" stage="remote"

ENV DJANGO_CONFIGURATION=Remote

RUN su "$APPUSER" -c "uv sync --frozen --group remote"

COPY --chown=$APPUSER . .

RUN DJANGO_SECRET_KEY=build python3 -m manage collectstatic --clear --link --noinput

USER $APPUSER

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["gunicorn", "{{ cookiecutter.django_settings_dirname }}.asgi"]


FROM base AS local

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="{{ cookiecutter.service_slug }}" stage="local"

ENV DJANGO_CONFIGURATION=Local

RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        curl \
        gettext \
        git \
        graphviz \
        openssh-client \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN su "$APPUSER" -c "uv sync --frozen --group local"

COPY --chown=$APPUSER . .

USER $APPUSER

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["sh", "-c", "exec python3 -m manage runserver 0.0.0.0:${INTERNAL_SERVICE_PORT}"]
