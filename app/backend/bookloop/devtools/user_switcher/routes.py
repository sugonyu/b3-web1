"""Discord의 View As와 비슷한 로컬 개발용 사용자 관점 전환 route.

실제 인증을 대체하는 기능이 아니다. DEBUG와 명시적 설정이 모두 켜진 경우에만
Tony, Mina, Alex demo 계정으로 Flask-Login session을 바꿔 권한별 화면을 점검한다.

Outline:
1. DEMO_USERNAMES and user_switcher Blueprint
2. protect_developer_tool() — explicit local/debug access gate
3. switch_user() — allowed demo session switch
"""

from flask import Blueprint, abort, current_app, redirect, url_for
from flask_login import login_user

from ...db.models import User


DEMO_USERNAMES = {"tony", "mina", "alex"}

user_switcher = Blueprint(
    "user_switcher",
    __name__,
    url_prefix="/dev/user-view",
)


@user_switcher.before_request
def protect_developer_tool():
    """운영 환경에서는 도구의 존재도 드러나지 않도록 404를 반환한다."""
    switcher_enabled = current_app.config.get(
        "ENABLE_DEV_USER_SWITCHER",
        False,
    )
    lan_switcher_enabled = current_app.config.get(
        "ENABLE_LAN_DEV_USER_SWITCHER",
        False,
    )
    if not switcher_enabled or (not current_app.debug and not lan_switcher_enabled):
        abort(404)


@user_switcher.post("/<username>")
def switch_user(username):
    """허용된 seed 사용자로만 session을 전환하고 제품 홈으로 돌아간다."""
    normalized_username = username.strip().lower()
    if normalized_username not in DEMO_USERNAMES:
        abort(404)

    user = User.query.filter_by(username=normalized_username).one_or_none()
    if user is None:
        abort(404)

    login_user(user)
    return redirect(url_for("jinja_client.product_home"))
