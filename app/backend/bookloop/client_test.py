"""BookLoop client 제공 방식의 차이를 비교하는 개발·학습용 hub.

이 Blueprint는 제품 기능이나 자동 테스트 실행기가 아니다. 브라우저에서 Jinja,
Flask가 제공하는 Vanilla UI, JSON API와 독립 Vanilla client의 실행 경계를 비교한다.
"""

from flask import Blueprint, render_template


client_test = Blueprint("client_test", __name__)


@client_test.get("/test")
@client_test.get("/test/")
def index():
    """네 client/API 진입점과 각 실행 방식의 차이를 설명한다."""
    return render_template("test/index.html")
