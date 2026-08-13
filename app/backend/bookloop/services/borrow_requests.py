"""BorrowRequest 생성·조회에 공통으로 사용하는 application service.

JSON API와 Python/Jinja 화면은 응답 형식이 다르지만 같은 validation,
authorization과 SQLAlchemy transaction 규칙을 사용한다.

Outline:
1. BorrowRequestServiceError — expected workflow errors
2. create/get_authorized_borrow_request_service() — request creation and access
3. list_borrower/list_listing_owner_requests_service() — scoped histories
4. decision and contact context services — approval privacy boundary
5. update_borrow_request_status_service() — owner decision transitions
6. return and cancel services — exchange completion workflow
"""

from ..db import db
from ..db.models import BookListing, BorrowRequest, User


class BorrowRequestServiceError(Exception):
    """route가 HTTP 응답으로 변환할 수 있는 예상된 application 오류."""

    def __init__(self, message, status_code, request_id=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        # 중복 요청처럼 이미 존재하는 resource가 있으면 browser UI가 다시 열 수 있다.
        self.request_id = request_id


def create_borrow_request_service(listing_id, borrower_id):
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
        BorrowRequest.status.in_(("pending", "approved", "return_pending")),
    ).first()

    if active_request is not None:
        raise BorrowRequestServiceError(
            "active borrow request already exists",
            409,
            request_id=active_request.id,
        )

    borrow_request = BorrowRequest(listing=listing, borrower=borrower)
    db.session.add(borrow_request)
    db.session.commit()

    return borrow_request


def get_authorized_borrow_request_service(request_id, user_id):
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


def list_borrower_requests_service(borrower_id):
    """현재 사용자가 직접 만든 BorrowRequest만 최신순으로 반환한다."""
    return (
        BorrowRequest.query.filter_by(borrower_id=borrower_id)
        .order_by(BorrowRequest.id.desc())
        .all()
    )


def list_listing_owner_requests_service(owner_id):
    """현재 사용자가 소유한 listing에 들어온 요청만 최신순으로 반환한다."""
    return (
        BorrowRequest.query.join(BookListing)
        .filter(BookListing.owner_id == owner_id)
        .order_by(BorrowRequest.id.desc())
        .all()
    )


def get_borrower_decision_context_service(borrow_request):
    """owner가 판단할 수 있는 privacy-safe borrower 집계만 반환한다."""
    borrower_requests = BorrowRequest.query.filter_by(
        borrower_id=borrow_request.borrower_id
    )
    completed_exchanges = borrower_requests.filter_by(status="returned").count()
    active_requests = borrower_requests.filter(
        BorrowRequest.status.in_(("pending", "approved", "return_pending"))
    ).count()

    return {
        "request_created_at": borrow_request.created_at,
        "member_since": borrow_request.borrower.created_at,
        "completed_exchanges": completed_exchanges,
        "active_requests": active_requests,
        "is_first_time_borrower": completed_exchanges == 0,
    }


def get_approved_contact_context_service(borrow_request, viewer_id):
    """승인된 요청의 두 당사자에게만 상대방 연락처를 반환한다."""
    if borrow_request.status not in ("approved", "return_pending"):
        return None

    if viewer_id == borrow_request.borrower_id:
        contact_user = borrow_request.listing.owner
        contact_role = "Book owner"
    elif viewer_id == borrow_request.listing.owner_id:
        contact_user = borrow_request.borrower
        contact_role = "Borrower"
    else:
        raise BorrowRequestServiceError(
            "borrow request access forbidden",
            403,
        )

    return {
        "username": contact_user.username,
        "email": contact_user.email,
        "role": contact_role,
    }


def update_borrow_request_status_service(request_id, owner_id, next_status):
    """listing owner의 허용된 결정만 저장하고 변경된 요청을 반환한다."""
    borrow_request = db.session.get(BorrowRequest, request_id)

    if borrow_request is None:
        raise BorrowRequestServiceError("borrow request not found", 404)

    # browser body가 주장하는 owner가 아니라 로그인 session ID를 받는다.
    if borrow_request.listing.owner_id != owner_id:
        raise BorrowRequestServiceError("owner permission required", 403)

    allowed_transitions = {"pending": {"approved", "rejected"}}
    if next_status not in allowed_transitions.get(borrow_request.status, set()):
        raise BorrowRequestServiceError("invalid borrow request transition", 409)

    if next_status == "approved" and not borrow_request.listing.availability:
        raise BorrowRequestServiceError("listing is not available", 409)

    borrow_request.status = next_status
    if next_status == "approved":
        borrow_request.listing.availability = False
    db.session.commit()
    return borrow_request


def request_return_confirmation_service(request_id, borrower_id):
    """borrower가 실제 반납 후 owner 확인을 요청한다."""
    borrow_request = db.session.get(BorrowRequest, request_id)
    if borrow_request is None:
        raise BorrowRequestServiceError("borrow request not found", 404)
    if borrow_request.borrower_id != borrower_id:
        raise BorrowRequestServiceError("borrower permission required", 403)
    if borrow_request.status != "approved":
        raise BorrowRequestServiceError("return cannot be requested", 409)

    borrow_request.status = "return_pending"
    db.session.commit()
    return borrow_request


def confirm_book_return_service(request_id, owner_id):
    """listing owner가 책을 받은 뒤 교환을 returned로 완료한다."""
    borrow_request = db.session.get(BorrowRequest, request_id)
    if borrow_request is None:
        raise BorrowRequestServiceError("borrow request not found", 404)
    if borrow_request.listing.owner_id != owner_id:
        raise BorrowRequestServiceError("owner permission required", 403)
    if borrow_request.status != "return_pending":
        raise BorrowRequestServiceError("return cannot be confirmed", 409)

    borrow_request.status = "returned"
    borrow_request.listing.availability = True
    db.session.commit()
    return borrow_request


def cancel_borrow_request_service(request_id, borrower_id):
    """요청자 본인이 아직 pending인 요청만 취소한다."""
    borrow_request = db.session.get(BorrowRequest, request_id)

    if borrow_request is None:
        raise BorrowRequestServiceError("borrow request not found", 404)

    if borrow_request.borrower_id != borrower_id:
        raise BorrowRequestServiceError("borrower permission required", 403)

    if borrow_request.status != "pending":
        raise BorrowRequestServiceError("borrow request cannot be cancelled", 409)

    borrow_request.status = "cancelled"
    db.session.commit()
    return borrow_request
