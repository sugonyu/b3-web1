"""개발 전용 read-only database inspector의 접근과 노출 경계 테스트."""

import unittest
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, Report, User


class DeveloperDatabaseInspectorTest(unittest.TestCase):
    def create_test_app(
        self,
        inspector_enabled=False,
        debug=False,
        lan_enabled=False,
    ):
        """각 테스트가 독립적인 in-memory SQLite app을 사용하게 한다."""
        return create_app(
            {
                "TESTING": True,
                "DEBUG": debug,
                "SECRET_KEY": "test-secret",
                "ENABLE_DEV_DB_INSPECTOR": inspector_enabled,
                "ENABLE_LAN_DEV_DB_INSPECTOR": lan_enabled,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )

    def seed_database(self, app):
        """화면과 관계 ID를 검증할 최소 User, listing, request를 만든다."""
        with app.app_context():
            db.create_all()
            owner = User(
                username="mina",
                email="mina.private@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            borrower = User(
                username="tony",
                email="tony.private@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="NDG",
                is_admin=True,
            )
            listing = BookListing(
                title="The Odyssey",
                author="Homer",
                owner=owner,
            )
            borrow_request = BorrowRequest(
                listing=listing,
                borrower=borrower,
            )
            report = Report(
                reporter=borrower,
                reported_user=owner,
                borrow_request=borrow_request,
                category="no_show",
                details="The reported user did not arrive at the agreed place.",
                status="under_review",
            )
            db.session.add_all([owner, borrower, listing, borrow_request, report])
            db.session.commit()

    def login(self, client, username):
        """LAN 권한 테스트를 위한 실제 Flask-Login session을 만든다."""

        return client.post(
            "/login",
            data={"username": username, "password": "1111"},
        )

    def test_inspector_is_hidden_when_explicit_setting_is_disabled(self):
        app = self.create_test_app(inspector_enabled=False, debug=True)

        response = app.test_client().get("/dev/db")

        self.assertEqual(response.status_code, 404)
        response.close()

    def test_inspector_is_hidden_outside_debug_mode(self):
        app = self.create_test_app(inspector_enabled=True, debug=False)

        response = app.test_client().get("/dev/db")

        self.assertEqual(response.status_code, 404)
        response.close()

    def test_lan_guest_is_redirected_to_login(self):
        app = self.create_test_app(
            inspector_enabled=True,
            debug=False,
            lan_enabled=True,
        )
        self.seed_database(app)

        response = app.test_client().get(
            "/dev/db/",
            environ_base={"REMOTE_ADDR": "192.168.1.3"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login?next=/dev/db/")
        response.close()

    def test_lan_non_admin_receives_forbidden(self):
        app = self.create_test_app(
            inspector_enabled=True,
            debug=False,
            lan_enabled=True,
        )
        self.seed_database(app)
        client = app.test_client()
        self.login(client, "mina")

        response = client.get(
            "/dev/db/",
            environ_base={"REMOTE_ADDR": "192.168.1.3"},
        )

        self.assertEqual(response.status_code, 403)
        response.close()

    def test_lan_admin_can_open_inspector(self):
        app = self.create_test_app(
            inspector_enabled=True,
            debug=False,
            lan_enabled=True,
        )
        self.seed_database(app)
        client = app.test_client()
        self.login(client, "tony")

        response = client.get(
            "/dev/db/",
            environ_base={"REMOTE_ADDR": "100.115.92.193"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Borrow Requests", response.data)
        response.close()

    def test_lan_public_source_is_hidden_even_for_admin(self):
        app = self.create_test_app(
            inspector_enabled=True,
            debug=False,
            lan_enabled=True,
        )
        self.seed_database(app)
        client = app.test_client()
        self.login(client, "tony")

        response = client.get(
            "/dev/db/",
            environ_base={"REMOTE_ADDR": "8.8.8.8"},
        )

        self.assertEqual(response.status_code, 404)
        response.close()

    def test_inspector_lists_safe_fields_for_four_models(self):
        app = self.create_test_app(inspector_enabled=True, debug=True)
        self.seed_database(app)

        response = app.test_client().get("/dev/db")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Users", response.data)
        self.assertIn(b"Book Listings", response.data)
        self.assertIn(b"Borrow Requests", response.data)
        self.assertIn(b"Reports", response.data)
        self.assertIn(b'href="/dev/db/"', response.data)
        self.assertIn(b"Reload", response.data)
        self.assertIn(b"Server:", response.data)
        self.assertIn(b"localhost", response.data)
        self.assertIn(b"/static/bookloop/python-favicon.svg", response.data)
        self.assertIn(b"Course &amp; Presentation Resources", response.data)
        self.assertIn(b"python3 bl_cli.py reset-demo-requests", response.data)
        self.assertIn(b"Users and Book Listings are preserved", response.data)
        self.assertIn(b"web1-schedule-summer-2026.html", response.data)
        self.assertIn(b"bookloop/README.html", response.data)
        self.assertIn(b"docs/presentations/", response.data)
        self.assertEqual(response.data.count(b'target="_blank"'), 3)
        self.assertIn(b"mina", response.data)
        self.assertIn(b"tony", response.data)
        self.assertIn(b"The Odyssey", response.data)
        self.assertIn(b"no_show", response.data)
        self.assertIn(b"The reported user did not arrive", response.data)
        self.assertIn(b"under_review", response.data)
        self.assertIn(b"Reporter", response.data)
        self.assertIn(b"Reported user", response.data)
        self.assertIn(b"pending", response.data)
        self.assertIn(b'aria-label="Borrow request status legend"', response.data)
        self.assertIn(b'class="status-pill status-pending"', response.data)
        self.assertIn(b'class="status-pill status-approved"', response.data)
        self.assertIn(b'class="status-pill status-rejected"', response.data)
        self.assertIn(b'class="status-pill status-cancelled"', response.data)
        self.assertIn(b'class="status-pill status-returned"', response.data)
        self.assertIn(b'class="status-pill status-under_review"', response.data)
        self.assertIn(b"<th>ID</th><th>Status</th><th>Listing</th><th>Owner</th><th>Borrower</th><th>Created</th>", response.data)
        self.assertNotIn(b"Created (Toronto)", response.data)
        self.assertIn(b"<th>ID</th><th>Reporter</th><th>Reported user</th><th>Category</th><th>Details</th><th>Status</th><th>Created</th>", response.data)
        self.assertIn(b"<th>ID</th><th>Title</th><th>Author</th><th>Available</th><th>Owner</th><th>Created</th>", response.data)
        self.assertIn(b"<code>#1</code> \xc2\xb7 The Odyssey", response.data)
        self.assertIn(b"<code>#1</code> \xc2\xb7 mina", response.data)
        self.assertIn(b"<code>#2</code> \xc2\xb7 tony", response.data)
        self.assertIn(b"<code>#1</code> \xc2\xb7 mina</td>", response.data)

        # 자주 확인하는 거래 흐름부터 위에 보이도록 model section 순서를 고정한다.
        requests_position = response.data.index(b'id="requests-heading"')
        listings_position = response.data.index(b'id="listings-heading"')
        users_position = response.data.index(b'id="users-heading"')
        self.assertLess(requests_position, listings_position)
        self.assertLess(listings_position, users_position)

        # 실제 private 값이 HTML 어디에도 섞이지 않았는지 값 자체로 검사한다.
        self.assertNotIn(b"mina.private@example.com", response.data)
        self.assertNotIn(b"tony.private@example.com", response.data)
        self.assertNotIn(b"mina.private@example.com", response.data)
        self.assertNotIn(b"never-render-this-hash", response.data)
        self.assertNotIn(b"another-private-hash", response.data)
        response.close()

    def test_inspector_shows_newest_rows_first_with_toronto_time(self):
        app = self.create_test_app(inspector_enabled=True, debug=True)
        self.seed_database(app)

        with app.app_context():
            listing = BookListing.query.one()
            borrower = User.query.filter_by(username="tony").one()
            first_request = BorrowRequest.query.one()
            first_request.created_at = datetime(
                2026, 8, 5, 16, 0, tzinfo=timezone.utc
            )
            newest_request = BorrowRequest(
                listing=listing,
                borrower=borrower,
                created_at=datetime(2026, 8, 6, 21, 30, tzinfo=timezone.utc),
            )
            db.session.add(newest_request)
            db.session.commit()

        response = app.test_client().get("/dev/db")
        html = response.get_data(as_text=True)

        requests_table = html.split('<section aria-labelledby="requests-heading">', 1)[1]
        requests_table = requests_table.split('<section aria-labelledby="listings-heading">', 1)[0]
        self.assertLess(requests_table.index("<td>2</td>"), requests_table.index("<td>1</td>"))
        self.assertIn("Aug 6 · 5:30 PM", requests_table)
        self.assertIn("Aug 5 · 12:00 PM", requests_table)
        self.assertIn("Aug 12 ·", html)
        response.close()

    def test_inspector_get_does_not_change_database_rows(self):
        app = self.create_test_app(inspector_enabled=True, debug=True)
        self.seed_database(app)

        with app.app_context():
            counts_before = (
                User.query.count(),
                BookListing.query.count(),
                BorrowRequest.query.count(),
            )

        response = app.test_client().get("/dev/db")
        response.close()

        with app.app_context():
            counts_after = (
                User.query.count(),
                BookListing.query.count(),
                BorrowRequest.query.count(),
            )

        self.assertEqual(counts_after, counts_before)


if __name__ == "__main__":
    unittest.main()
