"""BookLoop Flask 개발 서버 진입점.

AWP 참조:
/home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class18-jun-17-wed-flask-intro/01_basic_routes.py

병렬공부 대응:
- Express 진입점: app/backend-express/src/server.js
- 둘 다 application을 만든 뒤 port를 열지만, Flask는 현재 여기서 DB schema도 준비한다.

서버 프로필:
- 기본 ``python run.py``: Main Crostini의 0.0.0.0:5000에서 안전한 LAN 데모 실행
- 로컬 디버그: FLASK_RUN_HOST=127.0.0.1 FLASK_DEBUG=true python run.py

Outline:
1. imports and Flask application factory
2. app — module-level Flask application
3. env_flag() — environment variable boolean parser
4. __main__ — local development server and database preparation
"""

import os

from bookloop import create_app
from bookloop.db import db


app = create_app()


def env_flag(name: str, default: bool = False) -> bool:
    """일반적인 환경변수 표기를 Python bool로 바꾼다."""

    fallback = "true" if default else "false"
    return os.getenv(name, fallback).strip().lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    # 이 파일은 BookLoop의 로컬 개발 서버 진입점이다. 새 SQLite 파일은 파일만
    # 생기고 table은 없을 수 있으므로 첫 요청 전에 현재 model schema를 준비한다.
    # create_all()은 이미 존재하는 table이나 row를 삭제하지 않는다. 이후 migration을
    # 도입하면 이 개발 편의 단계는 Flask-Migrate 명령으로 교체할 수 있다.
    with app.app_context():
        db.create_all()

    # Main ChromeOS에서 TCP 5000 포트 포워딩을 켜면 Rose가 Main의 LAN IP로
    # 접속할 수 있다. LAN 기본값에서는 Werkzeug debugger를 노출하지 않는다.
    # 필요한 경우 환경변수로 host/port/debug를 명시적으로 덮어쓸 수 있다.
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_RUN_PORT", "5000")),
        debug=env_flag("FLASK_DEBUG"),
    )
