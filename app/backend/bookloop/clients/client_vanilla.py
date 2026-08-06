"""Flask 전용 Vanilla client 파일을 `/vanilla/` 경로로 제공한다.

AWP 참조:
/home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/

이 파일은 Python으로 화면을 만드는 client가 아니다. `bookloop/flask_vanilla/`에
보관한 Flask 전용 HTML/CSS/JavaScript 복사본을 `/vanilla/` 경로로 전달하는
Blueprint다. 독립 JS Vanilla client는 `app/frontend/js-vanilla/`에서
Port 8080으로 실행한다.
Jinja 렌더링과 JSON API 처리도 담당하지 않는다.
"""

from pathlib import Path

from flask import Blueprint, send_from_directory


# Flask와 독립 JS 실행 경계를 분리하기 위한 Flask 전용 복사본.
FRONTEND_DIRECTORY = Path(__file__).resolve().parents[1] / "flask_vanilla"

# 이 Blueprint는 정적 Vanilla client의 보조 제공 경로만 소유한다.
vanilla_client = Blueprint(
    "vanilla_client",
    __name__,
    url_prefix="/vanilla",
    static_folder=str(FRONTEND_DIRECTORY),
    static_url_path="",
)


@vanilla_client.get("/")
def index():
    """독립 Vanilla client의 시작 파일인 index.html을 반환한다."""
    return send_from_directory(FRONTEND_DIRECTORY, "index.html")
