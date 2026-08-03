"""BorrowRequest 생성·조회에 공통으로 사용하는 application service.

JSON API와 Python/Jinja 화면은 응답 형식이 다르지만 같은 validation,
authorization과 SQLAlchemy transaction 규칙을 사용한다.
"""

from ..database import db
from ..models import BookListing, BorrowRequest, User


class BorrowRequestServiceError(Exception):
    """route가 HTTP 응답으로 변환할 수 있는 예상된 application 오류."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def create_borrow_request(listing_id, borrower_id):
    """검증된 pending BorrowRequest를 저장하고 model 객체를 반환한다."""
    listing = db.session.get(BookListing, listing_id)

    if listing is None:
        raise BorrowRequestServiceError("listing not found", 404)

    if isinstance(borrower_id, bool) or not isinstance(borrower_id, int):
        raise BorrowRequestServiceError("borrower_id must be an integer", 400)

    borrower = db.session.get(User, borrower_id)

    if borrower is None:
        raise BorrowRequestServiceError("borrower not found", 404)

    if listing.owner_id == borrower.id:
        raise BorrowRequestServiceError("owner cannot borrow own listing", 409)

    if not listing.availability:
        raise BorrowRequestServiceError("listing is not available", 409)

    active_request = BorrowRequest.query.filter(
        BorrowRequest.listing_id == listing.id,
        BorrowRequest.borrower_id == borrower.id,
        BorrowRequest.status.in_(("pending", "approved")),
    ).first()

    if active_request is not None:
        raise BorrowRequestServiceError(
            "active borrow request already exists",
            409,
        )

    borrow_request = BorrowRequest(listing=listing, borrower=borrower)
    db.session.add(borrow_request)
    db.session.commit()

    return borrow_request


def get_authorized_borrow_request(request_id, user_id):
    """요청자 또는 listing owner에게만 지정된 BorrowRequest를 반환한다."""
    borrow_request = db.session.get(BorrowRequest, request_id)

    if borrow_request is None:
        raise BorrowRequestServiceError("borrow request not found", 404)

    allowed_user_ids = {
        borrow_request.borrower_id,
        borrow_request.listing.owner_id,
    }

    if user_id not in allowed_user_ids:
        raise BorrowRequestServiceError(
            "borrow request access forbidden",
            403,
        )

    return borrow_request
