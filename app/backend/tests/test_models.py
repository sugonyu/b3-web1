"""Core model and relationship tests."""

import unittest

from bookloop import create_app
from bookloop.database import db
from bookloop.models import BookListing, BorrowRequest, User


class CoreModelTest(unittest.TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_owns_book_listing(self):
        owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="Montreal",
        )
        listing = BookListing(
            title="The Vegetarian",
            author="Han Kang",
            owner=owner,
        )
        db.session.add(owner)
        db.session.commit()

        self.assertEqual(listing.owner, owner)
        self.assertEqual(owner.book_listings, [listing])
        self.assertTrue(listing.availability)

    def test_borrow_request_connects_borrower_and_listing(self):
        owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        borrower = User(
            username="borrower",
            email="borrower@example.com",
            password_hash="test-hash",
            general_area="Verdun",
        )
        listing = BookListing(
            title="Almond",
            author="Sohn Won-pyung",
            owner=owner,
        )
        borrow_request = BorrowRequest(listing=listing, borrower=borrower)
        db.session.add_all([owner, borrower, listing, borrow_request])
        db.session.commit()

        self.assertEqual(borrow_request.status, "pending")
        self.assertEqual(borrow_request.listing, listing)
        self.assertEqual(borrow_request.borrower, borrower)
        self.assertEqual(listing.borrow_requests, [borrow_request])
        self.assertEqual(borrower.borrow_requests, [borrow_request])


if __name__ == "__main__":
    unittest.main()
