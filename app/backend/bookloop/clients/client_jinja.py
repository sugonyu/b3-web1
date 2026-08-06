"""Flask가 직접 렌더링하는 optional Jinja 비교 client.

AWP 참조:
- Jinja template:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class18-jun-17-wed-flask-intro/03_templates.py
- Blueprint:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/

이 파일은 독립 JavaScript client와 구조를 비교하기 위한 학습용 경로다.
공유 health service의 Python 데이터를 Jinja template에 전달해 HTML을 만든다.
"""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..db.models import BookListing
from ..services.borrow_requests import (
    BorrowRequestServiceError,
    create_borrow_request,
    get_authorized_borrow_request,
)
from ..services.health import get_health_status


# 이 Blueprint는 Jinja로 서버 렌더링되는 화면 경로만 소유한다.
jinja_client = Blueprint("jinja_client", __name__)


@jinja_client.get("/")
def product_home():
    """로그인 상태와 공유 가능한 책 목록을 보여주는 D2 제품 홈."""
    listings = BookListing.query.order_by(BookListing.id).all()
    return render_template("bookloop/index.html", listings=listings)


@jinja_client.post("/listings/<int:listing_id>/request")
@login_required
def request_book(listing_id):
    """현재 로그인 사용자의 요청을 공통 service로 생성한다."""
    try:
        borrow_request = create_borrow_request(listing_id, current_user.id)
    except BorrowRequestServiceError as error:
        listings = BookListing.query.order_by(BookListing.id).all()
        return (
            render_template(
                "bookloop/index.html",
                listings=listings,
                error=error.message,
                existing_request_id=error.request_id,
            ),
            error.status_code,
        )

    # 저장된 request의 고유 URL로 이동해 새로고침해도 같은 row를 다시 읽는다.
    return redirect(
        url_for("jinja_client.request_detail", request_id=borrow_request.id)
    )


@jinja_client.get("/requests/<int:request_id>")
@login_required
def request_detail(request_id):
    """요청자나 책 소유자에게만 저장된 요청 결과를 보여준다."""
    try:
        borrow_request = get_authorized_borrow_request(
            request_id,
            current_user.id,
        )
    except BorrowRequestServiceError as error:
        return render_template("bookloop/request_error.html", error=error), error.status_code

    return render_template(
        "bookloop/request_detail.html",
        borrow_request=borrow_request,
    )


@jinja_client.get("/jinja/")
def jinja_reference():
    """공유 health service를 보여주는 Python/Jinja 기술 참고 화면."""
    return render_template(
        "jinja_reference/index.html",
        health=get_health_status(),
    )
