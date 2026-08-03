"""BookLoop Flask 개발 서버 진입점.

AWP 참조:
/home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class18-jun-17-wed-flask-intro/01_basic_routes.py
"""

from bookloop import create_app
from bookloop.database import db


app = create_app()


if __name__ == "__main__":
    # 이 파일은 BookLoop의 로컬 개발 서버 진입점이다. 새 SQLite 파일은 파일만
    # 생기고 table은 없을 수 있으므로 첫 요청 전에 현재 model schema를 준비한다.
    # create_all()은 이미 존재하는 table이나 row를 삭제하지 않는다. 이후 migration을
    # 도입하면 이 개발 편의 단계는 Flask-Migrate 명령으로 교체할 수 있다.
    with app.app_context():
        db.create_all()

    app.run(debug=True)
