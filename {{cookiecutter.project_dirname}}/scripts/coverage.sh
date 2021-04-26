#!/usr/bin/env bash

coverage run manage.py test --configuration=Testing --noinput --parallel $@
