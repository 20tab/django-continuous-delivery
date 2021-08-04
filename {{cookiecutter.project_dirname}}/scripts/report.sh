#!/usr/bin/env bash

set -ex

coverage combine
coverage html
coverage report -m
