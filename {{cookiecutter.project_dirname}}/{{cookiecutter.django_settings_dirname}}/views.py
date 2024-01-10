"""The main app views."""

from django.http import HttpResponse
from django.views.generic import View


class HealthView(View):
    """The health endpoint view."""

    http_method_names = ("get", "head", "options")

    def get(self, request, *args, **kwargs):
        """Return health endpoint GET response."""
        return HttpResponse(status=204)
