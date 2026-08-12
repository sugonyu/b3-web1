"""Private Stage A-2 core model and relationship tests."""

import unittest

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, Report, User


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
        self.assertIsNotNone(owner.created_at)
        self.assertIsNotNone(listing.created_at)

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
        self.assertIsNotNone(borrow_request.created_at)

    def test_report_persists_related_request_and_both_parties(self):
        owner = User(
            username="mina",
            email="mina@example.com",
            password_hash="test-hash",
            general_area="Montreal",
        )
        borrower = User(
            username="tony",
            email="tony@example.com",
            password_hash="test-hash",
            general_area="Montreal",
        )
        listing = BookListing(
            title="The Odyssey",
            author="Homer",
            owner=owner,
        )
        borrow_request = BorrowRequest(listing=listing, borrower=borrower)
        report = Report(
            reporter=borrower,
            reported_user=owner,
            borrow_request=borrow_request,
            category="no_show",
            details="The arranged exchange did not happen.",
        )
        db.session.add(report)
        db.session.commit()

        saved_report = db.session.get(Report, report.id)

        self.assertEqual(saved_report.status, "open")
        self.assertEqual(saved_report.reporter, borrower)
        self.assertEqual(saved_report.reported_user, owner)
        self.assertEqual(saved_report.borrow_request, borrow_request)
        self.assertEqual(borrower.submitted_reports, [saved_report])
        self.assertEqual(owner.received_reports, [saved_report])
        self.assertEqual(borrow_request.reports, [saved_report])
        self.assertIsNotNone(saved_report.created_at)


if __name__ == "__main__":
    unittest.main()
