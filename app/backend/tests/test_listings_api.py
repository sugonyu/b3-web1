"""Private Stage A-3 BookListing CRUD endpoint tests."""

import unittest

from bookloop import create_app
from bookloop.database import db
from bookloop.models import BookListing, User


class BookListingCollectionEndpointTest(unittest.TestCase):
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
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_listings_returns_empty_collection(self):
        response = self.client.get("/api/listings")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"listings": []})

    def test_get_listings_returns_public_listing_data(self):
        owner = User(
            username="book_owner",
            email="private@example.com",
            password_hash="private-test-hash",
            general_area="NDG",
        )
        listing = BookListing(
            title="Almond",
            author="Sohn Won-pyung",
            owner=owner,
        )
        db.session.add_all([owner, listing])
        db.session.commit()

        response = self.client.get("/api/listings")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "listings": [
                    {
                        "id": listing.id,
                        "title": "Almond",
                        "author": "Sohn Won-pyung",
                        "availability": True,
                        "owner": {
                            "id": owner.id,
                            "username": "book_owner",
                            "general_area": "NDG",
                        },
                    }
                ]
            },
        )
        self.assertNotIn("email", response.get_json()["listings"][0]["owner"])
        self.assertNotIn(
            "password_hash",
            response.get_json()["listings"][0]["owner"],
        )

    def test_post_listings_creates_one_listing(self):
        owner = User(
            username="book_owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        db.session.add(owner)
        db.session.commit()

        response = self.client.post(
            "/api/listings",
            json={
                "title": "  Almond  ",
                "author": "  Sohn Won-pyung  ",
                "owner_id": owner.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BookListing.query.count(), 1)
        self.assertEqual(response.get_json()["listing"]["title"], "Almond")
        self.assertEqual(
            response.get_json()["listing"]["author"],
            "Sohn Won-pyung",
        )
        self.assertEqual(response.get_json()["listing"]["owner"]["id"], owner.id)

    def test_post_listings_rejects_missing_title(self):
        response = self.client.post(
            "/api/listings",
            json={
                "author": "Han Kang",
                "owner_id": 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "title is required"})
        self.assertEqual(BookListing.query.count(), 0)

    def test_post_listings_rejects_unknown_owner(self):
        response = self.client.post(
            "/api/listings",
            json={
                "title": "The Vegetarian",
                "author": "Han Kang",
                "owner_id": 999,
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "owner not found"})
        self.assertEqual(BookListing.query.count(), 0)

    def test_get_one_listing_returns_single_resource(self):
        owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        listing = BookListing(title="Almond", author="Sohn Won-pyung", owner=owner)
        db.session.add_all([owner, listing])
        db.session.commit()

        response = self.client.get(f"/api/listings/{listing.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["listing"]["id"], listing.id)
        self.assertEqual(response.get_json()["listing"]["title"], "Almond")

    def test_get_one_listing_returns_404_for_unknown_id(self):
        response = self.client.get("/api/listings/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "listing not found"})

    def test_patch_listing_updates_owner_resource(self):
        owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        listing = BookListing(title="Old Title", author="Old Author", owner=owner)
        db.session.add_all([owner, listing])
        db.session.commit()

        response = self.client.patch(
            f"/api/listings/{listing.id}",
            json={
                "owner_id": owner.id,
                "title": "New Title",
                "availability": False,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["listing"]["title"], "New Title")
        self.assertFalse(response.get_json()["listing"]["availability"])

    def test_patch_listing_rejects_non_owner(self):
        owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        other_user = User(
            username="other",
            email="other@example.com",
            password_hash="test-hash",
            general_area="Verdun",
        )
        listing = BookListing(title="Almond", author="Sohn Won-pyung", owner=owner)
        db.session.add_all([owner, other_user, listing])
        db.session.commit()

        response = self.client.patch(
            f"/api/listings/{listing.id}",
            json={"owner_id": other_user.id, "title": "Changed"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.get_json(),
            {"error": "owner permission required"},
        )

    def test_delete_listing_removes_owner_resource(self):
        owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        listing = BookListing(title="Almond", author="Sohn Won-pyung", owner=owner)
        db.session.add_all([owner, listing])
        db.session.commit()
        listing_id = listing.id

        response = self.client.delete(
            f"/api/listings/{listing_id}",
            json={"owner_id": owner.id},
        )

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(db.session.get(BookListing, listing_id))


if __name__ == "__main__":
    unittest.main()
