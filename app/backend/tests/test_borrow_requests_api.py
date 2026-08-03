"""Private Stage A-4 BorrowRequest workflow endpoint tests."""

import unittest

from bookloop import create_app
from bookloop.database import db
from bookloop.models import BookListing, BorrowRequest, User


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
        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
            json={"borrower_id": self.borrower.id},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["request"]["status"], "pending")
        self.assertEqual(BorrowRequest.query.count(), 1)

    def test_post_request_rejects_listing_owner(self):
        response = self.client.post(
            f"/api/listings/{self.listing.id}/requests",
            json={"borrower_id": self.owner.id},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(),
            {"error": "owner cannot borrow own listing"},
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

    def test_patch_request_approves_and_reserves_listing(self):
        borrow_request = self.create_pending_request()

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"owner_id": self.owner.id, "status": "approved"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["request"]["status"], "approved")
        self.assertFalse(self.listing.availability)

    def test_patch_request_returns_book_and_restores_availability(self):
        borrow_request = self.create_pending_request()
        borrow_request.status = "approved"
        self.listing.availability = False
        db.session.commit()

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"owner_id": self.owner.id, "status": "returned"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["request"]["status"], "returned")
        self.assertTrue(self.listing.availability)

    def test_patch_request_rejects_invalid_transition(self):
        borrow_request = self.create_pending_request()

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"owner_id": self.owner.id, "status": "returned"},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(),
            {"error": "invalid borrow request transition"},
        )

    def test_patch_request_rejects_non_owner(self):
        borrow_request = self.create_pending_request()

        response = self.client.patch(
            f"/api/requests/{borrow_request.id}",
            json={"owner_id": self.borrower.id, "status": "approved"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {"error": "owner permission required"},
        )


if __name__ == "__main__":
    unittest.main()
