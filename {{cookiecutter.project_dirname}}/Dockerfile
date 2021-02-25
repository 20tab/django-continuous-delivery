FROM python:3.8-slim-buster AS base

ARG USER=appuser
ENV APPUSER=$USER DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 WORKDIR=/app
WORKDIR $WORKDIR
RUN useradd --home-dir $WORKDIR $APPUSER
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


FROM base AS remote

COPY --chown=$APPUSER ./requirements/remote.txt requirements/remote.txt
RUN python3 -m pip install --no-cache-dir -r requirements/remote.txt
COPY --chown=$APPUSER . .
USER $APPUSER
CMD python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --clear --noinput && \
    uwsgi uwsgiconf/docker.ini


FROM base AS test

ENV DJANGO_CONFIGURATION=Testing
COPY --chown=$APPUSER ./requirements/test.txt requirements/test.txt
RUN python3 -m pip install --no-cache-dir -r requirements/test.txt
COPY --chown=$APPUSER . .
USER $APPUSER
CMD ./scripts/test.sh


FROM base AS local

RUN apt-get update && apt-get install -y --no-install-recommends \
        gettext \
        graphviz \
        libpq-dev \
        make
COPY ./requirements/local.txt requirements/local.txt
RUN python3 -m pip install --no-cache-dir -r requirements/local.txt
COPY --chown=$APPUSER . .
USER $APPUSER
CMD python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --clear --noinput && \
    python3 manage.py runserver 0.0.0.0:8000
