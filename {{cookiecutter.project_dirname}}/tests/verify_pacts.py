"""Define tests to verify pacts."""

import re

from pactman.verifier.verify import ProviderStateMissing


class ProviderStatesHandler:
    """A handler for provider states."""

    def __init__(self):
        """Initialize the instance."""
        self.handlers = []
        self.context = {}

    def register(self, state_matcher):
        """Register the given function as a handler."""

        def outer_wrapper(function):
            """Register and return the function."""
            try:
                pattern = re.compile(state_matcher, re.IGNORECASE)
            except re.error:
                raise ValueError(f"Invalid pattern provided: {state_matcher}.")
            self.handlers.append((pattern, function))
            return function

        return outer_wrapper

    def handle(self, state, context):
        """Handle the given provider state."""
        handlers = iter(self.handlers)
        while True:
            try:
                pattern, function = next(handlers)
            except StopIteration:
                break
            else:
                result = pattern.match(state)
                if result:
                    return function(context=context, **result.groupdict())
        raise ProviderStateMissing(state)

    def tear_down(self):
        """Clean up after handling states."""
        try:
            self.context["traveller"].stop()
        except KeyError:
            pass

    def run(self, name, **params):
        """Set up the given provider state."""
        self.context = {**params}
        for handler_name in name.split("/"):
            self.handle(handler_name.strip(), self.context)


handler = ProviderStatesHandler()


def test_pacts(live_server, pact_verifier):
    """Test pacts."""
    pact_verifier.verify(live_server.url, handler.run)
    handler.tear_down()
