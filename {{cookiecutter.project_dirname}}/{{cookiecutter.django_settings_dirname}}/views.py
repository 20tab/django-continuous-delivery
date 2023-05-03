"""The main app views."""

from django.http import JsonResponse
from django.views.generic import View


class HealthView(View):
    """The health endpoint view."""

    http_method_names = ("get", "options")

    def get(self, request, *args, **kwargs):
        """Return health endpoint response."""
        return JsonResponse({"status": "ok"})
