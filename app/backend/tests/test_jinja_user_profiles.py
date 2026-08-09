"""Privacy-safe Jinja 사용자 profile의 공개 범위 테스트."""

import unittest

from werkzeug.security import generate_password_hash

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, User


class JinjaUserProfileTest(unittest.TestCase):
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
            db.create_all()
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
                general_area="NDG",
            )
            alex = User(
                username="alex",
                email="alex@example.com",
                password_hash=generate_password_hash("1111"),
                general_area="Laval",
            )
            odyssey = BookListing(
                title="The Odyssey",
                author="Homer",
                owner=mina,
                availability=True,
            )
            hidden_book = BookListing(
                title="Private Draft",
                author="Unknown",
                owner=mina,
                availability=False,
            )
            db.session.add_all([mina, tony, alex, odyssey, hidden_book])
            db.session.commit()
            self.mina_id = mina.id
            self.tony_id = tony.id
            self.alex_id = alex.id
            self.odyssey_id = odyssey.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username="tony"):
        return self.client.post(
            "/login",
            data={"username": username, "password": "1111"},
        )

    def test_profile_requires_login_and_returns_to_same_url(self):
        response = self.client.get(f"/users/{self.mina_id}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"],
            f"/login?next=/users/{self.mina_id}",
        )

    def test_profile_shows_minimum_safe_fields_and_available_books(self):
        self.login()

        response = self.client.get(f"/users/{self.mina_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Privacy-safe member profile", response.data)
        self.assertIn("mina 👩".encode(), response.data)
        self.assertIn(b"Montreal", response.data)
        self.assertIn(b"Member since", response.data)
        self.assertIn(b"Completed exchanges", response.data)
        self.assertIn(b"The Odyssey", response.data)
        self.assertIn(b"Contact information protected", response.data)
        self.assertIn(b"until you and this member have an approved", response.data)
        self.assertIn(b'aria-label="Email privacy policy"', response.data)
        self.assertNotIn(b"Private Draft", response.data)
        self.assertNotIn(b"mina@example.com", response.data)
        self.assertNotIn(b"tony@example.com", response.data)
        self.assertNotIn(b"password", response.data.lower())

    def test_user_can_see_own_email_on_own_profile(self):
        self.login("tony")

        response = self.client.get(f"/users/{self.tony_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"tony@example.com", response.data)
        self.assertIn(b"This is your private account email", response.data)
        self.assertNotIn(b"mina@example.com", response.data)

    def test_approved_parties_can_see_each_others_email_on_profiles(self):
        with self.app.app_context():
            listing = db.session.get(BookListing, self.odyssey_id)
            borrower = db.session.get(User, self.tony_id)
            db.session.add(
                BorrowRequest(
                    listing=listing,
                    borrower=borrower,
                    status="approved",
                )
            )
            db.session.commit()

        self.login("tony")
        owner_profile = self.client.get(f"/users/{self.mina_id}")
        self.assertIn(b"mina@example.com", owner_profile.data)
        self.assertIn(b"have an approved borrowing request", owner_profile.data)

        self.client.post("/logout")
        self.login("mina")
        borrower_profile = self.client.get(f"/users/{self.tony_id}")
        self.assertIn(b"tony@example.com", borrower_profile.data)

        self.client.post("/logout")
        self.login("alex")
        unrelated_profile = self.client.get(f"/users/{self.mina_id}")
        self.assertNotIn(b"mina@example.com", unrelated_profile.data)
        self.assertIn(b"Contact information protected", unrelated_profile.data)

    def test_returned_request_counts_for_borrower_and_owner_profiles(self):
        with self.app.app_context():
            listing = db.session.get(BookListing, self.odyssey_id)
            borrower = db.session.get(User, self.tony_id)
            db.session.add(
                BorrowRequest(
                    listing=listing,
                    borrower=borrower,
                    status="returned",
                )
            )
            db.session.commit()

        self.login()
        owner_profile = self.client.get(f"/users/{self.mina_id}")
        borrower_profile = self.client.get(f"/users/{self.tony_id}")

        self.assertIn(b"<dd>1</dd>", owner_profile.data)
        self.assertIn(b"<dd>1</dd>", borrower_profile.data)

    def test_missing_profile_returns_404_without_private_data(self):
        self.login()

        response = self.client.get("/users/999")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Profile not found", response.data)
        self.assertNotIn(b"example.com", response.data)

    def test_books_home_links_signed_in_user_and_owner_profiles(self):
        self.login()

        response = self.client.get("/")

        self.assertIn(
            f'href="/users/{self.tony_id}"'.encode(),
            response.data,
        )
        self.assertIn(
            f'href="/users/{self.mina_id}"'.encode(),
            response.data,
        )


if __name__ == "__main__":
    unittest.main()
