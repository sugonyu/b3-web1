"""D2 Jinja 제품 화면의 최소 borrowing-request 흐름 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User


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
        self.assertIn(b"Signed in as tony", response.data)
        self.assertIn(b"User #2", response.data)
        self.assertIn(b"The Odyssey", response.data)
        self.assertIn(b"Homer", response.data)
        self.assertIn(b"Request this book", response.data)
        self.assertNotIn(b"mina@example.com", response.data)

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
        self.assertIn(b"The Odyssey", result_response.data)
        self.assertIn(b"saved successfully", result_response.data)
        self.assertNotIn(b"tony@example.com", result_response.data)

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
        self.assertIn(b"owner cannot borrow own listing", response.data)

    def test_duplicate_active_request_is_blocked(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")

        response = self.client.post(
            f"/listings/{self.listing_id}/request",
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(b"active borrow request already exists", response.data)
        self.assertIn(b"BorrowRequest #1", response.data)
        self.assertIn(b'href="/requests/1"', response.data)
        self.assertIn(b"View Request #1", response.data)
        with self.app.app_context():
            self.assertEqual(BorrowRequest.query.count(), 1)

    def test_unrelated_user_cannot_open_request_result(self):
        self.login("tony")
        self.client.post(f"/listings/{self.listing_id}/request")
        self.client.post("/logout")
        self.login("alex")

        response = self.client.get("/requests/1")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"<strong>403</strong>", response.data)
        self.assertIn(b"borrow request access forbidden", response.data)

    def test_missing_request_result_shows_404_code_and_message(self):
        self.login("tony")

        response = self.client.get("/requests/999")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<strong>404</strong>", response.data)
        self.assertIn(b"borrow request not found", response.data)


if __name__ == "__main__":
    unittest.main()
