#!/usr/bin/env bash

wait-for-it --quiet --service postgres:5432 -- \
  python3 manage.py behave --configuration=Testing --simple
