FROM python:3.9-slim-bullseye AS base

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=appuser
ENV APPUSER=$USER LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 WORKDIR=/app
WORKDIR $WORKDIR
RUN useradd --skel /dev/null --create-home $APPUSER
RUN chown $APPUSER:$APPUSER $WORKDIR
ENV PATH="/home/${APPUSER}/.local/bin:${PATH}"
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/base.txt requirements/base.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
    && su $APPUSER -c "python3 -m pip install --user --upgrade pip~=21.3.0" \
    && su $APPUSER -c "python3 -m pip install --user --no-cache-dir -r requirements/base.txt" \
    && apt-get purge -y --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --chown=$APPUSER ./requirements/common.txt requirements/common.txt
RUN su $APPUSER -c "python3 -m pip install --user --no-cache-dir -r requirements/common.txt"


FROM base AS test

ENV DJANGO_CONFIGURATION=Testing
USER $APPUSER
COPY --chown=$APPUSER ./requirements/test.txt requirements/test.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/test.txt
COPY --chown=$APPUSER . .
CMD ./scripts/test.sh --reverse


FROM base AS remote

USER $APPUSER
ARG PACKAGES_PATH=/home/${APPUSER}/.local/lib/python3.9/site-packages
COPY --chown=$APPUSER ./requirements/remote.txt requirements/remote.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/remote.txt \
    && find ${PACKAGES_PATH}/botocore/data/* -not -name s3 -delete \
    && find ${PACKAGES_PATH}/babel/locale-data/* -not -name en* -not -name it* -not -name root* -delete
COPY --chown=$APPUSER . .
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["python3", "-m", "gunicorn", "jetmarketreloaded.asgi:application"]


FROM base AS local

ENV DJANGO_CONFIGURATION=Local PYTHONFAULTHANDLER=1
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
        git \
        graphviz \
        libpq-dev \
        make \
        openssh-client
USER $APPUSER
COPY --chown=$APPUSER ./requirements/local.txt requirements/local.txt
RUN python3 -m pip install --user --no-cache-dir -r requirements/local.txt
COPY --chown=$APPUSER . .
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
