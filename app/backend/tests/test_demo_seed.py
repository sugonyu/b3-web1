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
            self.assertEqual(BookListing.query.count(), 4)
            self.assertEqual(BorrowRequest.query.count(), 0)

            tony = User.query.filter_by(username="tony").one()
            mina = User.query.filter_by(username="mina").one()
            odyssey = BookListing.query.filter_by(title="The Odyssey").one()
            iliad = BookListing.query.filter_by(title="The Iliad").one()
            vegetarian = BookListing.query.filter_by(title="The Vegetarian").one()
            human_acts = BookListing.query.filter_by(title="Human Acts").one()
            self.assertTrue(check_password_hash(tony.password_hash, "test-demo-password"))
            self.assertTrue(tony.is_admin)
            self.assertFalse(mina.is_admin)
            self.assertEqual(odyssey.author, "Homer")
            self.assertEqual(odyssey.owner, tony)
            self.assertEqual(iliad.author, "Homer")
            self.assertEqual(iliad.owner, tony)
            self.assertEqual(vegetarian.author, "Han Kang")
            self.assertEqual(vegetarian.owner, mina)
            self.assertEqual(human_acts.author, "Han Kang")
            self.assertEqual(human_acts.owner, mina)

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
            self.assertEqual(BookListing.query.count(), 4)
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
                listing = BookListing.query.filter_by(title="The Vegetarian").one()
                listing_id = listing.id
                listing.title = "Almond"
                listing.author = "Sohn Won-pyung"
                db.session.commit()

            result = self.runner.invoke(args=["seed-demo"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("created users=0, listings=0", result.output)
        with self.app.app_context():
            listing = BookListing.query.filter_by(
                owner_id=User.query.filter_by(username="mina").one().id,
                title="The Vegetarian",
            ).one()
            self.assertEqual(listing.id, listing_id)
            self.assertEqual(listing.title, "The Vegetarian")
            self.assertEqual(listing.author, "Han Kang")

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
            demo_listing.availability = False
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
            self.assertTrue(db.session.get(BookListing, demo_listing_id).availability)
            self.assertEqual(User.query.count(), 3)
            self.assertEqual(BookListing.query.count(), 5)

    def test_reset_is_safe_when_demo_data_does_not_exist(self):
        result = self.runner.invoke(args=["reset-demo-requests"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("deleted=0", result.output)
        self.assertIn("remaining BorrowRequests=0", result.output)


if __name__ == "__main__":
    unittest.main()
