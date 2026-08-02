"""Flask가 직접 렌더링하는 optional Jinja 비교 client.

이 파일은 독립 JavaScript client와 구조를 비교하기 위한 경로다.
공유 health service의 Python 데이터를 Jinja template에 전달해 HTML을 만든다.
"""

from flask import Blueprint, render_template

from .services.health import get_health_status


# 이 Blueprint는 Jinja로 서버 렌더링되는 화면 경로만 소유한다.
jinja_client = Blueprint("jinja_client", __name__)


@jinja_client.get("/")
@jinja_client.get("/jinja/")
def index():
    """공유 service 데이터를 template에 전달해 Jinja HTML을 렌더링한다."""
    return render_template(
        "web/index.html",
        health=get_health_status(),
    )
