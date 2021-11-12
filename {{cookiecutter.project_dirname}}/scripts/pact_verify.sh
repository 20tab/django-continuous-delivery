#!/usr/bin/env bash

wait-for-it --quiet --service postgres:5432 -- \
  pytest --dc=Testing --disable-warnings \
    --pact-provider-name=$PACT_PROVIDER_NAME \
	  $@ pacts/verify_pacts.py
