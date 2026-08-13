"""개발 전용 View-as-user 도구의 설정, allowlist와 session 경계 테스트."""

import unittest

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import User


class DeveloperUserSwitcherTest(unittest.TestCase):
    def create_test_app(self, switcher_enabled=False, debug=False, lan_switcher=False):
        return create_app(
            {
                "TESTING": True,
                "DEBUG": debug,
                "ENABLE_DEV_USER_SWITCHER": switcher_enabled,
                "ENABLE_LAN_DEV_USER_SWITCHER": lan_switcher,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )

    def seed_users(self, app):
        with app.app_context():
            db.create_all()
            db.session.add_all(
                [
                    User(username="tony", email="tony@example.com", password_hash="hash", general_area="Montreal"),
                    User(username="mina", email="mina@example.com", password_hash="hash", general_area="Montreal"),
                    User(username="alex", email="alex@example.com", password_hash="hash", general_area="Laval"),
                ]
            )
            db.session.commit()

    def test_switcher_is_hidden_when_setting_is_disabled(self):
        app = self.create_test_app(switcher_enabled=False, debug=True)
        self.seed_users(app)

        response = app.test_client().post("/dev/user-view/tony")

        self.assertEqual(response.status_code, 404)

    def test_switcher_is_hidden_outside_debug_mode(self):
        app = self.create_test_app(switcher_enabled=True, debug=False)
        self.seed_users(app)

        response = app.test_client().post("/dev/user-view/tony")

        self.assertEqual(response.status_code, 404)

    def test_allowed_seed_user_switches_session_and_renders_dev_banner(self):
        app = self.create_test_app(switcher_enabled=True, debug=True)
        self.seed_users(app)
        client = app.test_client()

        response = client.post("/dev/user-view/mina", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("mina 👩".encode(), response.data)
        self.assertIn("DEV · Viewing as mina 👩".encode(), response.data)
        self.assertIn(b'action="/dev/user-view/tony"', response.data)
        self.assertIn(b'id="dev-user-switcher"', response.data)
        self.assertIn(b'id="dev-user-switcher-toggle"', response.data)
        self.assertIn(b'aria-expanded="false"', response.data)
        self.assertIn(b"dev-user-switcher.js", response.data)
        self.assertNotIn(b"mina@example.com", response.data)

    def test_lan_opt_in_allows_switcher_without_debug(self):
        app = self.create_test_app(
            switcher_enabled=True,
            debug=False,
            lan_switcher=True,
        )
        self.seed_users(app)

        response = app.test_client().post(
            "/dev/user-view/mina",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("DEV · Viewing as mina 👩".encode(), response.data)

    def test_unknown_or_non_seed_user_is_rejected(self):
        app = self.create_test_app(switcher_enabled=True, debug=True)
        self.seed_users(app)
        client = app.test_client()

        self.assertEqual(client.post("/dev/user-view/jiyun").status_code, 404)
        self.assertEqual(client.post("/dev/user-view/unknown").status_code, 404)


if __name__ == "__main__":
    unittest.main()
