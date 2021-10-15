#!/usr/bin/env bash

set -ex

python3 -m coverage combine
python3 -m coverage html
python3 -m coverage report -m
