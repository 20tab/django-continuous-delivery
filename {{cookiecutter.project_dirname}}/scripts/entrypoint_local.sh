#!/usr/bin/env bash

set -euo pipefail

./entrypoint.sh
minio-client alias set minio http://minio:9000 minio-admin minio-admin;
minio-client mb --quiet --ignore-existing minio/{{ cookiecutter.project_slug }};
minio-client anonymous set download minio/{{ cookiecutter.project_slug }};
exec "${@}"
