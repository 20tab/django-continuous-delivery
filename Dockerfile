FROM python:3.12-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ARG OUTPUT_BASE_DIR=/data
ENV OUTPUT_BASE_DIR=${OUTPUT_BASE_DIR}
WORKDIR /app
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        curl \
        git \
        gnupg \
        libpq-dev \
        software-properties-common \
    && curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - \
    && apt-add-repository "deb https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    && apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        terraform \
    && rm -rf /var/lib/apt/lists/*
COPY ./requirements/common.txt requirements/common.txt
RUN python3 -m pip install --no-cache-dir -r requirements/common.txt
COPY . .
RUN mkdir ${OUTPUT_BASE_DIR}
ENTRYPOINT [ "python", "/app/start.py" ]
