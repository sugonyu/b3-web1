"""BookLoop JSON API의 첫 blueprint.

AWP 참조:
- Blueprint:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/
- jsonify route:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class22-jul-15-wed-database-models-validation/ex/station_bike-1n-bi-nav-1.2-json-route.py

병렬공부 대응:
- Express health Router: app/backend-express/src/routes/health.js
- 현재 Express는 health route만 대응하며, 이 파일의 전체 제품 API를 복제하지 않는다.
"""

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from .db import db
from .db.models import BookListing, User
from .services.borrow_requests import (
    BorrowRequestServiceError,
    cancel_borrow_request_service,
    confirm_book_return_service,
    create_borrow_request_service,
    get_authorized_borrow_request_service,
    list_borrower_requests_service,
    list_listing_owner_requests_service,
    request_return_confirmation_service,
    update_borrow_request_status_service,
)
from .services.health import get_health_status_service


api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/health")
def health():
    """frontend와 운영 검수가 사용할 최소 상태 endpoint.

    Express의 healthRouter.get("/health")와 같은 HTTP adapter 역할이다.
    """
    return jsonify(get_health_status_service())


def listing_to_dict(listing):
    """BookListing을 개인정보가 제외된 public JSON 구조로 변환한다."""
    return {
        "id": listing.id,
        "title": listing.title,
        "author": listing.author,
        "availability": listing.availability,
        "owner": {
            "id": listing.owner.id,
            "username": listing.owner.username,
            "general_area": listing.owner.general_area,
        },
    }


def borrow_request_to_dict(borrow_request):
    """BorrowRequest를 개인정보가 제외된 public JSON 구조로 변환한다."""
    return {
        "id": borrow_request.id,
        "status": borrow_request.status,
        "listing_id": borrow_request.listing_id,
        "listing": listing_to_dict(borrow_request.listing),
        "borrower": {
            "id": borrow_request.borrower.id,
            "username": borrow_request.borrower.username,
            "general_area": borrow_request.borrower.general_area,
        },
    }


@api.get("/listings")
def get_listings():
    """BookListing collection을 ID 순서의 JSON 목록으로 반환한다."""
    listings = BookListing.query.order_by(BookListing.id).all()

    return jsonify(
        {
            "listings": [listing_to_dict(listing) for listing in listings],
        }
    )


