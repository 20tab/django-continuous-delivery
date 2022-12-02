"""Define pacts provider state handler."""

import re
from datetime import datetime

import time_machine
from django.utils.text import slugify
from pactman.verifier.verify import ProviderStateMissing

DEFAULT_DATETIME = datetime(2021, 5, 17, 8, 30, 00)


def make_key(*args):  # pragma: no cover
    """Make a key."""
    return slugify("-".join(str(i) for i in args if i))


class ProviderStatesContext(dict):
    """A context for Provider states inizialization."""

    def __init__(self, *args, **kwargs):
        """Initialize the instance."""
        self.live_server = None
        self.freezer = None
        self.patchers = {}
        self.requests_mockers = {}
        return super().__init_subclass__()

    def set_default_freezer(self):
        """Set the default freezer."""
        freezer = time_machine.travel(DEFAULT_DATETIME, tick=False)
        freezer.start()
        self.freezer = freezer

    def cleanup(self):
        """Clean up the context."""
        self.freezer and self.freezer.stop()
        [i.stop() for i in self.patchers.values()]
        [i.stop() for i in self.requests_mockers.values()]


class ProviderStatesHandler:
    """A Provider states handler."""

    def __init__(self):
        """Initialize the instance."""
        self.handlers = []
        self.context = ProviderStatesContext()

    def register(self, state_matcher):
        """Register the given function as a handler."""

        def outer_wrapper(function):
            """Register and return the function."""
            try:
                pattern = re.compile(state_matcher, re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid pattern provided: {state_matcher}.") from e
            self.handlers.append((pattern, function))
            return function

        return outer_wrapper

    def set_live_server(self, live_server):
        """Set the live server in context."""
        self.context.live_server = live_server

    def handle(self, state, context, **params):
        """Handle the given provider state."""
        handlers = iter(self.handlers)
        while True:
            try:
                pattern, function = next(handlers)
                if result := pattern.match(state):
                    function(context=context, **params, **result.groupdict())
                    return
            except (StopIteration, TypeError):
                break
        raise ProviderStateMissing(state)

    def tear_down(self):
        """Clean up after handling states."""
        self.context.cleanup()

    def run(self, provider_state_name, **params):
        """Set up the given provider state."""
        self.context.set_default_freezer()
        for handler_name in provider_state_name.split("/"):
            self.handle(handler_name.strip(), self.context, **params)


handler = ProviderStatesHandler()
