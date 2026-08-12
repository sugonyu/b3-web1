"""Reporting MVP service tests.

File: tests/test_reports_service.py
Role: `create_report_service()`의 성공·권한·검증 경계를 작은 fixture로 확인한다.

Outline:
1. ReportServiceTest.setUp() — memory SQLite와 세 사용자/request 준비
2. ReportServiceTest.tearDown() — session과 table 정리
3. borrower/owner valid create tests
4. unrelated/self-report authorization tests
5. category/details/request validation tests
"""

import unittest

from bookloop import create_app
from bookloop.db import db
from bookloop.db.models import BookListing, BorrowRequest, Report, User
from bookloop.services.reports import ReportServiceError, create_report_service


class ReportServiceTest(unittest.TestCase):
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

        self.owner = User(
            username="owner",
            email="owner@example.com",
            password_hash="test-hash",
            general_area="Montreal",
        )
        self.borrower = User(
            username="borrower",
            email="borrower@example.com",
            password_hash="test-hash",
            general_area="Verdun",
        )
        self.unrelated = User(
            username="unrelated",
            email="unrelated@example.com",
            password_hash="test-hash",
            general_area="NDG",
        )
        self.listing = BookListing(
            title="The Odyssey",
            author="Homer",
            owner=self.owner,
        )
        self.borrow_request = BorrowRequest(
            listing=self.listing,
            borrower=self.borrower,
        )
        db.session.add_all(
            [self.owner, self.borrower, self.unrelated, self.listing, self.borrow_request]
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_borrower_can_report_and_server_derives_owner(self):
        report = create_report_service(
            self.borrow_request.id,
            self.borrower.id,
            "no_show",
            "The arranged exchange did not happen.",
        )

        self.assertIsInstance(report, Report)
        self.assertEqual(report.reporter_id, self.borrower.id)
        self.assertEqual(report.reported_user_id, self.owner.id)
        self.assertEqual(report.status, "open")
        self.assertEqual(report.details, "The arranged exchange did not happen.")

    def test_owner_can_report_and_server_derives_borrower(self):
        report = create_report_service(
            self.borrow_request.id,
            self.owner.id,
            "book_condition",
            "The book was returned with new damage.",
        )

        self.assertEqual(report.reporter_id, self.owner.id)
        self.assertEqual(report.reported_user_id, self.borrower.id)

    def test_unrelated_user_is_forbidden(self):
        with self.assertRaisesRegex(ReportServiceError, "not a request party") as context:
            create_report_service(
                self.borrow_request.id,
                self.unrelated.id,
                "other",
                "This user is not part of the exchange.",
            )

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(Report.query.count(), 0)

    def test_self_report_is_rejected(self):
        self.borrow_request.borrower_id = self.owner.id
        db.session.commit()

        with self.assertRaisesRegex(ReportServiceError, "cannot report yourself") as context:
            create_report_service(
                self.borrow_request.id,
                self.owner.id,
                "other",
                "The exchange participant cannot report themselves.",
            )

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(Report.query.count(), 0)

    def test_invalid_category_is_rejected(self):
        with self.assertRaisesRegex(ReportServiceError, "invalid report category"):
            create_report_service(
                self.borrow_request.id,
                self.borrower.id,
                "spam",
                "This category is not allowed.",
            )

        self.assertEqual(Report.query.count(), 0)

    def test_details_must_be_between_10_and_500_characters(self):
        for details in ("too short", "x" * 501):
            with self.assertRaisesRegex(ReportServiceError, "between 10 and 500"):
                create_report_service(
                    self.borrow_request.id,
                    self.borrower.id,
                    "other",
                    details,
                )

        self.assertEqual(Report.query.count(), 0)

    def test_unknown_request_is_not_found(self):
        with self.assertRaisesRegex(ReportServiceError, "borrow request not found") as context:
            create_report_service(
                999,
                self.borrower.id,
                "other",
                "The request no longer exists in the system.",
            )

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
