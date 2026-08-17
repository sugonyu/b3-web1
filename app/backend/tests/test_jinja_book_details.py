"""Book details 페이지와 목록→상세→요청 진입 흐름 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User


class JinjaBookDetailsTest(unittest.TestCase):
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
                general_area="Verdun",
            )
            mina_book = BookListing(
                title="The Vegetarian",
                author="Han Kang",
                owner=mina,
                availability=True,
            )
            db.create_all()
            db.session.add_all([mina, tony, mina_book])
            db.session.commit()
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

    def test_books_home_links_to_independent_details_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(f'href="/books/{self.mina_book_id}"'.encode(), response.data)
        self.assertIn(b"View details", response.data)

    def test_guest_can_view_book_details_without_private_contact_data(self):
        response = self.client.get(f"/books/{self.mina_book_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Book details", response.data)
        self.assertIn(b"The Vegetarian", response.data)
        self.assertIn(b"Han Kang", response.data)
        self.assertIn(b"Montreal", response.data)
        self.assertIn(b"Sign in before requesting a book.", response.data)
        self.assertIn(b"Log in to request", response.data)
        self.assertNotIn(b"mina@example.com", response.data)

    def test_authenticated_borrower_sees_request_form_on_details_page(self):
        self.login("tony")

        response = self.client.get(f"/books/{self.mina_book_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Request this book", response.data)
        self.assertIn(b'Message (optional)', response.data)
        self.assertIn(b'name="message"', response.data)
        self.assertIn(b"Send request", response.data)

    def test_owner_sees_book_details_without_request_form(self):
        self.login("mina")

        response = self.client.get(f"/books/{self.mina_book_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is your book.", response.data)
        self.assertNotIn(b'name="message"', response.data)

    def test_existing_request_is_reachable_from_book_details(self):
        self.login("tony")
        create_response = self.client.post(
            f"/listings/{self.mina_book_id}/request",
            data={"message": "Could we meet near the metro?"},
        )

        self.assertEqual(create_response.status_code, 302)
        request_id = create_response.headers["Location"].rsplit("/", 1)[-1]

        response = self.client.get(f"/books/{self.mina_book_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You already requested this book.", response.data)
        self.assertIn(f'href="/requests/{request_id}"'.encode(), response.data)
        self.assertIn(b"View existing request", response.data)
        self.assertNotIn(b'name="message"', response.data)

        with self.app.app_context():
            self.assertEqual(BorrowRequest.query.count(), 1)

    def test_missing_book_details_returns_not_found(self):
        response = self.client.get("/books/999")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Book not found", response.data)


if __name__ == "__main__":
    unittest.main()
