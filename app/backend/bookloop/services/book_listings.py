"""현재 로그인 사용자의 BookListing 관리 service."""

from ..db import db
from ..db.models import BookListing


class BookListingServiceError(Exception):
    """route가 제품 화면 응답으로 바꿀 수 있는 예상된 listing 오류."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def list_owner_book_listings_service(owner_id):
    """현재 로그인 사용자의 책만 최신 등록 순서로 반환한다."""
    return (
        BookListing.query.filter_by(owner_id=owner_id)
        .order_by(BookListing.id.desc())
        .all()
    )


def get_owner_book_listing_service(listing_id, owner_id):
    """지정 listing이 현재 로그인 사용자의 소유인지 확인한다."""
    listing = db.session.get(BookListing, listing_id)

    if listing is None:
        raise BookListingServiceError("listing not found", 404)

    if listing.owner_id != owner_id:
        raise BookListingServiceError("owner permission required", 403)

    return listing


def create_book_listing_service(owner_id, title, author):
    """필수 문자열을 검증하고 현재 사용자의 새 책을 저장한다."""
    clean_title = _required_text(title, "title")
    clean_author = _required_text(author, "author")

    listing = BookListing(
        title=clean_title,
        author=clean_author,
        owner_id=owner_id,
        availability=True,
    )
    db.session.add(listing)
    db.session.commit()
    return listing


def update_book_listing_service(listing_id, owner_id, title, author):
    """현재 사용자의 책 제목과 저자만 수정한다."""
    listing = get_owner_book_listing_service(listing_id, owner_id)
    listing.title = _required_text(title, "title")
    listing.author = _required_text(author, "author")
    db.session.commit()
    return listing


def update_book_listing_availability_service(listing_id, owner_id, availability):
    """현재 사용자의 책 availability만 변경한다."""
    listing = get_owner_book_listing_service(listing_id, owner_id)

    if not isinstance(availability, bool):
        raise BookListingServiceError("availability must be boolean", 400)

    listing.availability = availability
    db.session.commit()
    return listing


def delete_book_listing_service(listing_id, owner_id):
    """현재 사용자의 request history가 없는 책 listing만 삭제한다."""
    listing = get_owner_book_listing_service(listing_id, owner_id)

    if listing.borrow_requests:
        raise BookListingServiceError("listing has borrow request history", 409)

    db.session.delete(listing)
    db.session.commit()


def _required_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise BookListingServiceError(f"{field_name} cannot be blank", 400)
    return value.strip()
