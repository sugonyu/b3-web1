"""BookLoop browser login, session 유지와 logout 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import User


class BrowserAuthenticationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            db.session.add(
                User(
                    username="tony",
                    email="tony@example.com",
                    password_hash=generate_password_hash("1111"),
                    general_area="Montreal",
                )
            )
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_contains_password_form_without_private_values(self):
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="username"', response.data)
        self.assertIn(b'name="password"', response.data)
        self.assertIn("👨 Tony · 👩 Mina · 🕵️ Alex".encode(), response.data)
        self.assertNotIn(b"tony@example.com", response.data)
        self.assertNotIn(b"scrypt:", response.data)

    def test_valid_login_starts_a_session_that_survives_a_new_request(self):
        response = self.client.post(
            "/login",
            data={"username": "tony", "password": "1111"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("tony 👨".encode(), response.data)

        refreshed_response = self.client.get("/")
        self.assertIn("tony 👨".encode(), refreshed_response.data)

    def test_invalid_password_returns_401_without_starting_a_session(self):
        response = self.client.post(
            "/login",
            data={"username": "tony", "password": "wrong"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid username or password.", response.data)
        home_response = self.client.get("/")
        self.assertIn(b"Sign in before requesting a book.", home_response.data)

    def test_login_rejects_external_next_redirect(self):
        response = self.client.post(
            "/login?next=https://example.com/unsafe",
            data={"username": "tony", "password": "1111"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")

    def test_logout_ends_session_and_protected_api_returns_401(self):
        self.client.post(
            "/login",
            data={"username": "tony", "password": "1111"},
        )

        logout_response = self.client.post("/logout", follow_redirects=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b"Sign in before requesting a book.", logout_response.data)

        protected_response = self.client.get("/api/requests/999")
        self.assertEqual(protected_response.status_code, 401)
        self.assertEqual(
            protected_response.get_json(),
            {"error": "authentication required"},
        )

    def test_register_creates_hashed_user_and_starts_session(self):
        response = self.client.post(
            "/register",
            data={
                "username": "new-reader",
                "email": "reader@example.com",
                "general_area": "NDG",
                "password": "1111",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("new-reader 👤".encode(), response.data)

        with self.app.app_context():
            user = User.query.filter_by(username="new-reader").one()
            self.assertNotEqual(user.password_hash, "1111")
            self.assertTrue(user.password_hash.startswith("scrypt:"))

    def test_register_rejects_duplicate_without_creating_another_user(self):
        response = self.client.post(
            "/register",
            data={
                "username": "tony",
                "email": "another@example.com",
                "general_area": "Verdun",
                "password": "1111",
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(b"Username or email is already registered.", response.data)
        with self.app.app_context():
            self.assertEqual(User.query.count(), 1)

    def test_register_requires_every_field(self):
        response = self.client.post(
            "/register",
            data={
                "username": "new-reader",
                "email": "",
                "general_area": "NDG",
                "password": "1111",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"All fields are required.", response.data)


if __name__ == "__main__":
    unittest.main()
