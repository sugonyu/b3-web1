"""BookLoop client 제공 방식의 차이를 비교하는 개발·학습용 hub.

이 Blueprint는 제품 기능이나 자동 테스트 실행기가 아니다. 브라우저에서 Jinja,
Flask가 제공하는 Vanilla UI, JSON API와 독립 Vanilla client의 실행 경계를 비교한다.
"""

from flask import Blueprint, render_template


test_hub = Blueprint(
    "test_hub",
    __name__,
    template_folder="templates",
)


@test_hub.get("/test")
@test_hub.get("/test/")
def index():
    """제품 client, API와 개발 도구 진입점의 차이를 설명한다."""
    return render_template("test_hub/index.html")
