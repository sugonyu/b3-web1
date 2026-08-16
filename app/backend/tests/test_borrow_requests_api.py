"""Private Stage A-4 BorrowRequest workflow endpoint tests."""

import unittest

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User


class BorrowRequestWorkflowEndpointTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        self.borrower = User(
            username="borrower",
            email="borrower@example.com",
            password_hash="test-hash",
            general_area="Verdun",
        )
        self.other_user = User(
            username="other-user",
            email="other@example.com",
            password_hash="other-test-hash",
            general_area="Plateau",
        )
        self.listing = BookListing(
            title="Almond",
            author="Sohn Won-pyung",
            owner=self.owner,
        )
        db.session.add_all(
            [self.owner, self.borrower, self.other_user, self.listing]
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_pending_request(self):
        borrow_request = BorrowRequest(
            listing=self.listing,
            borrower=self.borrower,
        )
        db.session.add(borrow_request)
        db.session.commit()
        return borrow_request

    def login_as(self, user):
        """Flask-Login이 읽는 test session에 현재 사용자 ID를 기록한다."""
        with self.client.session_transaction() as session:
            session["_user_id"] = str(user.id)
            session["_fresh"] = True

    def test_post_request_creates_pending_request(self):
        self.login_as(self.borrower)
        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
            json={"message": "Could we arrange pickup this weekend?"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["request"]["status"], "pending")
        self.assertEqual(
            response.get_json()["request"]["message"],
            "Could we arrange pickup this weekend?",
        )
        self.assertEqual(BorrowRequest.query.count(), 1)

    def test_post_request_rejects_message_over_500_characters(self):
        self.login_as(self.borrower)
        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
            json={"message": "x" * 501},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "request message is too long"},
        )
        self.assertEqual(BorrowRequest.query.count(), 0)

    def test_post_request_rejects_listing_owner(self):
        self.login_as(self.owner)
        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(),
            {"error": "owner cannot borrow own listing"},
        )

    def test_post_request_requires_login(self):
        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
            json={"borrower_id": self.borrower.id},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"error": "authentication required"})
        self.assertEqual(BorrowRequest.query.count(), 0)

    def test_post_request_uses_session_identity_not_body_user_id(self):
        self.login_as(self.borrower)

        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
            json={"borrower_id": self.owner.id},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json()["request"]["borrower"]["id"],
            self.borrower.id,
        )

    def test_get_request_allows_borrower_and_hides_private_fields(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.borrower)

        response = self.client.get(f"/api/requests/{borrow_request.id}")

        self.assertEqual(response.status_code, 200)
        request_data = response.get_json()["request"]
        self.assertEqual(request_data["id"], borrow_request.id)
        self.assertEqual(request_data["status"], "pending")
        self.assertEqual(request_data["listing_id"], self.listing.id)
        self.assertEqual(request_data["borrower"]["id"], self.borrower.id)
        self.assertNotIn("email", request_data["borrower"])
        self.assertNotIn("password_hash", request_data["borrower"])
        self.assertNotIn(self.borrower.email, response.get_data(as_text=True))

    def test_get_request_allows_listing_owner(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.owner)

        response = self.client.get(f"/api/requests/{borrow_request.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["request"]["id"], borrow_request.id)

    def test_get_request_rejects_unrelated_user(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.other_user)

        response = self.client.get(f"/api/requests/{borrow_request.id}")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {"error": "borrow request access forbidden"},
        )

    def test_get_request_rejects_logged_out_user(self):
        borrow_request = self.create_pending_request()

        response = self.client.get(f"/api/requests/{borrow_request.id}")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.get_json(),
            {"error": "authentication required"},
        )

    def test_get_request_returns_404_for_missing_request(self):
        self.login_as(self.borrower)

        response = self.client.get("/api/requests/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json(),
            {"error": "borrow request not found"},
        )

    def test_get_borrower_requests_returns_only_session_users_rows(self):
        first_request = self.create_pending_request()
        other_request = BorrowRequest(
            listing=self.listing,
            borrower=self.other_user,
        )
        db.session.add(other_request)
        db.session.commit()
        self.login_as(self.borrower)

        response = self.client.get("/api/requests")

        self.assertEqual(response.status_code, 200)
        request_rows = response.get_json()["requests"]
        self.assertEqual([row["id"] for row in request_rows], [first_request.id])
        self.assertEqual(request_rows[0]["listing"]["title"], "Almond")
        self.assertNotIn("email", request_rows[0]["borrower"])
        self.assertNotIn(self.borrower.email, response.get_data(as_text=True))

    def test_get_listing_requests_returns_only_session_owners_rows(self):
        owned_request = self.create_pending_request()
        other_listing = BookListing(
            title="The Odyssey",
            author="Homer",
            owner=self.other_user,
        )
        unrelated_request = BorrowRequest(
            listing=other_listing,
            borrower=self.borrower,
        )
        db.session.add_all([other_listing, unrelated_request])
        db.session.commit()
        self.login_as(self.owner)

        response = self.client.get("/api/listing-requests")

        self.assertEqual(response.status_code, 200)
        request_rows = response.get_json()["requests"]
        self.assertEqual([row["id"] for row in request_rows], [owned_request.id])
        self.assertEqual(request_rows[0]["listing"]["owner"]["id"], self.owner.id)
        self.assertNotIn("email", request_rows[0]["listing"]["owner"])
        self.assertNotIn(self.owner.email, response.get_data(as_text=True))

    def test_request_collection_endpoints_require_login(self):
        sent_response = self.client.get("/api/requests")
        received_response = self.client.get("/api/listing-requests")

        self.assertEqual(sent_response.status_code, 401)
        self.assertEqual(received_response.status_code, 401)
        self.assertEqual(
            sent_response.get_json(),
            {"error": "authentication required"},
        )

    def test_patch_request_approves_and_reserves_listing(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.owner)

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"status": "approved"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["request"]["status"], "approved")
        self.assertFalse(self.listing.availability)

    def test_patch_request_returns_book_and_restores_availability(self):
        borrow_request = self.create_pending_request()
        borrow_request.status = "return_pending"
        self.listing.availability = False
        db.session.commit()
        self.login_as(self.owner)

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"status": "returned"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["request"]["status"], "returned")
        self.assertTrue(self.listing.availability)

    def test_patch_request_rejects_invalid_transition(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.owner)

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"status": "returned"},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(),
            {"error": "return cannot be confirmed"},
        )

    def test_patch_request_rejects_non_owner(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.borrower)

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"owner_id": self.owner.id, "status": "approved"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {"error": "owner permission required"},
        )

    def test_patch_request_requires_login(self):
        borrow_request = self.create_pending_request()

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"owner_id": self.owner.id, "status": "approved"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"error": "authentication required"})
        self.assertEqual(borrow_request.status, "pending")

    def test_patch_request_allows_borrower_to_cancel_pending_request(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.borrower)

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"status": "cancelled"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["request"]["status"], "cancelled")
        self.assertTrue(self.listing.availability)

    def test_patch_request_rejects_owner_cancelling_borrowers_request(self):
        borrow_request = self.create_pending_request()
        self.login_as(self.owner)

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"status": "cancelled"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {"error": "borrower permission required"},
        )


if __name__ == "__main__":
    unittest.main()
