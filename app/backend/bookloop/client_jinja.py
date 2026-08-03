"""Flask가 직접 렌더링하는 optional Jinja 비교 client.

AWP 참조:
- Jinja template:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class18-jun-17-wed-flask-intro/03_templates.py
- Blueprint:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/

이 파일은 독립 JavaScript client와 구조를 비교하기 위한 학습용 경로다.
공유 health service의 Python 데이터를 Jinja template에 전달해 HTML을 만든다.
"""

from flask import Blueprint, render_template

from .services.health import get_health_status


# 이 Blueprint는 Jinja로 서버 렌더링되는 화면 경로만 소유한다.
jinja_client = Blueprint("jinja_client", __name__)


@jinja_client.get("/")
def product_home():
    """D2 제품 UI를 확장할 독립 BookLoop 홈의 최소 기준점을 렌더링한다."""
    return render_template("product/index.html")


@jinja_client.get("/jinja/")
def jinja_reference():
    """공유 health service를 보여주는 Python/Jinja 기술 참고 화면."""
    return render_template(
        "web/index.html",
        health=get_health_status(),
    )
