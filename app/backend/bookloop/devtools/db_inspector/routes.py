"""BookLoop SQLite 내용을 안전하게 읽는 개발 전용 route.

이 모듈은 제품용 Admin 기능이 아니다. 허용된 model field만 읽으며, 테스트·데모
중에는 누구나 demo BorrowRequest와 Report를 reset할 수 있다.

Outline:
1. db_inspector Blueprint
2. protect_developer_tool() — temporary test/demo boundary
3. index() — privacy-safe table display
4. reset_demo_requests() — demo BorrowRequest and Report reset action
"""

from flask import Blueprint, redirect, render_template, url_for

from ...db.models import BookListing, BorrowRequest, Report, User
from ..bl_cli.seed.commands import reset_demo_requests
from ...services.time_display import format_short_local_datetime


db_inspector = Blueprint(
    "db_inspector",
    __name__,
    url_prefix="/dev/db",
    template_folder="templates",
)


@db_inspector.before_request
def protect_developer_tool():
    """테스트·데모 기간의 임시 공개 boundary.

    테스트·데모 기간에는 조회와 demo reset을 누구에게나 열어 둔다. 이 Blueprint는
    운영 제품 기능이 아니며, reset은 BorrowRequest와 Report를 초기화한다.

    설정이나 network와 관계없이 조회와 reset을 허용한다.
    """
    return None


@db_inspector.get("")
@db_inspector.get("/")
def index():
    """네 핵심 model을 newest-first로 읽어 Inspector template에 전달한다.

    query 결과는 SQLAlchemy 객체이지만 template은 허용된 field만 명시적으로
    출력한다. 특히 User의 email과 password_hash는 절대로 화면에 표시하지 않는다.
    이 route에는 commit, flush, add, delete 호출이 없으므로 GET 전후 database
    상태가 바뀌지 않는다.
    """
    users = User.query.order_by(User.created_at.desc(), User.id.desc()).all()
    listings = BookListing.query.order_by(
        BookListing.created_at.desc(),
        BookListing.id.desc(),
    ).all()
    borrow_requests = BorrowRequest.query.order_by(
        BorrowRequest.created_at.desc(),
        BorrowRequest.id.desc(),
    ).all()
    reports = Report.query.order_by(
        Report.created_at.desc(),
        Report.id.desc(),
    ).all()

    return render_template(
        "db_inspector/index.html",
        users=users,
        listings=listings,
        borrow_requests=borrow_requests,
        reports=reports,
        format_time=format_short_local_datetime,
    )


@db_inspector.post("/reset")
def reset():
    """테스트·데모용 BorrowRequest와 Report를 초기화하고 다시 조회한다."""
    result = reset_demo_requests()
    return redirect(
        url_for("db_inspector.index", reset_deleted=result["deleted_requests"])
    )
