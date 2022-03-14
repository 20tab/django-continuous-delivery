"""Define pacts provider state handler."""

import re
from datetime import datetime
from unittest.mock import patch

from freezegun import freeze_time
from pactman.verifier.verify import ProviderStateMissing


class ProviderStatesHandler:
    """A handler for provider states."""

    def __init__(self):
        """Initialize the instance."""
        self.handlers = []
        self.context = {}
        self.patchers = []

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

    def add_patch(self, *args, **kwargs):
        """Create a patcher."""
        self.patchers.append(patch(*args, **kwargs))

    def init_patchers(self):
        """Initialize the patchers."""
        [i.start() for i in self.patchers]

    def set_default_freezer(self):
        """Set the default freezer."""
        frozen_datetime = datetime(2021, 5, 17, 8, 30, 00)
        freezer = freeze_time(frozen_datetime, tz_offset=0)
        freezer.start()
        self.context["freezer"] = freezer

    def handle(self, state, context):
        """Handle the given provider state."""
        handlers = iter(self.handlers)
        while True:
            try:
                pattern, function = next(handlers)
            except StopIteration:
                break
            else:
                if result := pattern.match(state):
                    return function(context=context, **result.groupdict())
        raise ProviderStateMissing(state)

    def tear_down(self):
        """Clean up after handling states."""
        try:
            self.context["freezer"].stop()
        except KeyError:
            pass
        [i.stop() for i in self.patchers]

    def run(self, name, **params):
        """Set up the given provider state."""
        self.context = {**params, "patchers": {}}
        self.set_default_freezer()
        self.init_patchers()
        for handler_name in name.split("/"):
            self.handle(handler_name.strip(), self.context)


handler = ProviderStatesHandler()
