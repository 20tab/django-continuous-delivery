"""The main app views tests."""

from rest_framework import status
from rest_framework.test import APITestCase


class ApiHealthTest(APITestCase):
    """The health view tests."""

    url = "/api/health/"

    def test_health(self):
        """Test api health endpoint."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
