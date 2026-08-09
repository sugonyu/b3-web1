"""Flask가 직접 렌더링하는 현재 기본 Python/Jinja 제품 client.

AWP 참조:
- Jinja template:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class18-jun-17-wed-flask-intro/03_templates.py
- Blueprint:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/

BookLoop의 `/`, Sent/Received와 Request detail 제품 route를 소유한다. Jinja route는
공유 service를 직접 호출해 HTML을 만들고, 미래 React는 JSON API를 거쳐 같은
service를 사용한다. `/jinja/` 기술 참고 route도 현재 이 Blueprint가 제공한다.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..db.models import BookListing
from ..services.borrow_requests import (
    BorrowRequestServiceError,
    cancel_borrow_request_service,
    confirm_book_return_service,
    create_borrow_request_service,
    get_approved_contact_context_service,
    get_borrower_decision_context_service,
    get_authorized_borrow_request_service,
    list_borrower_requests_service,
    list_listing_owner_requests_service,
    request_return_confirmation_service,
    update_borrow_request_status_service,
)
from ..services.health import get_health_status_service
from ..services.time_display import format_toronto_date, format_toronto_datetime
from ..services.user_profiles import get_public_user_profile_service


# 이 Blueprint는 Jinja로 서버 렌더링되는 화면 경로만 소유한다.
jinja_client = Blueprint("jinja_client", __name__)


def get_request_feedback(error):
    """service 오류를 HTTP code를 보존한 사용자용 제품 메시지로 바꾼다."""
    messages = {
        "active borrow request already exists": {
            "title": "Request already exists",
            "message": "You already have an active request for this book.",
        },
        "owner cannot borrow own listing": {
            "title": "This is your book",
            "message": "You cannot request a book that you own.",
        },
        "listing is not available": {
            "title": "Book unavailable",
            "message": "This book is not available for a new request.",
        },
        "listing not found": {
            "title": "Book not found",
            "message": "This book listing does not exist.",
        },
        "borrow request access forbidden": {
            "title": "Access denied",
            "message": "Only the borrower or book owner can view this request.",
        },
        "borrow request not found": {
            "title": "Request not found",
            "message": "This borrowing request does not exist.",
        },
        "owner permission required": {
            "title": "Decision not allowed",
            "message": "Only the owner of this book can decide this request.",
        },
        "invalid borrow request transition": {
            "title": "Decision already completed",
            "message": "This request cannot move to the selected status.",
        },
        "borrower permission required": {
            "title": "Cancellation not allowed",
            "message": "Only the borrower who created this request can cancel it.",
        },
        "borrow request cannot be cancelled": {
            "title": "Request cannot be cancelled",
            "message": "Only a pending request can be cancelled.",
        },
        "return cannot be requested": {
            "title": "Return request not available",
            "message": "Only an approved exchange can begin the return confirmation flow.",
        },
        "return cannot be confirmed": {
            "title": "Return confirmation not available",
            "message": "The borrower must mark the book as returned before the owner confirms it.",
        },
    }
    feedback = messages.get(
        error.message,
        {
            "title": "Request unavailable",
            "message": "The request could not be completed.",
        },
    )
    return {
        **feedback,
        "status_code": error.status_code,
        "tone": "warning" if error.status_code == 409 else "error",
        "icon": "⚠️" if error.status_code == 409 else "⛔",
    }


def get_product_home_context():
    """제품 홈의 listing과 로그인 사용자별 request 개수를 준비한다."""
    context = {
        "listings": BookListing.query.order_by(BookListing.id).all(),
        "borrower_request_count": 0,
        "owner_request_count": 0,
        "active_request_listing_ids": set(),
    }
    if current_user.is_authenticated:
        borrower_requests = list_borrower_requests_service(current_user.id)
        context["borrower_request_count"] = len(borrower_requests)
        context["owner_request_count"] = len(
            list_listing_owner_requests_service(current_user.id)
        )
        context["active_request_listing_ids"] = {
            borrow_request.listing_id
            for borrow_request in borrower_requests
            if borrow_request.status in ("pending", "approved", "return_pending")
        }
    return context


@jinja_client.get("/")
def product_home():
    """로그인 상태와 공유 가능한 책 목록을 보여주는 D2 제품 홈."""
    return render_template("bookloop/index.html", **get_product_home_context())


@jinja_client.post("/listings/<int:listing_id>/request", endpoint="request_book")
@login_required
def create_borrow_request(listing_id):
    """현재 로그인 사용자의 요청을 공통 service로 생성한다."""
    try:
        borrow_request = create_borrow_request_service(listing_id, current_user.id)
    except BorrowRequestServiceError as error:
        context = get_product_home_context()
        context.update(
            feedback=get_request_feedback(error),
            existing_request_id=error.request_id,
        )
        return (
            render_template("bookloop/index.html", **context),
            error.status_code,
        )

    # 저장된 request의 고유 URL로 이동해 새로고침해도 같은 row를 다시 읽는다.
    return redirect(
        url_for("jinja_client.request_detail", request_id=borrow_request.id)
    )


@jinja_client.get("/requests/<int:request_id>", endpoint="request_detail")
@login_required
def get_borrow_request(request_id):
    """요청자나 책 소유자에게만 저장된 요청 결과를 보여준다."""
    try:
        borrow_request = get_authorized_borrow_request_service(
            request_id,
            current_user.id,
        )
    except BorrowRequestServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback=get_request_feedback(error),
            ),
            error.status_code,
        )

    decision_context = None
    if current_user.id == borrow_request.listing.owner_id:
        decision_context = get_borrower_decision_context_service(borrow_request)

    approved_contact = get_approved_contact_context_service(
        borrow_request,
        current_user.id,
    )

    return render_template(
        "bookloop/request_detail.html",
        borrow_request=borrow_request,
        approved_contact=approved_contact,
        decision_context=decision_context,
        format_toronto_date=format_toronto_date,
        format_toronto_datetime=format_toronto_datetime,
    )


@jinja_client.get("/users/<int:user_id>", endpoint="user_profile")
@login_required
def get_user_profile(user_id):
    """로그인 사용자에게 privacy-safe 읽기 전용 profile을 보여준다."""
    profile = get_public_user_profile_service(user_id, current_user.id)
    if profile is None:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback={
                    "title": "Profile not found",
                    "message": "This member profile does not exist.",
                    "status_code": 404,
                    "tone": "error",
                    "icon": "⛔",
                },
            ),
            404,
        )

    return render_template(
        "bookloop/user_profile.html",
        profile=profile,
        format_toronto_date=format_toronto_date,
    )

@jinja_client.get("/requests/", endpoint="borrower_request_history")
@login_required
def get_borrower_requests():
    """로그인 사용자가 직접 만든 요청만 보여주는 D3 목록 화면."""
    borrow_requests = list_borrower_requests_service(current_user.id)
    return render_template(
        "bookloop/request_history.html",
        borrow_requests=borrow_requests,
    )


@jinja_client.post("/requests/<int:request_id>/cancel", endpoint="cancel_request")
@login_required
def cancel_borrow_request(request_id):
    """borrower가 owner 결정 전 pending request를 취소한다."""
    try:
        borrow_request = cancel_borrow_request_service(request_id, current_user.id)
    except BorrowRequestServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback=get_request_feedback(error),
            ),
            error.status_code,
        )

    flash(f"Request #{borrow_request.id} was cancelled.", "success")
    return redirect(url_for("jinja_client.borrower_request_history"))


@jinja_client.get("/listing-requests/", endpoint="listing_owner_request_history")
@login_required
def get_listing_owner_requests():
    """로그인 사용자가 소유한 책에 들어온 요청만 보여주는 D3 화면."""
    borrow_requests = list_listing_owner_requests_service(current_user.id)
    return render_template(
        "bookloop/owner_request_history.html",
        borrow_requests=borrow_requests,
    )


@jinja_client.post("/requests/<int:request_id>/decision", endpoint="decide_borrow_request")
@login_required
def update_borrow_request(request_id):
    """책 소유자가 pending 요청을 승인하거나 거절한다."""
    next_status = request.form.get("status")
    try:
        borrow_request = update_borrow_request_status_service(
            request_id,
            current_user.id,
            next_status,
        )
    except BorrowRequestServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback=get_request_feedback(error),
            ),
            error.status_code,
        )

    flash(
        f"Request #{borrow_request.id} was {borrow_request.status}.",
        "success",
    )
    return redirect(url_for("jinja_client.listing_owner_request_history"))


@jinja_client.post("/requests/<int:request_id>/return", endpoint="request_book_return")
@login_required
def request_return_confirmation(request_id):
    """borrower가 실제 반납 후 owner의 확인을 요청한다."""
    try:
        borrow_request = request_return_confirmation_service(request_id, current_user.id)
    except BorrowRequestServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback=get_request_feedback(error),
            ),
            error.status_code,
        )

    flash(f"Request #{borrow_request.id} is waiting for owner return confirmation.", "success")
    return redirect(url_for("jinja_client.request_detail", request_id=request_id))


@jinja_client.post("/requests/<int:request_id>/confirm-return", endpoint="confirm_return")
@login_required
def confirm_book_return(request_id):
    """owner가 책을 받은 뒤 교환 완료와 listing 재공개를 확정한다."""
    try:
        borrow_request = confirm_book_return_service(request_id, current_user.id)
    except BorrowRequestServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback=get_request_feedback(error),
            ),
            error.status_code,
        )

    flash(f"Request #{borrow_request.id} was returned. The book is available again.", "success")
    return redirect(url_for("jinja_client.request_detail", request_id=request_id))


@jinja_client.get("/jinja/")
def jinja_reference():
    """공유 health service를 보여주는 Python/Jinja 기술 참고 화면."""
    return render_template(
        "jinja_reference/index.html",
        health=get_health_status_service(),
    )
