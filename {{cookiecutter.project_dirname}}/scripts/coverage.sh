#!/usr/bin/env bash

# Bash "strict mode", to help catch problems and bugs in the shell script
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

coverage run manage.py test --configuration=Testing --noinput --parallel
