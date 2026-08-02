"""Vanilla frontend route tests."""

import unittest

from bookloop import create_app


class VanillaFrontendTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

    def test_index_returns_bookloop_html(self):
        response = self.client.get("/vanilla/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BookLoop", response.data)
        self.assertIn(b"./vanilla-favicon.svg", response.data)
        response.close()

    def test_favicon_asset_is_available(self):
        response = self.client.get("/vanilla/vanilla-favicon.svg")

        self.assertEqual(response.status_code, 200)
        response.close()

    def test_javascript_asset_is_available(self):
        response = self.client.get("/vanilla/app.js")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'healthApiUrl = "http://127.0.0.1:5000/api/health"',
            response.data,
        )
        self.assertIn(b"fetch(healthApiUrl)", response.data)
        response.close()


if __name__ == "__main__":
    unittest.main()
