FROM python:3.9-slim-buster AS base

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=appuser
ENV APPUSER=$USER LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 WORKDIR=/app
WORKDIR $WORKDIR
RUN useradd --skel /dev/null --create-home $APPUSER
RUN chown $APPUSER:$APPUSER $WORKDIR
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        mime-support \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/base.txt requirements/base.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
    && python3 -m pip install --no-cache-dir -r requirements/base.txt \
    && apt-get purge -y --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/common.txt requirements/common.txt
RUN python3 -m pip install --no-cache-dir -r requirements/common.txt


FROM base AS test

ENV DJANGO_CONFIGURATION=Testing
COPY --chown=$APPUSER ./requirements/test.txt requirements/test.txt
RUN python3 -m pip install --no-cache-dir -r requirements/test.txt
COPY --chown=$APPUSER . .
USER $APPUSER
CMD ./scripts/test.sh --reverse


FROM base AS remote

COPY --chown=$APPUSER ./requirements/remote.txt requirements/remote.txt
RUN python3 -m pip install --no-cache-dir -r requirements/remote.txt
COPY --chown=$APPUSER . .
USER $APPUSER
CMD python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --clear --noinput && \
    gunicorn {{cookiecutter.project_slug}}.asgi:application


FROM base AS local

RUN apt-get update && apt-get install -y --no-install-recommends \
        gettext \
        git \
        graphviz \
        libpq-dev \
        make \
        openssh-client
COPY ./requirements/local.txt requirements/local.txt
RUN python3 -m pip install --no-cache-dir -r requirements/local.txt
COPY --chown=$APPUSER . .
USER $APPUSER
CMD python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --clear --noinput && \
    python3 manage.py runserver 0.0.0.0:8000
