"""Private Stage A-1 health endpoint test."""

import unittest

from bookloop import create_app


class HealthEndpointTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

    def test_health_returns_service_status(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "app": "BookLoop",
                "service": "flask-api",
                "status": "ok",
                "version": "0.2.0",
            },
        )

    def test_health_allows_local_live_preview_origin(self):
        response = self.client.get(
            "/api/health",
            headers={"Origin": "http://127.0.0.1:3000"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"],
            "http://127.0.0.1:3000",
        )

    def test_health_allows_local_wordpress_static_origin(self):
        response = self.client.get(
            "/api/health",
            headers={"Origin": "http://localhost:8080"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"],
            "http://localhost:8080",
        )


if __name__ == "__main__":
    unittest.main()
