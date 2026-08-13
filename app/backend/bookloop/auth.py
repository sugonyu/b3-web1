"""BookLoop의 Flask-Login session authentication 설정과 browser route.

Outline:
1. login_manager and auth Blueprint
2. load_user(), unauthorized() — session restoration and 401/redirect split
3. safe_next_url() — local redirect validation
4. login(), register(), logout() — browser authentication routes
"""

from urllib.parse import urlsplit

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .db import db


login_manager = LoginManager()
auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    """Session에 저장된 사용자 ID로 현재 User를 다시 불러온다."""
    from .db.models import User

    try:
        parsed_user_id = int(user_id)
    except (TypeError, ValueError):
        return None

    return db.session.get(User, parsed_user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """API에는 401 JSON을, browser 화면에는 로그인 이동을 반환한다."""
    if request.blueprint == "api":
        return jsonify({"error": "authentication required"}), 401

    if request.method == "GET":
        return redirect(url_for("auth.login", next=request.path))

    return redirect(url_for("auth.login"))


def safe_next_url(candidate):
    """외부 사이트 redirect를 막고 이 Flask 앱 안의 path만 허용한다."""
    if not candidate:
        return None

    parsed = urlsplit(candidate)
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
        return None

    return candidate


@auth.route("/login", methods=["GET", "POST"])
def login():
    """username과 password를 검증하고 Flask-Login session을 시작한다."""
    from .db.models import User

    if current_user.is_authenticated:
        return redirect(url_for("jinja_client.product_home"))

    error = None
    status_code = 200
    next_url = safe_next_url(request.values.get("next"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).one_or_none()

        if user is None or not check_password_hash(user.password_hash, password):
            # 어떤 값이 틀렸는지 구분하지 않아 존재하는 계정을 추측하기 어렵게 한다.
            error = "Invalid username or password."
            status_code = 401
        else:
            login_user(user)
            return redirect(next_url or url_for("jinja_client.product_home"))

    return render_template(
        "auth/login.html",
        error=error,
        next_url=next_url,
    ), status_code


@auth.route("/register", methods=["GET", "POST"])
def register():
    """새 User를 만들고 같은 browser request에서 로그인 session을 시작한다."""
    from .db.models import User

    if current_user.is_authenticated:
        return redirect(url_for("jinja_client.product_home"))

    error = None
    status_code = 200

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        general_area = request.form.get("general_area", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not general_area or not password:
            error = "All fields are required."
            status_code = 400
        elif User.query.filter(
            (User.username == username) | (User.email == email)
        ).first():
            error = "Username or email is already registered."
            status_code = 409
        else:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                general_area=general_area,
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("jinja_client.product_home"))

    return render_template("auth/register.html", error=error), status_code


@auth.post("/logout")
@login_required
def logout():
    """현재 browser session을 종료하고 제품 홈으로 돌아간다."""
    logout_user()
    return redirect(url_for("jinja_client.product_home"))
