FROM python:3.8-slim-buster AS base

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        gettext \
        libpq5 \
        mime-support \
    && rm -rf /var/lib/apt/lists/*
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


FROM base AS prod

COPY ./requirements/prod.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . .
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --clear --noinput && \
    uwsgi uwsgiconf/docker.ini


FROM base AS dev

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        libpq-dev \
        make \
        ssh-client
COPY ./requirements/dev.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --clear --noinput && \
    uwsgi uwsgiconf/docker.ini


FROM base AS test

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && pip3 install --no-cache-dir -U pip tox
CMD tox -e coverage,reporthtml,report
