"""Tests to verify pacts."""

from django.utils.module_loading import autodiscover_modules

from pacts.handler import handler

autodiscover_modules("tests.pact_states")


def test_pacts(live_server, pact_verifier):
    """Test pacts."""
    pact_verifier.verify(live_server.url, handler.run)
    handler.tear_down()
