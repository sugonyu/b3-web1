"""JSON이나 Jinja에 종속되지 않는 BorrowRequest 공통 service 테스트."""

import unittest

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User
from bookloop.services.borrow_requests import (
    BorrowRequestServiceError,
    cancel_borrow_request_service,
    create_borrow_request_service,
    get_approved_contact_context_service,
    get_borrower_decision_context_service,
    get_authorized_borrow_request_service,
    list_borrower_requests_service,
    list_listing_owner_requests_service,
    update_borrow_request_status_service,
)


class BorrowRequestServiceTest(unittest.TestCase):
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

        self.owner = User(
            username="mina",
            email="mina@example.com",
            password_hash="test-hash",
            general_area="Montreal",
        )
        self.borrower = User(
            username="tony",
            email="tony@example.com",
            password_hash="test-hash",
            general_area="Montreal",
        )
        self.other_user = User(
            username="alex",
            email="alex@example.com",
            password_hash="test-hash",
            general_area="Montreal",
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

    def test_create_returns_persisted_pending_request(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        self.assertEqual(borrow_request.status, "pending")
        self.assertEqual(BorrowRequest.query.count(), 1)
        self.assertEqual(borrow_request.listing, self.listing)
        self.assertEqual(borrow_request.borrower, self.borrower)

    def test_create_strips_and_persists_optional_message(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
            "  Is pickup near NDG possible?  ",
        )

        self.assertEqual(borrow_request.message, "Is pickup near NDG possible?")

    def test_create_rejects_message_over_500_characters(self):
        with self.assertRaises(BorrowRequestServiceError) as context:
            create_borrow_request_service(
                self.listing.id,
                self.borrower.id,
                "x" * 501,
            )

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "request message is too long")

    def test_create_rejects_duplicate_active_request(self):
        create_borrow_request_service(self.listing.id, self.borrower.id)

        with self.assertRaises(BorrowRequestServiceError) as context:
            create_borrow_request_service(self.listing.id, self.borrower.id)

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(
            context.exception.message,
            "active borrow request already exists",
        )
        self.assertEqual(context.exception.request_id, 1)

    def test_read_allows_borrower_and_owner(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        borrower_result = get_authorized_borrow_request_service(
            borrow_request.id,
            self.borrower.id,
        )
        owner_result = get_authorized_borrow_request_service(
            borrow_request.id,
            self.owner.id,
        )

        self.assertEqual(borrower_result, borrow_request)
        self.assertEqual(owner_result, borrow_request)

    def test_read_rejects_unrelated_user(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        with self.assertRaises(BorrowRequestServiceError) as context:
            get_authorized_borrow_request_service(
                borrow_request.id,
                self.other_user.id,
            )

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(
            context.exception.message,
            "borrow request access forbidden",
        )

    def test_read_returns_not_found_for_missing_request(self):
        with self.assertRaises(BorrowRequestServiceError) as context:
            get_authorized_borrow_request_service(999, self.borrower.id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.message, "borrow request not found")

    def test_borrower_list_returns_only_own_requests_latest_first(self):
        first_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )
        other_listing = BookListing(
            title="The Odyssey",
            author="Homer",
            owner=self.owner,
        )
        db.session.add(other_listing)
        db.session.commit()
        second_request = create_borrow_request_service(
            other_listing.id,
            self.borrower.id,
        )
        unrelated_request = BorrowRequest(
            listing=other_listing,
            borrower=self.other_user,
            status="rejected",
        )
        db.session.add(unrelated_request)
        db.session.commit()

        result = list_borrower_requests_service(self.borrower.id)

        self.assertEqual(
            [borrow_request.id for borrow_request in result],
            [second_request.id, first_request.id],
        )

    def test_owner_list_returns_only_requests_for_owned_listings(self):
        owned_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )
        second_owner = User(
            username="jiyun",
            email="jiyun@example.com",
            password_hash="test-hash",
            general_area="Laval",
        )
        other_listing = BookListing(
            title="Pachinko",
            author="Min Jin Lee",
            owner=second_owner,
        )
        db.session.add_all([second_owner, other_listing])
        db.session.commit()
        db.session.add(
            BorrowRequest(
                listing=other_listing,
                borrower=self.other_user,
            )
        )
        db.session.commit()

        result = list_listing_owner_requests_service(self.owner.id)

        self.assertEqual(result, [owned_request])

    def test_owner_approves_request_and_reserves_listing(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        result = update_borrow_request_status_service(
            borrow_request.id,
            self.owner.id,
            "approved",
        )

        self.assertEqual(result.status, "approved")
        self.assertFalse(self.listing.availability)

    def test_owner_rejects_request_without_reserving_listing(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        result = update_borrow_request_status_service(
            borrow_request.id,
            self.owner.id,
            "rejected",
        )

        self.assertEqual(result.status, "rejected")
        self.assertTrue(self.listing.availability)

    def test_approved_contact_returns_only_the_other_party(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )
        update_borrow_request_status_service(
            borrow_request.id,
            self.owner.id,
            "approved",
        )

        borrower_view = get_approved_contact_context_service(
            borrow_request,
            self.borrower.id,
        )
        owner_view = get_approved_contact_context_service(
            borrow_request,
            self.owner.id,
        )

        self.assertEqual(borrower_view["email"], "mina@example.com")
        self.assertEqual(borrower_view["role"], "Book owner")
        self.assertEqual(owner_view["email"], "tony@example.com")
        self.assertEqual(owner_view["role"], "Borrower")
        self.assertNotIn("password_hash", borrower_view)

    def test_contact_stays_hidden_until_request_is_approved(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        self.assertIsNone(
            get_approved_contact_context_service(borrow_request, self.borrower.id)
        )

    def test_approved_contact_rejects_unrelated_user(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )
        update_borrow_request_status_service(
            borrow_request.id,
            self.owner.id,
            "approved",
        )

        with self.assertRaises(BorrowRequestServiceError) as context:
            get_approved_contact_context_service(
                borrow_request,
                self.other_user.id,
            )

        self.assertEqual(context.exception.status_code, 403)

    def test_non_owner_cannot_decide_request(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        with self.assertRaises(BorrowRequestServiceError) as context:
            update_borrow_request_status_service(
                borrow_request.id,
                self.other_user.id,
                "approved",
            )

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(borrow_request.status, "pending")

    def test_decision_context_returns_only_privacy_safe_aggregates(self):
        completed_request = BorrowRequest(
            listing=self.listing,
            borrower=self.borrower,
            status="returned",
        )
        current_request = BorrowRequest(
            listing=self.listing,
            borrower=self.borrower,
            status="pending",
        )
        db.session.add_all([completed_request, current_request])
        db.session.commit()

        context = get_borrower_decision_context_service(current_request)

        self.assertEqual(context["completed_exchanges"], 1)
        self.assertEqual(context["active_requests"], 1)
        self.assertFalse(context["is_first_time_borrower"])
        self.assertEqual(context["member_since"], self.borrower.created_at)
        self.assertEqual(context["request_created_at"], current_request.created_at)
        self.assertNotIn("email", context)
        self.assertNotIn("password_hash", context)

    def test_borrower_cancels_pending_request(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        result = cancel_borrow_request_service(borrow_request.id, self.borrower.id)

        self.assertEqual(result.status, "cancelled")
        self.assertTrue(self.listing.availability)

    def test_non_borrower_cannot_cancel_request(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )

        with self.assertRaises(BorrowRequestServiceError) as context:
            cancel_borrow_request_service(borrow_request.id, self.owner.id)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(borrow_request.status, "pending")

    def test_borrower_cannot_cancel_after_owner_decision(self):
        borrow_request = create_borrow_request_service(
            self.listing.id,
            self.borrower.id,
        )
        update_borrow_request_status_service(
            borrow_request.id,
            self.owner.id,
            "approved",
        )

        with self.assertRaises(BorrowRequestServiceError) as context:
            cancel_borrow_request_service(borrow_request.id, self.borrower.id)

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(borrow_request.status, "approved")


if __name__ == "__main__":
    unittest.main()
