"""JSON이나 Jinja에 종속되지 않는 BorrowRequest 공통 service 테스트."""

import unittest

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User
from bookloop.services.borrow_requests import (
    BorrowRequestServiceError,
    create_borrow_request,
    get_authorized_borrow_request,
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
        borrow_request = create_borrow_request(
            self.listing.id,
            self.borrower.id,
        )

        self.assertEqual(borrow_request.status, "pending")
        self.assertEqual(BorrowRequest.query.count(), 1)
        self.assertEqual(borrow_request.listing, self.listing)
        self.assertEqual(borrow_request.borrower, self.borrower)

    def test_create_rejects_duplicate_active_request(self):
        create_borrow_request(self.listing.id, self.borrower.id)

        with self.assertRaises(BorrowRequestServiceError) as context:
            create_borrow_request(self.listing.id, self.borrower.id)

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(
            context.exception.message,
            "active borrow request already exists",
        )
        self.assertEqual(context.exception.request_id, 1)

    def test_read_allows_borrower_and_owner(self):
        borrow_request = create_borrow_request(
            self.listing.id,
            self.borrower.id,
        )

        borrower_result = get_authorized_borrow_request(
            borrow_request.id,
            self.borrower.id,
        )
        owner_result = get_authorized_borrow_request(
            borrow_request.id,
            self.owner.id,
        )

        self.assertEqual(borrower_result, borrow_request)
        self.assertEqual(owner_result, borrow_request)

    def test_read_rejects_unrelated_user(self):
        borrow_request = create_borrow_request(
            self.listing.id,
            self.borrower.id,
        )

        with self.assertRaises(BorrowRequestServiceError) as context:
            get_authorized_borrow_request(
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
            get_authorized_borrow_request(999, self.borrower.id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.message, "borrow request not found")


if __name__ == "__main__":
    unittest.main()
