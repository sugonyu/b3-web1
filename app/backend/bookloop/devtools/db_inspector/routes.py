"""BookLoop SQLite 내용을 안전하게 읽는 개발 전용 route.

이 모듈은 제품용 Admin 기능이 아니다. GET 요청으로 허용된 model field만 읽으며,
일반 database 변경 route는 제공하지 않는다. 로컬 demo BorrowRequest reset만
명시적인 POST action으로 허용한다.

Outline:
1. db_inspector Blueprint and INTERNAL_NETWORKS allowlist
2. request_address(), is_internal_address() — local access check
3. protect_developer_tool() — development-only boundary
4. index() — privacy-safe read-only table display
5. reset_demo_requests() — local demo BorrowRequest and Report reset action
"""

from ipaddress import ip_address, ip_network

from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for
from flask_login import current_user

from ...db.models import BookListing, BorrowRequest, Report, User
from ..bl_cli.seed.commands import reset_demo_requests
from ...services.time_display import format_short_local_datetime


db_inspector = Blueprint(
    "db_inspector",
    __name__,
    url_prefix="/dev/db",
    template_folder="templates",
)


INTERNAL_NETWORKS = tuple(
    ip_network(network)
    for network in (
        "127.0.0.0/8",
        "::1/128",
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        # ChromeOS Crostini port forwarding에서 보일 수 있는 shared address 범위.
        "100.64.0.0/10",
        "fc00::/7",
        "fe80::/10",
    )
)


def request_address():
    """프록시 header를 신뢰하지 않고 직접 연결한 client IP만 해석한다."""

    try:
        return ip_address(request.remote_addr or "")
    except ValueError:
        return None


def is_internal_address(address):
    """loopback, 사설 LAN과 Crostini forwarding 범위만 허용한다."""

    return address is not None and any(address in network for network in INTERNAL_NETWORKS)


@db_inspector.before_request
def protect_developer_tool():
    """로컬 DEBUG 또는 보호된 LAN 관리자 요청만 허용한다.

    로컬 DEBUG 요청은 기존 개발 편의를 유지한다. DEBUG를 끈 LAN 데모에서는
    두 feature flag, 내부 source IP와 관리자 session을 모두 검사한다. 전달받은
    X-Forwarded-For는 신뢰하지 않고 Flask가 본 직접 연결 주소만 사용한다.

    비활성화 또는 외부 network에서는 404로 route 존재를 숨기고, 내부 network의
    로그인 사용자에게만 403으로 관리자 권한 부족을 알린다.
    """
    inspector_enabled = current_app.config.get(
        "ENABLE_DEV_DB_INSPECTOR",
        False,
    )

    if not inspector_enabled:
        abort(404)

    address = request_address()

    if current_app.debug and address is not None and address.is_loopback:
        return None

    lan_enabled = current_app.config.get(
        "ENABLE_LAN_DEV_DB_INSPECTOR",
        False,
    )

    if not lan_enabled or not is_internal_address(address):
        abort(404)

    if not current_user.is_authenticated:
        return redirect(url_for("auth.login", next=request.path))

    if not current_user.is_admin:
        abort(403)

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
    """Inspector에서 demo BorrowRequest만 초기화하고 다시 조회한다."""
    result = reset_demo_requests()
    return redirect(
        url_for("db_inspector.index", reset_deleted=result["deleted_requests"])
    )
