#!/usr/bin/env bash

wait-for-it --quiet --service postgres:5432 -- \
  coverage run manage.py test --configuration=Testing --noinput --parallel $@
