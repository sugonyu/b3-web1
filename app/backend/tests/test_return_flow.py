"""W3-14 borrower 시작 → owner 확인의 two-step 반납 흐름 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User
from bookloop.services.borrow_requests import (
    BorrowRequestServiceError,
    confirm_book_return_service,
    get_approved_contact_context_service,
    request_return_confirmation_service,
)


class ReturnFlowTest(unittest.TestCase):
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
            listing = BookListing(
                title="The Odyssey",
                author="Homer",
                owner=tony,
                availability=False,
            )
            borrow_request = BorrowRequest(
                listing=listing,
                borrower=mina,
                status="approved",
            )
            db.session.add_all([tony, mina, alex, listing, borrow_request])
            db.session.commit()
            self.tony_id = tony.id
            self.mina_id = mina.id
            self.alex_id = alex.id
            self.request_id = borrow_request.id
            self.listing_id = listing.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username):
        return self.client.post("/login", data={"username": username, "password": "1111"})

    def test_service_requires_borrower_then_owner_and_reopens_listing(self):
        with self.app.app_context():
            pending_confirmation = request_return_confirmation_service(
                self.request_id,
                self.mina_id,
            )
            self.assertEqual(pending_confirmation.status, "return_pending")
            self.assertFalse(pending_confirmation.listing.availability)
            self.assertEqual(
                get_approved_contact_context_service(pending_confirmation, self.mina_id)["email"],
                "tony@example.com",
            )

            returned = confirm_book_return_service(self.request_id, self.tony_id)
            self.assertEqual(returned.status, "returned")
            self.assertTrue(returned.listing.availability)
            self.assertIsNone(get_approved_contact_context_service(returned, self.mina_id))

    def test_wrong_actor_and_wrong_order_are_blocked(self):
        with self.app.app_context():
            with self.assertRaises(BorrowRequestServiceError) as unrelated:
                request_return_confirmation_service(self.request_id, self.alex_id)
            self.assertEqual(unrelated.exception.status_code, 403)

            with self.assertRaises(BorrowRequestServiceError) as too_early:
                confirm_book_return_service(self.request_id, self.tony_id)
            self.assertEqual(too_early.exception.status_code, 409)

    def test_jinja_flow_shows_role_specific_actions(self):
        self.login("mina")
        borrower_detail = self.client.get(f"/requests/{self.request_id}")
        self.assertIn(b"I returned this book", borrower_detail.data)

        start_return = self.client.post(
            f"/requests/{self.request_id}/return",
            follow_redirects=True,
        )
        self.assertEqual(start_return.status_code, 200)
        self.assertIn(b"Return Pending", start_return.data)
        self.assertIn(b"Waiting for the book owner", start_return.data)

        self.client.post("/logout")
        self.login("tony")
        owner_detail = self.client.get(f"/requests/{self.request_id}")
        self.assertIn(b"Confirm book received", owner_detail.data)

        finish_return = self.client.post(
            f"/requests/{self.request_id}/confirm-return",
            follow_redirects=True,
        )
        self.assertEqual(finish_return.status_code, 200)
        self.assertIn(b"Returned", finish_return.data)
        self.assertNotIn(b"tony@example.com", finish_return.data)

    def test_json_api_uses_the_same_two_step_contract(self):
        self.login("mina")
        start_response = self.client.patch(
            f"/api/requests/{self.request_id}",
            json={"status": "return_pending"},
        )
        self.assertEqual(start_response.status_code, 200)
        self.assertEqual(start_response.get_json()["request"]["status"], "return_pending")

        self.client.post("/logout")
        self.login("tony")
        finish_response = self.client.patch(
            f"/api/requests/{self.request_id}",
            json={"status": "returned"},
        )
        self.assertEqual(finish_response.status_code, 200)
        self.assertEqual(finish_response.get_json()["request"]["status"], "returned")

        with self.app.app_context():
            self.assertTrue(db.session.get(BookListing, self.listing_id).availability)


if __name__ == "__main__":
    unittest.main()
