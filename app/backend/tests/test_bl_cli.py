"""python3로 직접 실행하는 BookLoop CLI command 테스트."""

import unittest
from unittest.mock import patch

from click.testing import CliRunner

from bookloop import create_app
from bookloop.db import db
from bookloop.devtools.bl_cli.commands import create_cli
from bookloop.db.models import BookListing, BorrowRequest, User


class BookLoopCliTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.cli = create_cli(lambda: self.app)
        self.runner = CliRunner()

    def test_no_command_shows_bookloop_usage(self):
        result = self.runner.invoke(self.cli)

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("BookLoop CLI (BL-CLI)", result.output)
        self.assertIn("python3 bl_cli.py <command>", result.output)
        self.assertIn("seed-demo", result.output)
        self.assertIn("reset-demo-requests", result.output)
        self.assertIn("upgrade-created-at", result.output)
        self.assertIn("upgrade-request-message", result.output)

    def test_seed_demo_command_uses_the_shared_seed_function(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "1111"},
            clear=True,
        ):
            result = self.runner.invoke(self.cli, ["seed-demo"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Demo seed complete", result.output)
        with self.app.app_context():
            self.assertEqual(User.query.count(), 3)
            self.assertEqual(BookListing.query.count(), 4)
            self.assertFalse(User.query.filter_by(username="tony").one().is_admin)
            self.assertTrue(User.query.filter_by(username="alex").one().is_admin)
            self.assertEqual(BorrowRequest.query.count(), 0)

    def test_reset_demo_requests_keeps_users_and_listing(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "1111"},
            clear=True,
        ):
            self.runner.invoke(self.cli, ["seed-demo"])

        with self.app.app_context():
            tony = User.query.filter_by(username="tony").one()
            listing = BookListing.query.filter_by(title="The Odyssey").one()
            db.session.add(BorrowRequest(listing=listing, borrower=tony))
            db.session.commit()

        result = self.runner.invoke(self.cli, ["reset-demo-requests"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("deleted=1", result.output)
        self.assertIn("demo listings restored=4", result.output)
        with self.app.app_context():
            self.assertEqual(BorrowRequest.query.count(), 0)
            self.assertEqual(User.query.count(), 3)
            self.assertEqual(BookListing.query.count(), 4)

    def test_reset_restores_the_original_four_demo_listings(self):
        with patch.dict(
            "os.environ",
            {"BOOKLOOP_DEMO_PASSWORD": "1111"},
            clear=True,
        ):
            self.runner.invoke(self.cli, ["seed-demo"])

        with self.app.app_context():
            changed_listing = BookListing.query.filter_by(title="The Vegetarian").one()
            changed_listing.title = "Temporary title"
            changed_listing.author = "Temporary author"
            changed_listing.availability = False
            db.session.delete(BookListing.query.filter_by(title="Human Acts").one())
            db.session.commit()

        result = self.runner.invoke(self.cli, ["reset-demo-requests"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("demo listings restored=4", result.output)
        with self.app.app_context():
            expected_titles = {
                "The Odyssey",
                "The Iliad",
                "The Vegetarian",
                "Human Acts",
            }
            self.assertTrue(
                expected_titles.issubset(
                    {listing.title for listing in BookListing.query.all()}
                )
            )
            self.assertTrue(
                all(
                    listing.availability
                    for listing in BookListing.query.filter(
                        BookListing.title.in_(tuple(expected_titles))
                    ).all()
                )
            )

    def test_upgrade_created_at_is_safe_when_schema_is_current(self):
        result = self.runner.invoke(self.cli, ["upgrade-created-at"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("already current", result.output)

    def test_upgrade_request_message_is_safe_when_schema_is_current(self):
        with self.app.app_context():
            db.create_all()

        result = self.runner.invoke(self.cli, ["upgrade-request-message"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("already current", result.output)


if __name__ == "__main__":
    unittest.main()
