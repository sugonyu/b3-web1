"""개발 전용 read-only database inspector의 접근과 노출 경계 테스트."""

import unittest

from bookloop import create_app
from bookloop.database import db
from bookloop.models import BookListing, BorrowRequest, User


class DeveloperDatabaseInspectorTest(unittest.TestCase):
    def create_test_app(self, inspector_enabled=False, debug=False):
        """각 테스트가 독립적인 in-memory SQLite app을 사용하게 한다."""
        return create_app(
            {
                "TESTING": True,
                "DEBUG": debug,
                "ENABLE_DEV_DB_INSPECTOR": inspector_enabled,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )

    def seed_database(self, app):
        """화면과 관계 ID를 검증할 최소 User, listing, request를 만든다."""
        with app.app_context():
            db.create_all()
            owner = User(
                username="mina",
                email="mina.private@example.com",
                password_hash="never-render-this-hash",
                general_area="Montreal",
            )
            borrower = User(
                username="tony",
                email="tony.private@example.com",
                password_hash="another-private-hash",
                general_area="NDG",
            )
            listing = BookListing(
                title="Almond",
                author="Sohn Won-pyung",
                owner=owner,
            )
            borrow_request = BorrowRequest(
                listing=listing,
                borrower=borrower,
            )
            db.session.add_all([owner, borrower, listing, borrow_request])
            db.session.commit()

    def test_inspector_is_hidden_when_explicit_setting_is_disabled(self):
        app = self.create_test_app(inspector_enabled=False, debug=True)

        response = app.test_client().get("/dev/db")

        self.assertEqual(response.status_code, 404)
        response.close()

    def test_inspector_is_hidden_outside_debug_mode(self):
        app = self.create_test_app(inspector_enabled=True, debug=False)

        response = app.test_client().get("/dev/db")

        self.assertEqual(response.status_code, 404)
        response.close()

    def test_inspector_lists_safe_fields_for_three_models(self):
        app = self.create_test_app(inspector_enabled=True, debug=True)
        self.seed_database(app)

        response = app.test_client().get("/dev/db")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Users", response.data)
        self.assertIn(b"Book Listings", response.data)
        self.assertIn(b"Borrow Requests", response.data)
        self.assertIn(b'href="/dev/db/"', response.data)
        self.assertIn(b"Reload", response.data)
        self.assertIn(b"/static/web/python-favicon.svg", response.data)
        self.assertIn(b"mina", response.data)
        self.assertIn(b"tony", response.data)
        self.assertIn(b"Almond", response.data)
        self.assertIn(b"pending", response.data)

        # 실제 private 값이 HTML 어디에도 섞이지 않았는지 값 자체로 검사한다.
        self.assertNotIn(b"mina.private@example.com", response.data)
        self.assertNotIn(b"tony.private@example.com", response.data)
        self.assertNotIn(b"never-render-this-hash", response.data)
        self.assertNotIn(b"another-private-hash", response.data)
        response.close()

    def test_inspector_get_does_not_change_database_rows(self):
        app = self.create_test_app(inspector_enabled=True, debug=True)
        self.seed_database(app)

        with app.app_context():
            counts_before = (
                User.query.count(),
                BookListing.query.count(),
                BorrowRequest.query.count(),
            )

        response = app.test_client().get("/dev/db")
        response.close()

        with app.app_context():
            counts_after = (
                User.query.count(),
                BookListing.query.count(),
                BorrowRequest.query.count(),
            )

        self.assertEqual(counts_after, counts_before)


if __name__ == "__main__":
    unittest.main()
