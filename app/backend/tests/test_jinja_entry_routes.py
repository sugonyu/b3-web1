"""Flask root와 Jinja reference 진입 route 테스트."""

import unittest

from bookloop import create_app
from bookloop.db import db


class JinjaEntryRoutesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        # W2-08 제품 홈은 실제 BookListing 테이블을 읽는다.
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_root_renders_independent_product_home(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<a', response.data)
        self.assertIn(b'class="product-logo"', response.data)
        self.assertIn(b'href="/"', response.data)
        self.assertIn(b"Sign in before requesting a book.", response.data)
        self.assertIn(b"Books", response.data)
        self.assertIn(b"Log in", response.data)
        self.assertNotIn(b"Sent requests", response.data)
        self.assertNotIn(b"Received requests", response.data)
        self.assertNotIn(b'href="/test/"', response.data)
        self.assertNotIn(b'href="/jinja/"', response.data)
        self.assertIn(b"/static/bookloop/python-favicon.svg", response.data)
        response.close()

    def test_jinja_reference_renders_shared_health_data(self):
        response = self.client.get("/jinja/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BookLoop", response.data)
        self.assertIn("🐍".encode(), response.data)
        self.assertIn(b"/static/bookloop/python-favicon.svg", response.data)
        self.assertIn(b"flask-api", response.data)
        self.assertIn(b"0.2.0", response.data)
        self.assertIn(b"http://127.0.0.1:3001/ejs/", response.data)
        self.assertIn(b"/static/bookloop/flask-logo.svg", response.data)

        favicon_response = self.client.get("/static/bookloop/python-favicon.svg")
        self.assertEqual(favicon_response.status_code, 200)

        logo_response = self.client.get("/static/bookloop/flask-logo.svg")
        self.assertEqual(logo_response.status_code, 200)
        self.assertIn("image/svg+xml", logo_response.content_type)


if __name__ == "__main__":
    unittest.main()
