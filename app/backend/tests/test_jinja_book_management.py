"""로그인 사용자의 BookListing 등록·수정·availability 화면 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, User


class JinjaBookManagementTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            mina = User(
                username="mina",
                email="mina@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            tony = User(
                username="tony",
                email="tony@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Montreal",
            )
            mina_book = BookListing(
                title="The Vegetarian",
                author="Han Kang",
                owner=mina,
            )
            db.create_all()
            db.session.add_all([mina, tony, mina_book])
            db.session.commit()
            self.mina_id = mina.id
            self.tony_id = tony.id
            self.mina_book_id = mina_book.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username):
        return self.client.post(
            "/login",
            data={"username": username, "password": "1111"},
        )

    def test_guest_is_redirected_from_my_books(self):
        response = self.client.get("/my-books/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login?next=/my-books/", response.headers["Location"])

    def test_owner_sees_only_own_books(self):
        self.login("mina")

        response = self.client.get("/my-books/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your book listings", response.data)
        self.assertIn(b"The Vegetarian", response.data)
        self.assertIn(b"Edit", response.data)
        self.assertIn(b"Make unavailable", response.data)
        self.assertNotIn(b"tony@example.com", response.data)

    def test_owner_can_add_book(self):
        self.login("tony")

        response = self.client.post(
            "/my-books/new",
            data={"title": "Almond", "author": "Sohn Won-pyung"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/my-books/")
        with self.app.app_context():
            listing = BookListing.query.filter_by(owner_id=self.tony_id).one()
            self.assertEqual(listing.title, "Almond")
            self.assertTrue(listing.availability)

    def test_blank_book_fields_are_rejected(self):
        self.login("tony")

        response = self.client.post(
            "/my-books/new",
            data={"title": "   ", "author": "Han Kang"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Book title is required.", response.data)
        with self.app.app_context():
            self.assertEqual(BookListing.query.filter_by(owner_id=self.tony_id).count(), 0)

    def test_owner_can_edit_book_details(self):
        self.login("mina")

        response = self.client.post(
            f"/my-books/{self.mina_book_id}/edit",
            data={"title": "Human Acts", "author": "Han Kang"},
        )

        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            listing = db.session.get(BookListing, self.mina_book_id)
            self.assertEqual(listing.title, "Human Acts")
            self.assertEqual(listing.author, "Han Kang")

    def test_non_owner_cannot_edit_book(self):
        self.login("tony")

        response = self.client.get(f"/my-books/{self.mina_book_id}/edit")

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Only the book owner can manage this listing.", response.data)

    def test_owner_can_change_availability(self):
        self.login("mina")

        response = self.client.post(
            f"/my-books/{self.mina_book_id}/availability",
        )

        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            listing = db.session.get(BookListing, self.mina_book_id)
            self.assertFalse(listing.availability)

    def test_non_owner_cannot_change_availability(self):
        self.login("tony")

        response = self.client.post(
            f"/my-books/{self.mina_book_id}/availability",
        )

        self.assertEqual(response.status_code, 403)
        with self.app.app_context():
            listing = db.session.get(BookListing, self.mina_book_id)
            self.assertTrue(listing.availability)

    def test_owner_can_delete_book_without_request_history(self):
        self.login("tony")
        with self.app.app_context():
            listing = BookListing(title="Almond", author="Sohn Won-pyung", owner_id=self.tony_id)
            db.session.add(listing)
            db.session.commit()
            listing_id = listing.id

        response = self.client.post(f"/my-books/{listing_id}/delete")

        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertIsNone(db.session.get(BookListing, listing_id))

    def test_book_with_request_history_cannot_be_deleted(self):
        self.login("mina")
        with self.app.app_context():
            from bookloop.db.models import BorrowRequest

            borrow_request = BorrowRequest(
                listing_id=self.mina_book_id,
                borrower_id=self.tony_id,
            )
            db.session.add(borrow_request)
            db.session.commit()

        response = self.client.post(f"/my-books/{self.mina_book_id}/delete")

        self.assertEqual(response.status_code, 409)
        self.assertIn(b"A book with borrow request history cannot be deleted.", response.data)
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(BookListing, self.mina_book_id))

    def test_non_owner_cannot_delete_book(self):
        self.login("tony")

        response = self.client.post(f"/my-books/{self.mina_book_id}/delete")

        self.assertEqual(response.status_code, 403)
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(BookListing, self.mina_book_id))


if __name__ == "__main__":
    unittest.main()