@api.post("/listings")
def create_listing():
    """검증된 JSON으로 BookListing 하나를 collection에 추가한다."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    title = data.get("title")
    author = data.get("author")
    owner_id = data.get("owner_id")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required"}), 400

    if not isinstance(author, str) or not author.strip():
        return jsonify({"error": "author is required"}), 400

    if isinstance(owner_id, bool) or not isinstance(owner_id, int):
        return jsonify({"error": "owner_id must be an integer"}), 400

    owner = db.session.get(User, owner_id)

    if owner is None:
        return jsonify({"error": "owner not found"}), 404

    listing = BookListing(
        title=title.strip(),
        author=author.strip(),
        owner=owner,
    )
    db.session.add(listing)
    db.session.commit()

    return jsonify({"listing": listing_to_dict(listing)}), 201


@api.get("/listings/<int:listing_id>")
def get_listing(listing_id):
    """ID로 지정한 BookListing 하나를 반환한다."""
    listing = db.session.get(BookListing, listing_id)

    if listing is None:
        return jsonify({"error": "listing not found"}), 404

    return jsonify({"listing": listing_to_dict(listing)})


@api.patch("/listings/<int:listing_id>")
def update_listing(listing_id):
    """임시 owner 확인 후 BookListing의 허용된 필드만 수정한다."""
    listing = db.session.get(BookListing, listing_id)

    if listing is None:
        return jsonify({"error": "listing not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    owner_id = data.get("owner_id")

    if isinstance(owner_id, bool) or not isinstance(owner_id, int):
        return jsonify({"error": "owner_id must be an integer"}), 400

    if listing.owner_id != owner_id:
        return jsonify({"error": "owner permission required"}), 403

    changed = False

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({"error": "title cannot be blank"}), 400
        listing.title = data["title"].strip()
        changed = True

    if "author" in data:
        if not isinstance(data["author"], str) or not data["author"].strip():
            return jsonify({"error": "author cannot be blank"}), 400
        listing.author = data["author"].strip()
        changed = True

    if "availability" in data:
        if not isinstance(data["availability"], bool):
            return jsonify({"error": "availability must be boolean"}), 400
        listing.availability = data["availability"]
        changed = True

    if not changed:
        return jsonify({"error": "no editable field provided"}), 400

    db.session.commit()

    return jsonify({"listing": listing_to_dict(listing)})


@api.delete("/listings/<int:listing_id>")
def delete_listing(listing_id):
    """임시 owner 확인 후 요청 기록이 없는 BookListing을 삭제한다."""
    listing = db.session.get(BookListing, listing_id)

    if listing is None:
        return jsonify({"error": "listing not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    owner_id = data.get("owner_id")

    if isinstance(owner_id, bool) or not isinstance(owner_id, int):
        return jsonify({"error": "owner_id must be an integer"}), 400

    if listing.owner_id != owner_id:
        return jsonify({"error": "owner permission required"}), 403

    if listing.borrow_requests:
        return jsonify({"error": "listing has borrow request history"}), 409

    db.session.delete(listing)
    db.session.commit()

    return "", 204


@api.post("/listings/<int:listing_id>/requests")
@login_required
def create_borrow_request(listing_id):
    """현재 로그인 사용자의 pending 요청을 생성한다."""
    try:
        borrow_request = create_borrow_request_service(
            listing_id,
            current_user.id,
        )
    except BorrowRequestServiceError as error:
        return jsonify({"error": error.message}), error.status_code

    return jsonify({"request": borrow_request_to_dict(borrow_request)}), 201


@api.get("/requests")
@login_required
def get_borrower_requests():
    """현재 사용자가 직접 만든 BorrowRequest만 최신순으로 반환한다."""
    borrow_requests = list_borrower_requests_service(current_user.id)
    return jsonify(
        {
            "requests": [
                borrow_request_to_dict(borrow_request)
                for borrow_request in borrow_requests
            ]
        }
    )


@api.get("/listing-requests")
@login_required
def get_listing_owner_requests():
    """현재 사용자의 책에 들어온 BorrowRequest만 최신순으로 반환한다."""
    borrow_requests = list_listing_owner_requests_service(current_user.id)
    return jsonify(
        {
            "requests": [
                borrow_request_to_dict(borrow_request)
                for borrow_request in borrow_requests
            ]
        }
    )


@api.get("/requests/<int:request_id>")
@login_required
def get_borrow_request(request_id):
    """요청자 본인 또는 listing owner에게 BorrowRequest 하나를 반환한다."""
    try:
        borrow_request = get_authorized_borrow_request_service(
            request_id,
            current_user.id,
        )
    except BorrowRequestServiceError as error:
        return jsonify({"error": error.message}), error.status_code

    return jsonify({"request": borrow_request_to_dict(borrow_request)})


@api.patch("/requests/<int:request_id>")
@login_required
def update_borrow_request(request_id):
    """로그인 역할에 따라 취소 또는 owner decision 상태를 변경한다."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    next_status = data.get("status")

    try:
        if next_status == "cancelled":
            borrow_request = cancel_borrow_request_service(request_id, current_user.id)
        elif next_status == "return_pending":
            borrow_request = request_return_confirmation_service(request_id, current_user.id)
        elif next_status == "returned":
            borrow_request = confirm_book_return_service(request_id, current_user.id)
        else:
            borrow_request = update_borrow_request_status_service(
                request_id,
                current_user.id,
                next_status,
            )
    except BorrowRequestServiceError as error:
        return jsonify({"error": error.message}), error.status_code

    return jsonify({"request": borrow_request_to_dict(borrow_request)})
