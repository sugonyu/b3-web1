"""BookLoop의 세 핵심 SQLAlchemy model과 관계를 정의한다."""

from flask_login import UserMixin

from .database import db


BORROW_REQUEST_STATUSES = ("pending", "approved", "rejected", "returned")
DEFAULT_BORROW_REQUEST_STATUS = BORROW_REQUEST_STATUSES[0]


class User(UserMixin, db.Model):
    """로그인 정보와 공개 가능한 최소 지역 정보만 저장하는 회원."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    general_area = db.Column(db.String(100), nullable=False)

    # 한 회원은 여러 listing을 소유하고 여러 borrow request를 만들 수 있다.
    book_listings = db.relationship("BookListing", back_populates="owner")
    borrow_requests = db.relationship("BorrowRequest", back_populates="borrower")

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class BookListing(db.Model):
    """한 회원이 지역사회에 공유하는 한국책 listing."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

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

    listing = db.relationship("BookListing", back_populates="borrow_requests")
    borrower = db.relationship("User", back_populates="borrow_requests")

    def __repr__(self):
        return f"<BorrowRequest {self.id}: {self.status}>"
