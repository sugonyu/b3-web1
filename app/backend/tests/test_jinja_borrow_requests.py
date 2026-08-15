"""Jinja 제품 화면의 borrowing-request와 Reporting 흐름 테스트.

Outline:
1. setUp()/tearDown() — memory SQLite와 Mina/Tony/Alex fixture
2. Books, login, Request detail/history 화면 테스트
3. owner decision, cancellation, return confirmation 테스트
4. authorized Report form과 실제 Report row 생성 테스트
5. unrelated user 권한 차단 테스트
"""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, Report, User


class JinjaBorrowRequestFlowTest(unittest.TestCase):
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
            mina = User(
                username="mina",
                email="mina@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            tony = User(
                username="tony",
                email="tony@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            alex = User(
                username="alex",
                email="alex@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            listing = BookListing(
                title="The Odyssey",
                author="Homer",
                owner=mina,
            )
            db.create_all()
            db.session.add_all([mina, tony, alex, listing])
            db.session.commit()
            self.listing_id = listing.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username):
        return self.client.post(
            "/login",
            data={"username": username, "password": "1111"},
        )

    def test_home_shows_seeded_book_and_request_action(self):
        self.login("tony")

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("tony 👨 · User #2".encode(), response.data)
        self.assertIn("tony 👨".encode(), response.data)
        self.assertIn(b"User #2", response.data)
        self.assertIn(b'class="data-table"', response.data)
        self.assertIn(b'aria-label="BookLoop product navigation"', response.data)
        self.assertIn(b'href="/requests/"', response.data)
        self.assertIn(b'href="/listing-requests/"', response.data)
        self.assertIn(b'aria-current="page"', response.data)
        self.assertIn("Owner · Area".encode(), response.data)
        self.assertIn(b"The Odyssey", response.data)
        self.assertIn("🌊 The Odyssey".encode(), response.data)
        self.assertIn("mina 👩".encode(), response.data)
        self.assertIn(b"Homer", response.data)
        self.assertIn(b"Request", response.data)
        self.assertIn("🙋 Sent requests (0)".encode(), response.data)
        self.assertIn("📬 Received requests (0)".encode(), response.data)
        self.assertNotIn(b"mina@example.com", response.data)

    def test_home_distinguishes_my_book_from_community_book(self):
        self.login("mina")

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"own-listing-row", response.data)
        self.assertIn(b"Your book", response.data)
        self.assertIn(b">You</strong>", response.data)

    def test_unauthenticated_request_redirects_to_login(self):
        response = self.client.post(
            f"/listings/{self.listing_id}/request",
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")
        with self.app.app_context():
            self.assertEqual(BorrowRequest.query.count(), 0)

    def test_logged_out_request_read_returns_to_same_page_after_login(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")

        protected_response = self.client.get("/requests/1")

        self.assertEqual(protected_response.status_code, 302)
        self.assertEqual(
            protected_response.headers["Location"],
            "/login?next=/requests/1",
        )

        login_page = self.client.get(protected_response.headers["Location"])
        self.assertIn(b"After login, return to", login_page.data)
        self.assertIn(b'value="/requests/1"', login_page.data)

        login_response = self.client.post(
            "/login?next=/requests/1",
            data={
                "username": "tony",
                "password": "1111",
                "next": "/requests/1",
            },
        )
        self.assertEqual(login_response.status_code, 302)
        self.assertEqual(login_response.headers["Location"], "/requests/1")

        result_response = self.client.get(login_response.headers["Location"])
        self.assertEqual(result_response.status_code, 200)
        self.assertIn(b"Request #1", result_response.data)

    def test_borrower_creates_and_reopens_pending_request(self):
        self.login("tony")

        create_response = self.client.post(
            f"/listings/{self.listing_id}/request",
        )

        self.assertEqual(create_response.status_code, 302)
        self.assertRegex(create_response.headers["Location"], r"/requests/\d+$")

        result_response = self.client.get(create_response.headers["Location"])
        self.assertEqual(result_response.status_code, 200)
        self.assertIn(b"Request #1", result_response.data)
        self.assertIn(b"Pending", result_response.data)
        self.assertIn(b"status-pending", result_response.data)
        self.assertIn(b"The Odyssey", result_response.data)
        self.assertIn("🌊 The Odyssey".encode(), result_response.data)
        self.assertIn(b"is currently Pending", result_response.data)
        self.assertNotIn(b"tony@example.com", result_response.data)
        self.assertNotIn(b"mina@example.com", result_response.data)
        self.assertNotIn(b"Approved contact exchange", result_response.data)

        # 새 GET이 같은 SQLite row를 읽으며 두 번째 request를 만들지 않는다.
        reopened_response = self.client.get("/requests/1")
        self.assertEqual(reopened_response.status_code, 200)
        with self.app.app_context():
            self.assertEqual(BorrowRequest.query.count(), 1)

    def test_owner_cannot_request_own_listing(self):
        self.login("mina")

        response = self.client.post(
            f"/listings/{self.listing_id}/request",
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(b"This is your book", response.data)
        self.assertIn(b"You cannot request a book that you own.", response.data)
        self.assertIn(b"<strong>409</strong>", response.data)

    def test_duplicate_active_request_is_blocked(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.post(
            f"/listings/{self.listing_id}/request",
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(b"Request already exists", response.data)
        self.assertIn(b"You already have an active request for this book.", response.data)
        self.assertIn(b"<strong>409</strong>", response.data)
        self.assertIn(b'href="/requests/1"', response.data)
        self.assertIn(b"View Request #1", response.data)
        with self.app.app_context():
            self.assertEqual(BorrowRequest.query.count(), 1)

    def test_home_disables_request_button_for_active_request(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Requested", response.data)
        self.assertRegex(response.data.decode(), r"<button[^>]+disabled[^>]*>\s*Requested")

    def test_unrelated_user_cannot_open_request_result(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("alex")

        response = self.client.get("/requests/1")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"<strong>403</strong>", response.data)
        self.assertIn(b"Access denied", response.data)
        self.assertIn(b"Only the borrower or book owner can view this request.", response.data)

    def test_missing_request_result_shows_404_code_and_message(self):
        self.login("tony")

        response = self.client.get("/requests/999")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<strong>404</strong>", response.data)
        self.assertIn(b"Request not found", response.data)
        self.assertIn(b"This borrowing request does not exist.", response.data)

    def test_borrower_history_shows_only_current_users_requests(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.get("/requests/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My borrowing requests", response.data)
        self.assertIn(b'class="data-table request-table"', response.data)
        self.assertIn(b"Sent requests", response.data)
        self.assertIn(b"Received requests", response.data)
        self.assertIn("tony 👨 · User #2".encode(), response.data)
        self.assertIn(b"The Odyssey", response.data)
        self.assertIn("🌊 The Odyssey".encode(), response.data)
        self.assertIn(b'data-label="Request"', response.data)
        self.assertIn(b'href="/requests/1"', response.data)
        self.assertNotIn(b'<th scope="col">Decision</th>', response.data)
        self.assertNotIn(b"tony@example.com", response.data)

    def test_borrower_history_requires_login(self):
        response = self.client.get("/requests/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login?next=/requests/")

    def test_listing_owner_history_shows_requests_for_owned_books(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("mina")

        response = self.client.get("/listing-requests/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Requests for my books", response.data)
        self.assertIn(b'class="data-table request-table"', response.data)
        self.assertIn("mina 👩 · User #1".encode(), response.data)
        self.assertIn("mina 👩".encode(), response.data)
        self.assertIn(b"The Odyssey", response.data)
        self.assertIn("🌊 The Odyssey".encode(), response.data)
        self.assertIn("tony 👨".encode(), response.data)
        self.assertIn(b'data-label="Request"', response.data)
        self.assertIn(b'href="/requests/1"', response.data)
        self.assertIn(b'<th scope="col">Decision</th>', response.data)
        self.assertIn(b"Review &amp; decide", response.data)
        self.assertNotIn(b"decision-approve", response.data)
        self.assertNotIn(b"tony@example.com", response.data)

    def test_listing_owner_reviews_decision_context_before_deciding(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("mina")

        response = self.client.get("/requests/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mina's Decision Context", response.data)
        self.assertIn(b"Requested at", response.data)
        self.assertIn(b"Member since", response.data)
        self.assertIn(b"Completed exchanges", response.data)
        self.assertIn(b"Active requests", response.data)
        self.assertIn(b"First-time borrower", response.data)
        self.assertIn(b"Decision guide", response.data)
        self.assertIn(b"Approve only when you can proceed", response.data)
        self.assertIn(b"Admin review remains separate", response.data)
        self.assertIn(b"No active Admin review notice", response.data)
        self.assertIn(b"Private contact details", response.data)
        self.assertIn(b"Approve", response.data)
        self.assertIn(b"Reject", response.data)
        self.assertNotIn(b"tony@example.com", response.data)

    def test_borrower_does_not_see_owner_decision_context_or_buttons(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.get("/requests/1")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Mina's Decision Context", response.data)
        self.assertNotIn(b"decision-approve", response.data)
        self.assertNotIn(b"decision-reject", response.data)
        self.assertNotIn(b"Decision guide", response.data)
        self.assertNotIn(b"Admin review notice", response.data)

    def test_open_report_does_not_notify_reported_owner_before_admin_triage(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post(
            "/requests/1/report",
            data={
                "category": "no_show",
                "details": "The arranged exchange did not happen.",
            },
        )
        self.client.post("/logout")
        self.login("mina")

        response = self.client.get("/requests/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No active Admin review notice", response.data)
        self.assertNotIn(b"Admin review notice</h3>", response.data)
        self.assertNotIn(b"The arranged exchange did not happen.", response.data)

    def test_reported_owner_sees_notice_after_admin_starts_review(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post(
            "/requests/1/report",
            data={
                "category": "no_show",
                "details": "The arranged exchange did not happen.",
            },
        )
        with self.app.app_context():
            report = Report.query.one()
            report.status = "under_review"
            db.session.commit()
        self.client.post("/logout")
        self.login("mina")

        response = self.client.get("/requests/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin review notice", response.data)
        self.assertIn(b"1 Admin review is in progress for this exchange", response.data)
        self.assertIn(b"Report details are visible only to Admin", response.data)
        self.assertIn(b"Do not contact the other member about the report", response.data)
        self.assertIn(b"does not automatically approve or reject", response.data)
        self.assertNotIn(b"The arranged exchange did not happen.", response.data)
        self.assertNotIn(b"tony@example.com", response.data)

    def test_request_parties_see_report_form(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        borrower_response = self.client.get("/requests/1")
        self.assertEqual(borrower_response.status_code, 200)
        self.assertIn(b"Report this exchange", borrower_response.data)
        self.assertIn(b"/requests/1/report", borrower_response.data)

        self.client.post("/logout")
        self.login("mina")
        owner_response = self.client.get("/requests/1")
        self.assertIn(b"Report this exchange", owner_response.data)

    def test_report_form_creates_row_and_redirects_with_feedback(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.post(
            "/requests/1/report",
            data={
                "category": "no_show",
                "details": "The arranged exchange did not happen.",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Report #1 was submitted for review.", response.data)
        with self.app.app_context():
            report = Report.query.one()
            self.assertEqual(report.reporter.username, "tony")
            self.assertEqual(report.reported_user.username, "mina")

    def test_reporter_can_track_own_report_status(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post(
            "/requests/1/report",
            data={
                "category": "no_show",
                "details": "The arranged exchange did not happen.",
            },
        )
        with self.app.app_context():
            report = Report.query.one()
            report.status = "under_review"
            db.session.commit()

        reporter_response = self.client.get("/reports/")
        self.assertEqual(reporter_response.status_code, 200)
        self.assertIn(b"My reports", reporter_response.data)
        self.assertIn(b"The Odyssey", reporter_response.data)
        self.assertIn(b"mina", reporter_response.data)
        self.assertIn(b"Under Review", reporter_response.data)
        self.assertIn(b'href="/reports/1"', reporter_response.data)

        detail_response = self.client.get("/reports/1")
        self.assertEqual(detail_response.status_code, 200)
        self.assertIn(b"Report detail", detail_response.data)
        self.assertIn(b"The arranged exchange did not happen.", detail_response.data)
        self.assertIn(b"Under Review", detail_response.data)

        self.client.post("/logout")
        self.login("mina")
        unrelated_response = self.client.get("/reports/")
        self.assertEqual(unrelated_response.status_code, 200)
        self.assertIn(b"You have not submitted a report.", unrelated_response.data)
        self.assertNotIn(b"The Odyssey", unrelated_response.data)
        self.assertEqual(self.client.get("/reports/1").status_code, 404)

    def test_unrelated_user_cannot_submit_report(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("alex")

        response = self.client.post(
            "/requests/1/report",
            data={
                "category": "other",
                "details": "This user is not part of the exchange.",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Only the borrower or book owner can report this request.", response.data)
        with self.app.app_context():
            self.assertEqual(Report.query.count(), 0)

    def test_borrower_cancels_pending_request_before_owner_decision(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        pending_page = self.client.get("/requests/")
        self.assertIn(b"Cancel request", pending_page.data)

        response = self.client.post(
            "/requests/1/cancel",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Request #1 was cancelled.", response.data)
        self.assertIn(b"Cancelled", response.data)
        self.assertIn(b"status-cancelled", response.data)
        self.assertNotIn(b"Cancel request", response.data)
        with self.app.app_context():
            self.assertEqual(db.session.get(BorrowRequest, 1).status, "cancelled")
            self.assertTrue(db.session.get(BookListing, self.listing_id).availability)

    def test_listing_owner_cannot_cancel_borrowers_request(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("mina")

        response = self.client.post("/requests/1/cancel")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Cancellation not allowed", response.data)
        with self.app.app_context():
            self.assertEqual(db.session.get(BorrowRequest, 1).status, "pending")

    def test_borrower_cannot_cancel_after_request_is_approved(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("mina")
        self.client.post("/requests/1/decision", data={"status": "approved"})
        self.client.post("/logout")
        self.login("tony")

        response = self.client.post("/requests/1/cancel")

        self.assertEqual(response.status_code, 409)
        self.assertIn(b"Request cannot be cancelled", response.data)
        with self.app.app_context():
            self.assertEqual(db.session.get(BorrowRequest, 1).status, "approved")

    def test_home_request_counts_follow_the_signed_in_users_role(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        borrower_home = self.client.get("/")
        self.assertIn("🙋 Sent requests (1)".encode(), borrower_home.data)
        self.assertIn("📬 Received requests (0)".encode(), borrower_home.data)

        self.client.post("/logout")
        self.login("mina")

        owner_home = self.client.get("/")
        self.assertIn("🙋 Sent requests (0)".encode(), owner_home.data)
        self.assertIn("📬 Received requests (1)".encode(), owner_home.data)

    def test_unrelated_user_sees_empty_owner_history(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("alex")

        response = self.client.get("/listing-requests/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No one has requested one of your books yet.", response.data)
        self.assertNotIn(b"The Odyssey", response.data)
        self.assertNotIn(b"Request #1", response.data)

    def test_listing_owner_approves_request_and_borrower_sees_result(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("mina")

        decision_response = self.client.post(
            "/requests/1/decision",
            data={"status": "approved"},
            follow_redirects=True,
        )

        self.assertEqual(decision_response.status_code, 200)
        self.assertIn(b"Decision saved", decision_response.data)
        self.assertIn(b"Request #1 was approved.", decision_response.data)
        self.assertIn(b"Approved", decision_response.data)
        self.assertIn(b"status-approved", decision_response.data)
        self.assertNotIn(b"decision-approve", decision_response.data)

        self.client.post("/logout")
        self.login("tony")
        borrower_response = self.client.get("/requests/")
        self.assertIn(b"Approved", borrower_response.data)

        borrower_detail = self.client.get("/requests/1")
        self.assertIn(b"Approved contact exchange", borrower_detail.data)
        self.assertIn(b"Contact mina", borrower_detail.data)
        self.assertIn(b"mina@example.com", borrower_detail.data)
        self.assertNotIn(b"tony@example.com", borrower_detail.data)

        self.client.post("/logout")
        self.login("mina")
        owner_detail = self.client.get("/requests/1")
        self.assertIn(b"Contact tony", owner_detail.data)
        self.assertIn(b"tony@example.com", owner_detail.data)
        self.assertNotIn(b"mina@example.com", owner_detail.data)

        with self.app.app_context():
            borrow_request = db.session.get(BorrowRequest, 1)
            listing = db.session.get(BookListing, self.listing_id)
            self.assertEqual(borrow_request.status, "approved")
            self.assertFalse(listing.availability)

    def test_listing_owner_rejects_request_and_listing_stays_available(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("mina")

        response = self.client.post(
            "/requests/1/decision",
            data={"status": "rejected"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Request #1 was rejected.", response.data)
        self.assertIn(b"Rejected", response.data)
        self.assertIn(b"status-rejected", response.data)
        with self.app.app_context():
            listing = db.session.get(BookListing, self.listing_id)
            self.assertTrue(listing.availability)

    def test_non_owner_cannot_decide_request_even_with_owner_form(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.post(
            "/requests/1/decision",
            data={"status": "approved"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Decision not allowed", response.data)
        with self.app.app_context():
            self.assertEqual(db.session.get(BorrowRequest, 1).status, "pending")


if __name__ == "__main__":
    unittest.main()
