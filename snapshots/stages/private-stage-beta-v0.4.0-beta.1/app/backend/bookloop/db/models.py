"""BookLoop의 핵심 SQLAlchemy model과 관계를 정의한다.

AWP 참조:
/home/sugonyu/jd/b2/test/test_py/b3-awp/classes/lia/models.py
"""

from datetime import datetime, timezone

from flask_login import UserMixin

from .database import db


BORROW_REQUEST_STATUSES = (
    "pending",
    "approved",
    "return_pending",
    "rejected",
    "cancelled",
    "returned",
)
DEFAULT_BORROW_REQUEST_STATUS = BORROW_REQUEST_STATUSES[0]

REPORT_STATUSES = (
    "open",
    "under_review",
    "resolved",
    "dismissed",
)
DEFAULT_REPORT_STATUS = REPORT_STATUSES[0]
REPORT_CATEGORIES = (
    "unsafe_contact",
    "no_show",
    "harassment",
    "book_condition",
    "other",
)


def utc_now():
    """새 row의 생성 시점을 timezone-aware UTC datetime으로 반환한다."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    """로그인 정보와 공개 가능한 최소 지역 정보만 저장하는 회원."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    general_area = db.Column(db.String(100), nullable=False)
    # 관리자 권한은 username이나 form 값이 아니라 DB의 server-side field로 판단한다.
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, default=utc_now)

    # 한 회원은 여러 listing을 소유하고 여러 borrow request를 만들 수 있다.
    book_listings = db.relationship("BookListing", back_populates="owner")
    borrow_requests = db.relationship("BorrowRequest", back_populates="borrower")
    submitted_reports = db.relationship(
        "Report",
        foreign_keys="Report.reporter_id",
        back_populates="reporter",
    )
    received_reports = db.relationship(
        "Report",
        foreign_keys="Report.reported_user_id",
        back_populates="reported_user",
    )

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class BookListing(db.Model):
    """한 회원이 지역사회에 공유하는 한국책 listing."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, default=utc_now)

    owner = db.relationship("User", back_populates="book_listings")
    borrow_requests = db.relationship("BorrowRequest", back_populates="listing")

    def __repr__(self):
        return f"<BookListing {self.id}: {self.title}>"


class BorrowRequest(db.Model):
    """책 listing과 요청자를 연결하고 대여 상태 변화를 기록한다."""

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.String(20),
        nullable=False,
        default=DEFAULT_BORROW_REQUEST_STATUS,
    )
    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("book_listing.id"),
        nullable=False,
    )
    borrower_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True, default=utc_now)

    listing = db.relationship("BookListing", back_populates="borrow_requests")
    borrower = db.relationship("User", back_populates="borrow_requests")
    reports = db.relationship("Report", back_populates="borrow_request")

    def __repr__(self):
        return f"<BorrowRequest {self.id}: {self.status}>"


class Report(db.Model):
    """대여 요청의 당사자가 운영자 검토를 요청한 최소 신고 기록."""

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reported_user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )
    borrow_request_id = db.Column(
        db.Integer,
        db.ForeignKey("borrow_request.id"),
        nullable=False,
    )
    category = db.Column(db.String(30), nullable=False)
    details = db.Column(db.String(500), nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default=DEFAULT_REPORT_STATUS,
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    reporter = db.relationship(
        "User",
        foreign_keys=[reporter_id],
        back_populates="submitted_reports",
    )
    reported_user = db.relationship(
        "User",
        foreign_keys=[reported_user_id],
        back_populates="received_reports",
    )
    borrow_request = db.relationship("BorrowRequest", back_populates="reports")

    def __repr__(self):
        return f"<Report {self.id}: {self.status}>"
