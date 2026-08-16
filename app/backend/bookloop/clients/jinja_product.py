"""Flask가 직접 렌더링하는 현재 기본 Python/Jinja 제품 client.

AWP 참조:
- Jinja template:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class18-jun-17-wed-flask-intro/03_templates.py
- Blueprint:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/

BookLoop의 `/`, Sent/Received와 Request detail 제품 route를 소유한다. Jinja route는
공유 service를 직접 호출해 HTML을 만들고, 미래 React는 JSON API를 거쳐 같은
service를 사용한다. `/jinja/` 기술 참고 route도 현재 이 Blueprint가 제공한다.

Outline:
1. imports — Flask, login, model과 shared services
2. get_request_feedback() — service error → product feedback
3. product/request routes — Books, BorrowRequest와 Request detail
4. create_report() — Report form → reports service → flash/redirect
5. profile/history/decision/return routes
6. jinja_reference() — Flask/Jinja learning reference
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
from ..services.reports import (
    ReportServiceError,
    create_report_service,
    get_reporter_report_detail_service,
    list_reporter_reports_service,
)
from ..services.book_listings import (
    BookListingServiceError,
    create_book_listing_service,
    delete_book_listing_service,
    get_owner_book_listing_service,
    list_owner_book_listings_service,
    update_book_listing_availability_service,
    update_book_listing_service,
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
        "request message is too long": {
            "title": "Message too long",
            "message": "The request message must be 500 characters or fewer.",
        },
        "request message must be a string": {
            "title": "Message not valid",
            "message": "The request message must be text.",
        },
        "return cannot be requested": {
            "title": "Return request not available",
            "message": "Only an approved exchange can begin the return confirmation flow.",
        },
        "return cannot be confirmed": {
            "title": "Return confirmation not available",
            "message": "The borrower must mark the book as returned before the owner confirms it.",
        },
        "borrow request not found": {
            "title": "Request not found",
            "message": "This borrowing request does not exist.",
        },
        "reporter is not a request party": {
            "title": "Report not allowed",
            "message": "Only the borrower or book owner can report this request.",
        },
        "invalid report category": {
            "title": "Category not allowed",
            "message": "Choose one of the available report categories.",
        },
        "report details must be text": {
            "title": "Details not valid",
            "message": "Report details must be text.",
        },
        "report details must be between 10 and 500 characters": {
            "title": "Details not valid",
            "message": "Report details must be between 10 and 500 characters.",
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


def get_book_listing_form_feedback(error):
    """BookListing service 오류를 등록·수정 화면 메시지로 바꾼다."""
    messages = {
        "title cannot be blank": "Book title is required.",
        "author cannot be blank": "Author is required.",
        "listing not found": "This book listing does not exist.",
        "owner permission required": "Only the book owner can manage this listing.",
    }
    return messages.get(error.message, "The book listing could not be saved.")


@jinja_client.get("/")
def product_home():
    """로그인 상태와 공유 가능한 책 목록을 보여주는 D2 제품 홈."""
    return render_template("bookloop/index.html", **get_product_home_context())


@jinja_client.get("/my-books/", endpoint="my_books")
@login_required
def my_books():
    """현재 로그인 사용자의 책 목록만 보여준다."""
    return render_template(
        "bookloop/my_books.html",
        listings=list_owner_book_listings_service(current_user.id),
    )


@jinja_client.route("/my-books/new", methods=["GET", "POST"], endpoint="new_book")
@login_required
def new_book():
    """현재 로그인 사용자가 새 책 listing을 등록한다."""
    form_data = {"title": "", "author": ""}

    if request.method == "POST":
        form_data = {
            "title": request.form.get("title", ""),
            "author": request.form.get("author", ""),
        }
        try:
            create_book_listing_service(
                current_user.id,
                form_data["title"],
                form_data["author"],
            )
        except BookListingServiceError as error:
            return render_template(
                "bookloop/book_form.html",
                form_data=form_data,
                form_title="Add a book",
                submit_label="Add book",
                error=get_book_listing_form_feedback(error),
            ), error.status_code

        flash("Your book was added.", "success")
        return redirect(url_for("jinja_client.my_books"))

    return render_template(
        "bookloop/book_form.html",
        form_data=form_data,
        form_title="Add a book",
        submit_label="Add book",
    )


@jinja_client.route(
    "/my-books/<int:listing_id>/edit",
    methods=["GET", "POST"],
    endpoint="edit_book",
)
@login_required
def edit_book(listing_id):
    """현재 로그인 사용자의 책 제목과 저자를 수정한다."""
    try:
        listing = get_owner_book_listing_service(listing_id, current_user.id)
    except BookListingServiceError as error:
        return render_template(
            "bookloop/request_error.html",
            feedback={
                "title": "Book management unavailable",
                "message": get_book_listing_form_feedback(error),
                "status_code": error.status_code,
                "tone": "error",
                "icon": "⛔",
            },
        ), error.status_code

    form_data = {"title": listing.title, "author": listing.author}
    if request.method == "POST":
        form_data = {
            "title": request.form.get("title", ""),
            "author": request.form.get("author", ""),
        }
        try:
            update_book_listing_service(
                listing_id,
                current_user.id,
                form_data["title"],
                form_data["author"],
            )
        except BookListingServiceError as error:
            return render_template(
                "bookloop/book_form.html",
                form_data=form_data,
                form_title="Edit your book",
                submit_label="Save changes",
                error=get_book_listing_form_feedback(error),
            ), error.status_code

        flash("Your book was updated.", "success")
        return redirect(url_for("jinja_client.my_books"))

    return render_template(
        "bookloop/book_form.html",
        form_data=form_data,
        form_title="Edit your book",
        submit_label="Save changes",
    )


@jinja_client.post(
    "/my-books/<int:listing_id>/availability",
    endpoint="change_book_availability",
)
@login_required
def change_book_availability(listing_id):
    """현재 로그인 사용자가 자신의 책 availability를 전환한다."""
    try:
        listing = get_owner_book_listing_service(listing_id, current_user.id)
        update_book_listing_availability_service(
            listing_id,
            current_user.id,
            not listing.availability,
        )
    except BookListingServiceError as error:
        return render_template(
            "bookloop/request_error.html",
            feedback={
                "title": "Availability change unavailable",
                "message": get_book_listing_form_feedback(error),
                "status_code": error.status_code,
                "tone": "error",
                "icon": "⛔",
            },
        ), error.status_code

    flash("Book availability was updated.", "success")
    return redirect(url_for("jinja_client.my_books"))


@jinja_client.post(
    "/my-books/<int:listing_id>/delete",
    endpoint="delete_book",
)
@login_required
def delete_book(listing_id):
    """현재 사용자의 request history가 없는 책을 삭제한다."""
    try:
        delete_book_listing_service(listing_id, current_user.id)
    except BookListingServiceError as error:
        feedback_message = get_book_listing_form_feedback(error)
        if error.message == "listing has borrow request history":
            feedback_message = "A book with borrow request history cannot be deleted."
        return render_template(
            "bookloop/request_error.html",
            feedback={
                "title": "Book cannot be deleted",
                "message": feedback_message,
                "status_code": error.status_code,
                "tone": "warning" if error.status_code == 409 else "error",
                "icon": "⚠️" if error.status_code == 409 else "⛔",
            },
        ), error.status_code

    flash("Your book was deleted.", "success")
    return redirect(url_for("jinja_client.my_books"))


@jinja_client.post("/listings/<int:listing_id>/request", endpoint="request_book")
@login_required
def create_borrow_request(listing_id):
    """현재 로그인 사용자의 요청을 공통 service로 생성한다."""
    try:
        borrow_request = create_borrow_request_service(
            listing_id,
            current_user.id,
            request.form.get("message", ""),
        )
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


@jinja_client.post("/requests/<int:request_id>/report", endpoint="report_request")
@login_required
def create_report(request_id):
    """현재 요청 당사자의 form을 Report service로 전달한다."""
    try:
        report = create_report_service(
            request_id,
            current_user.id,
            request.form.get("category"),
            request.form.get("details", ""),
        )
    except ReportServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback=get_request_feedback(error),
            ),
            error.status_code,
        )

    flash(f"Report #{report.id} was submitted for review.", "success")
    return redirect(url_for("jinja_client.request_detail", request_id=request_id))


@jinja_client.get("/reports/", endpoint="report_history")
@login_required
def get_report_history():
    """현재 로그인 사용자가 제출한 Report 상태만 보여준다."""
    reports = list_reporter_reports_service(current_user.id)
    return render_template("bookloop/report_history.html", reports=reports)


@jinja_client.get("/reports/<int:report_id>", endpoint="report_detail")
@login_required
def get_report_detail(report_id):
    """신고 제출자 본인에게만 Report detail을 보여준다."""
    report = get_reporter_report_detail_service(current_user.id, report_id)
    if report is None:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback={
                    "title": "Report not found",
                    "message": "This report is not available to your account.",
                    "status_code": 404,
                    "tone": "error",
                    "icon": "⛔",
                },
            ),
            404,
        )

    return render_template("bookloop/report_detail.html", report=report)


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
        "bookloop/borrower_request_history.html",
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
    """공유 health service를 보여주는 Python/Jinja 기술 참고 화면.

    Express 병렬공부 대응: app/backend-express/src/routes/ejs.js의 `/ejs/`.
    Flask의 render_template()과 Express의 response.render()를 비교한다.
    """
    # Express ejsRouter의 getHealthStatusService() 호출과 같은 service 단계다.
    # response.render("health", { health: ... })에 대응해 template에 데이터를 전달한다.
    return render_template(
        "jinja_reference/index.html",
        health=get_health_status_service(),
    )
