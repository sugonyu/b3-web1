"""Flask가 제공하는 Vanilla client route 테스트."""

import unittest

from bookloop import create_app


class FlaskVanillaTest(unittest.TestCase):
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
        self.assertIn(b"/static/bookloop/python-favicon.svg", response.data)
        self.assertIn(b'href="#about"', response.data)
        self.assertIn(b'href="#connection"', response.data)
        self.assertIn(b'href="#preview"', response.data)
        self.assertIn(b'href="#presentations"', response.data)
        self.assertIn(b'href="#related"', response.data)
        self.assertIn(b"BookLoop Flask home", response.data)
        self.assertIn(b"Flask Vanilla :5000", response.data)
        self.assertIn(
            b"http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/",
            response.data,
        )
        self.assertIn(
            b"Flask Server &amp; API Connection \xe2\x80\x94 Port 5000",
            response.data,
        )
        self.assertIn(b"Check Flask Server", response.data)
        self.assertIn(
            b"VS Code Live Preview Check \xe2\x80\x94 Port 3000",
            response.data,
        )
        self.assertIn(
            b"http://127.0.0.1:3000/b3-web1/index.html?vscode-livepreview=true",
            response.data,
        )
        self.assertIn(b"Check Live Preview Server", response.data)
        self.assertIn(
            b"2 \xc2\xb7 Course &amp; Presentation Resources \xe2\x80\x94 Port 8080",
            response.data,
        )
        self.assertIn(
            b'id="presentations" class="status-card"',
            response.data,
        )
        self.assertIn(
            b"http://localhost:8080/pub/b3-web1/docs/presentations/",
            response.data,
        )
        self.assertIn(
            b"http://localhost:8080/pub/b3-web1/web1-schedule-summer-2026.html#schedule-title",
            response.data,
        )
        self.assertIn(
            b"http://localhost:8080/pub/b3-web1/app/backend/bookloop/README.html",
            response.data,
        )
        self.assertEqual(response.data.count(b'target="_blank"'), 4)
        self.assertEqual(response.data.count(b'rel="noopener noreferrer"'), 4)
        self.assertIn(b"http://127.0.0.1:5000/test/", response.data)
        response.close()

    def test_favicon_asset_is_available(self):
        response = self.client.get("/static/bookloop/python-favicon.svg")

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
        self.assertIn(b"Flask server reachable", response.data)
        self.assertIn(b"Flask server or API unavailable", response.data)
        self.assertIn(b"fetch(livePreviewUrl", response.data)
        self.assertIn(b'mode: "no-cors"', response.data)
        self.assertIn(b"Live Preview server reachable", response.data)
        self.assertIn(b"Live Preview server unavailable", response.data)
        response.close()

    def test_stylesheet_uses_la_bella_vita_theme_tokens(self):
        response = self.client.get("/vanilla/style.css")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"--lbv-cream: #faf9f5", response.data)
        self.assertIn(b"--lbv-tomato: #a83226", response.data)
        self.assertIn(b"--lbv-olive: #4a5a24", response.data)
        response.close()


if __name__ == "__main__":
    unittest.main()
