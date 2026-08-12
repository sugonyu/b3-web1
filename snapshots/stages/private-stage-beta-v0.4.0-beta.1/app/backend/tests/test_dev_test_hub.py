"""BookLoop 개발용 비교 hub route와 핵심 링크 테스트."""

import unittest

from bookloop import create_app


class DeveloperTestHubTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

    def test_dev_test_hub_groups_clients_api_and_tools(self):
        response = self.client.get("/test")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BookLoop Test Hub", response.data)
        self.assertIn(b'class="brand-badge" href="/"', response.data)
        self.assertIn(b"/static/bookloop/python-favicon.svg", response.data)
        self.assertIn("1 · Clients".encode(), response.data)
        self.assertIn("2 · API".encode(), response.data)
        self.assertIn("3 · Developer Tools".encode(), response.data)
        self.assertIn(b'href="#clients"', response.data)
        self.assertIn(b'href="#api"', response.data)
        self.assertIn(b'href="#tools"', response.data)
        self.assertIn(b'href="/jinja/"', response.data)
        self.assertIn(b'href="/vanilla/"', response.data)
        self.assertIn(b'href="/api/health"', response.data)
        self.assertIn(b'href="/dev/db/"', response.data)
        self.assertIn(
            b"http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/",
            response.data,
        )
        response.close()


if __name__ == "__main__":
    unittest.main()
