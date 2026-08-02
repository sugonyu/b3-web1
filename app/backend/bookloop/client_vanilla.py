"""독립 Vanilla client 파일을 Flask 경로에서도 제공한다.

이 파일은 Python으로 화면을 만드는 client가 아니다. 별도 폴더의 순수
HTML/CSS/JavaScript를 찾아 Flask의 `/vanilla/` 경로로 전달하는 Blueprint다.
Jinja 렌더링과 JSON API 처리도 담당하지 않는다.
"""

from pathlib import Path

from flask import Blueprint, send_from_directory


# bookloop/에서 두 단계 위 app/로 이동해 독립 client 폴더의 실제 위치를 만든다.
FRONTEND_DIRECTORY = Path(__file__).resolve().parents[2] / "frontend-vanilla"

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
