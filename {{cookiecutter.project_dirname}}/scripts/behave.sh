#!/usr/bin/env bash

set -ex

wait-for-it --quiet --service postgres:5432 -- \
  python3 manage.py behave --configuration=Testing --simple
