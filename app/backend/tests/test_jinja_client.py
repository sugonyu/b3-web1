"""Optional Jinja comparison client tests."""

import unittest

from bookloop import create_app


class JinjaClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

    def test_root_renders_independent_product_home(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello BookLoop", response.data)
        self.assertIn(b'href="/test/"', response.data)
        self.assertIn(b'href="/jinja/"', response.data)
        self.assertIn(b"/static/web/python-favicon.svg", response.data)
        response.close()

    def test_jinja_reference_renders_shared_health_data(self):
        response = self.client.get("/jinja/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BookLoop", response.data)
        self.assertIn("🐍".encode(), response.data)
        self.assertIn(b"/static/web/python-favicon.svg", response.data)
        self.assertIn(b"flask-api", response.data)
        self.assertIn(b"0.2.0", response.data)

        favicon_response = self.client.get("/static/web/python-favicon.svg")
        self.assertEqual(favicon_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
