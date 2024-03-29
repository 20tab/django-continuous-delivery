FROM python:3.12-slim-bookworm AS base

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="backend" stage="base"
ARG DEBIAN_FRONTEND=noninteractive
ARG USER=appuser
ENV APPUSER=$USER LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 WORKDIR=/app
WORKDIR $WORKDIR
RUN useradd --skel /dev/null --create-home $APPUSER
RUN chown $APPUSER:$APPUSER $WORKDIR
ENV PATH="/home/${APPUSER}/.local/bin:${PATH}"
ARG PACKAGES_PATH=/home/${APPUSER}/.local/lib/python3.12/site-packages
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/base.txt requirements/base.txt
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
    && su $APPUSER -c "python3 -m pip install --user --no-cache-dir -r requirements/base.txt" \
    && find ${PACKAGES_PATH} -regex '^.*/locale/.*/*.\(mo\|po\)$' -not -path '*/en*' -not -path '*/it*' -delete || true \
    && apt-get purge --assume-yes --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/common.txt requirements/common.txt
RUN su $APPUSER -c "python3 -m pip install --user --no-cache-dir -r requirements/common.txt" \
    && find ${PACKAGES_PATH} -regex '^.*/locale/.*/*.\(mo\|po\)$' -not -path '*/en*' -not -path '*/it*' -delete || true

FROM base AS test

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="backend" stage="test"
ENV DJANGO_CONFIGURATION=Testing
USER $APPUSER
COPY --chown=$APPUSER ./requirements/test.txt requirements/test.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/test.txt
COPY --chown=$APPUSER . .
CMD ./scripts/test.sh

FROM base AS remote

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="backend" stage="remote"
ENV DJANGO_CONFIGURATION=Remote INTERNAL_SERVICE_PORT={{ cookiecutter.internal_service_port }}
USER $APPUSER
ARG PACKAGES_PATH=/home/${APPUSER}/.local/lib/python3.12/site-packages
COPY --chown=$APPUSER ./requirements/remote.txt requirements/remote.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/remote.txt \
    && find ${PACKAGES_PATH}/boto*/data/* -maxdepth 0 -type d -not -name s3* -exec rm -rf {} \; || true
COPY --chown=$APPUSER . .
RUN DJANGO_SECRET_KEY=build python3 -m manage collectstatic --clear --link --noinput
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["python3", "-m", "gunicorn", "{{ cookiecutter.django_settings_dirname }}.asgi"]

FROM base AS local

LABEL company="20tab" project="{{ cookiecutter.project_slug }}" service="backend" stage="local"
ENV DJANGO_CONFIGURATION=Local INTERNAL_SERVICE_PORT={{ cookiecutter.internal_service_port }}
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        curl \
        gcc \
        gettext \
        git \
        graphviz \
        libpq-dev \
        make \
        openssh-client \
        postgresql-client
USER $APPUSER
COPY --chown=$APPUSER ./requirements/local.txt requirements/local.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/local.txt
COPY --chown=$APPUSER . .
RUN DJANGO_SECRET_KEY=build python3 -m manage collectstatic --clear --link --noinput
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD python3 -m manage runserver 0.0.0.0:${INTERNAL_SERVICE_PORT}
