"""제품 Admin View의 role 경계와 privacy-safe queue 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, Report, User
from bookloop.services.admin_dashboard import (
    AdminDashboardServiceError,
    get_admin_dashboard_service,
    update_admin_report_status_service,
)


class AdminDashboardTest(unittest.TestCase):
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
            tony = User(
                username="tony",
                email="tony@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
                is_admin=True,
            )
            mina = User(
                username="mina",
                email="mina@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            alex = User(
                username="alex",
                email="alex@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            listing = BookListing(title="The Vegetarian", author="Han Kang", owner=mina)
            borrow_request = BorrowRequest(listing=listing, borrower=tony)
            report = Report(
                reporter=tony,
                reported_user=mina,
                borrow_request=borrow_request,
                category="no_show",
                details="Private moderation details must not appear in the queue.",
            )
            db.session.add_all([tony, mina, alex, listing, borrow_request, report])
            db.session.commit()
            self.tony_id = tony.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username):
        return self.client.post("/login", data={"username": username, "password": "1111"})

    def test_guest_is_redirected_to_login_with_admin_return_path(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login?next=/admin/")

    def test_member_receives_403_without_report_data(self):
        self.login("mina")

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Admin access denied", response.data)
        self.assertNotIn(b"no_show", response.data)
        self.assertNotIn(b"example.com", response.data)

    def test_admin_sees_read_only_privacy_safe_report_queue(self):
        self.login("tony")

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin dashboard", response.data)
        self.assertIn(b"System overview", response.data)
        self.assertIn(b"Book sharing overview", response.data)
        self.assertIn(b"Report review queue", response.data)
        status_position = response.data.index(b"Borrow request status")
        overview_position = response.data.index(b"Book sharing overview")
        self.assertLess(status_position, overview_position)
        self.assertIn(b"Member contact directory", response.data)
        self.assertIn(b"tony@example.com", response.data)
        self.assertIn(b"mina@example.com", response.data)
        self.assertIn(b"alex@example.com", response.data)
        self.assertIn(b"The Vegetarian", response.data)
        self.assertIn(b"mina", response.data)
        self.assertIn(b"Current borrower", response.data)
        self.assertIn(b">Status<", response.data)
        self.assertIn(b"Pending", response.data)
        self.assertNotIn(b"Current state", response.data)
        self.assertIn(b"Active requests", response.data)
        self.assertIn(b"Reports &amp; moderation", response.data)
        self.assertIn(b"Report review queue", response.data)
        report_position = response.data.index(b"Report review queue")
        status_position = response.data.index(b"Borrow request status")
        self.assertLess(report_position, status_position)
        self.assertIn(b">Reporter<", response.data)
        self.assertIn("tony 👨".encode(), response.data)
        self.assertIn(b"No Show", response.data)
        self.assertIn(b"#1", response.data)
        self.assertIn(b"Open", response.data)
        self.assertIn(b"Private moderation details must not appear in the queue.", response.data)
        self.assertNotIn(b"password", response.data.lower())
        # 공통 헤더의 logout form은 허용하지만 queue 안의 moderation form은 금지한다.
        self.assertNotIn(b'action="/admin/reports/', response.data.lower())

    def test_admin_can_review_report_and_change_status(self):
        self.login("tony")

        response = self.client.get("/admin/reports/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Report #1", response.data)
        self.assertIn(b"Details", response.data)
        self.assertIn(b"Private moderation details must not appear in the queue.", response.data)
        self.assertIn(b"mina@example.com", response.data)
        self.assertIn(b"Review decision", response.data)
        self.assertIn(b"Automatic email notifications are not part of the beta", response.data)

        update_response = self.client.post(
            "/admin/reports/1/status",
            data={"status": "under_review"},
        )

        self.assertEqual(update_response.status_code, 302)
        self.assertEqual(update_response.headers["Location"], "/admin/reports/1")
        with self.app.app_context():
            self.assertEqual(db.session.get(Report, 1).status, "under_review")

    def test_member_cannot_change_report_status(self):
        self.login("mina")

        response = self.client.post(
            "/admin/reports/1/status",
            data={"status": "resolved"},
        )

        self.assertEqual(response.status_code, 403)

    def test_invalid_report_status_is_rejected(self):
        with self.app.app_context():
            with self.assertRaisesRegex(AdminDashboardServiceError, "invalid report status"):
                update_admin_report_status_service(self.tony_id, 1, "archived")

    def test_member_cannot_open_report_detail(self):
        self.login("mina")

        response = self.client.get("/admin/reports/1")

        self.assertEqual(response.status_code, 403)
        self.assertNotIn(b"Private moderation details", response.data)

    def test_missing_report_detail_is_404_for_admin(self):
        self.login("tony")

        response = self.client.get("/admin/reports/999")

        self.assertEqual(response.status_code, 404)

    def test_admin_navigation_is_visible_only_to_admin(self):
        self.login("tony")
        admin_home = self.client.get("/")
        self.assertIn(b'href="/admin/"', admin_home.data)
        self.assertIn(b"Received reports", admin_home.data)
        self.assertNotIn(b"My reports", admin_home.data)

        self.client.post("/logout")
        self.login("alex")
        member_home = self.client.get("/")
        self.assertNotIn(b'href="/admin/"', member_home.data)

    def test_dashboard_aggregates_system_book_and_status_counts(self):
        with self.app.app_context():
            context = get_admin_dashboard_service(self.tony_id)

            self.assertEqual(
                context["system_counts"],
                {
                    "users": 3,
                    "listings": 1,
                    "available_listings": 1,
                    "active_requests": 1,
                    "open_reports": 1,
                },
            )
            self.assertEqual(context["request_status_counts"]["pending"], 1)
            self.assertEqual(context["report_status_counts"]["open"], 1)
            self.assertEqual(context["listing_rows"][0]["request_count"], 1)
            self.assertEqual(context["listing_rows"][0]["active_request_count"], 1)
            self.assertEqual(context["listing_rows"][0]["latest_request_status"], "pending")
            self.assertEqual(
                context["listing_rows"][0]["current_borrower"].username,
                "tony",
            )


if __name__ == "__main__":
    unittest.main()
