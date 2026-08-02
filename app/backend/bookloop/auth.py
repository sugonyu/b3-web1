"""BookLoop의 Flask-Login session authentication 설정."""

from flask import jsonify
from flask_login import LoginManager

from .database import db


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """Session에 저장된 사용자 ID로 현재 User를 다시 불러온다."""
    from .models import User

    try:
        parsed_user_id = int(user_id)
    except (TypeError, ValueError):
        return None

    return db.session.get(User, parsed_user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """보호된 JSON API의 비로그인 요청을 일관된 401로 반환한다."""
    return jsonify({"error": "authentication required"}), 401
