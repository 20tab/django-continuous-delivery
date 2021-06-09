#!/usr/bin/env bash

set -e

coverage combine
coverage html
coverage report
