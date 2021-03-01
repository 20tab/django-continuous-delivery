#!/usr/bin/env bash

black -q --check .
isort -q --check .
flake8
mypy .
