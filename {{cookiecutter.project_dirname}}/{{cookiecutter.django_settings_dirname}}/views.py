"""The main app views."""

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """The health endpoint view."""

    permission_classes = ()

    def get(self, request):
        """Return the health status."""
        return Response({"status": "ok"})
