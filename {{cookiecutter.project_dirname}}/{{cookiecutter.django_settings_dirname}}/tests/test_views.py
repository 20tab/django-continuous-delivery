"""The main app views tests."""

from django.test import Client, TestCase


class ApiHealthTest(TestCase):
    """The health view tests."""

    url = "/backend/health/"
    client = Client()

    def test_health(self):
        """Test api health endpoint."""
        with self.subTest("GET"):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "ok"})
            self.assertEqual(
                response.headers,
                {
                    "Content-Type": "application/json",
                    "X-Frame-Options": "SAMEORIGIN",
                    "Content-Length": "16",
                    "X-Content-Type-Options": "nosniff",
                    "Referrer-Policy": "same-origin",
                    "Cross-Origin-Opener-Policy": "same-origin",
                },
            )
        with self.subTest("OPTIONS"):
            response = self.client.options(self.url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b"")
            self.assertEqual(
                response.headers,
                {
                    "Content-Type": "text/html; charset=utf-8",
                    "X-Frame-Options": "SAMEORIGIN",
                    "Allow": "GET, OPTIONS",
                    "Content-Length": "0",
                    "X-Content-Type-Options": "nosniff",
                    "Referrer-Policy": "same-origin",
                    "Cross-Origin-Opener-Policy": "same-origin",
                },
            )
        with self.subTest("POST"):
            response = self.client.post(self.url)
            self.assertEqual(response.status_code, 405)
