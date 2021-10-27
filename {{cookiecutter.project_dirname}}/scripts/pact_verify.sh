#!/usr/bin/env bash

pytest --dc=Testing --disable-warnings \
    --pact-verify-consumer=$PACT_CONSUMER_NAME \
    --pact-provider-name=$PACT_PROVIDER_NAME \
	$@ tests/verify_pacts.py
