#!/usr/bin/env bash

set -euo pipefail

python3 -m coverage run manage.py test --configuration=Testing --noinput --parallel --shuffle --buffer
