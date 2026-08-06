"""D2 demo seed 명령의 재현성과 범위 테스트."""

import unittest
from unittest.mock import patch

from werkzeug.security import check_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User


class DemoSeedCommandTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.runner = self.app.test_cli_runner()

    def test_seed_requires_a_local_demo_password(self):
        with patch.dict("os.environ", {}, clear=True):
            result = self.runner.invoke(args=["seed-demo"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("BOOKLOOP_DEMO_PASSWORD", result.output)

    def test_seed_creates_starting_data_without_a_borrow_request(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "test-demo-password"},
            clear=True,
        ):
            result = self.runner.invoke(args=["seed-demo"])

        self.assertEqual(result.exit_code, 0, result.output)
        with self.app.app_context():
            self.assertEqual(User.query.count(), 3)
            self.assertEqual(BookListing.query.count(), 1)
            self.assertEqual(BorrowRequest.query.count(), 0)

            tony = User.query.filter_by(username="tony").one()
            mina = User.query.filter_by(username="mina").one()
            listing = BookListing.query.one()
            self.assertTrue(check_password_hash(tony.password_hash, "test-demo-password"))
            self.assertEqual(listing.title, "The Odyssey")
            self.assertEqual(listing.author, "Homer")
            self.assertEqual(listing.owner, mina)

    def test_second_seed_run_creates_no_duplicates(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "first-password"},
            clear=True,
        ):
            first_result = self.runner.invoke(args=["seed-demo"])

        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "1111"},
            clear=True,
        ):
            second_result = self.runner.invoke(args=["seed-demo"])

        self.assertEqual(first_result.exit_code, 0, first_result.output)
        self.assertEqual(second_result.exit_code, 0, second_result.output)
        self.assertIn("created users=0, listings=0", second_result.output)

        with self.app.app_context():
            self.assertEqual(User.query.count(), 3)
            self.assertEqual(BookListing.query.count(), 1)
            self.assertEqual(BorrowRequest.query.count(), 0)
            for user in User.query.all():
                self.assertTrue(check_password_hash(user.password_hash, "1111"))

    def test_seed_updates_legacy_almond_listing_without_creating_a_duplicate(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "1111"},
            clear=True,
        ):
            self.runner.invoke(args=["seed-demo"])

            with self.app.app_context():
                listing = BookListing.query.one()
                listing_id = listing.id
                listing.title = "Almond"
                listing.author = "Sohn Won-pyung"
                db.session.commit()

            result = self.runner.invoke(args=["seed-demo"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("created users=0, listings=0", result.output)
        with self.app.app_context():
            listing = BookListing.query.one()
            self.assertEqual(listing.id, listing_id)
            self.assertEqual(listing.title, "The Odyssey")
            self.assertEqual(listing.author, "Homer")

    def test_reset_removes_only_the_demo_listing_requests(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "1111"},
            clear=True,
        ):
            self.runner.invoke(args=["seed-demo"])

        with self.app.app_context():
            tony = User.query.filter_by(username="tony").one()
            mina = User.query.filter_by(username="mina").one()
            demo_listing = BookListing.query.filter_by(title="The Odyssey").one()
            other_listing = BookListing(
                title="Other Book",
                author="Other Author",
                owner=tony,
            )
            db.session.add(other_listing)
            db.session.flush()
            db.session.add_all(
                [
                    BorrowRequest(listing=demo_listing, borrower=tony),
                    BorrowRequest(listing=other_listing, borrower=mina),
                ]
            )
            db.session.commit()
            demo_listing_id = demo_listing.id
            other_listing_id = other_listing.id

        result = self.runner.invoke(args=["reset-demo-requests"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("deleted=1", result.output)
        self.assertIn("remaining BorrowRequests=1", result.output)
        with self.app.app_context():
            self.assertEqual(
                BorrowRequest.query.filter_by(listing_id=demo_listing_id).count(),
                0,
            )
            self.assertEqual(
                BorrowRequest.query.filter_by(listing_id=other_listing_id).count(),
                1,
            )
            self.assertEqual(User.query.count(), 3)
            self.assertEqual(BookListing.query.count(), 2)

    def test_reset_is_safe_when_demo_data_does_not_exist(self):
        result = self.runner.invoke(args=["reset-demo-requests"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("deleted=0", result.output)
        self.assertIn("remaining BorrowRequests=0", result.output)


if __name__ == "__main__":
    unittest.main()
