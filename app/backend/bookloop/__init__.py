"""BookLoop Flask application factory.

AWP 참조:
- Flask app 설정과 db.init_app():
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/lia/app.py
- Blueprint 등록 흐름:
  /home/sugonyu/jd/b2/test/test_py/b3-awp/classes/class19-jul-07-tue-flask-blueprints/

병렬공부 대응:
- Express app factory: app/backend-express/src/app.js의 createApp()
- Flask는 extension과 Blueprint를, Express는 middleware와 Router를 조립한다.

Outline:
1. environment loading and Flask extension imports
2. create_app() — configuration and extension setup
3. Blueprint registration — auth, product clients, API, Admin and devtools
4. local schema and CLI seed registration
"""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .api import api
from .admin import admin
from .auth import auth, login_manager
from .db import db
from .clients import jinja_client, vanilla_client
from .devtools.db_inspector import db_inspector
from .devtools.user_switcher import user_switcher
from .devtools.test_hub import test_hub
from .devtools.bl_cli.seed import register_seed_commands


def create_app(test_config=None):
    """설정과 extension, API blueprint를 연결해 Flask 앱을 생성한다."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "sqlite:///bookloop.db",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # 개발 DB Inspector는 명시적으로 true를 설정해야만 요청을 허용한다.
        # DEBUG도 함께 검사하므로 운영 환경에서 실수로 내부 데이터가 노출되지 않는다.
        ENABLE_DEV_DB_INSPECTOR=os.getenv(
            "ENABLE_DEV_DB_INSPECTOR",
            "false",
        ).lower()
        in {"1", "true", "yes", "on"},
        # DEBUG를 끈 LAN 데모에서 Inspector를 열 때 필요한 별도 opt-in이다.
        # route는 이 설정 외에도 내부 IP와 관리자 session을 검사한다.
        ENABLE_LAN_DEV_DB_INSPECTOR=os.getenv(
            "ENABLE_LAN_DEV_DB_INSPECTOR",
            "false",
        ).lower()
        in {"1", "true", "yes", "on"},
        # seed 사용자 관점 전환도 DEBUG와 별도 opt-in 설정이 모두 필요하다.
        ENABLE_DEV_USER_SWITCHER=os.getenv(
            "ENABLE_DEV_USER_SWITCHER",
            "false",
        ).lower()
        in {"1", "true", "yes", "on"},
        # Rose LAN 개발 단계에서만 별도 opt-in으로 View-as-user를 허용한다.
        ENABLE_LAN_DEV_USER_SWITCHER=os.getenv(
            "ENABLE_LAN_DEV_USER_SWITCHER",
            "false",
        ).lower()
        in {"1", "true", "yes", "on"},
    )

    if test_config:
        app.config.update(test_config)

    # 테스트에서는 환경 파일의 LAN 개발 도구가 화면에 섞이지 않도록 끈다.
    if app.config.get("TESTING") and not (
        test_config and test_config.get("ENABLE_LAN_DEV_USER_SWITCHER")
    ):
        app.config["ENABLE_LAN_DEV_USER_SWITCHER"] = False

    db.init_app(app)
    login_manager.init_app(app)

    # db.create_all()이 네 model을 찾을 수 있도록 metadata에 등록한다.
    from .db import models  # noqa: F401

    # Private Stage B0: VS Code Live Preview(3000)에서 Flask API(5000) 호출 허용.
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://127.0.0.1:3000",
                    "http://localhost:3000",
                    "http://127.0.0.1:8080",
                    "http://localhost:8080",
                ]
            }
        },
    )

    app.register_blueprint(api)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(vanilla_client)
    # Express createApp()의 app.use("/ejs", ejsRouter)와 같은 route module 등록이다.
    # Flask Blueprint는 /jinja/에서 Jinja를, Express Router는 /ejs/에서 EJS를 render한다.
    app.register_blueprint(jinja_client)
    app.register_blueprint(test_hub)
    # Blueprint는 항상 등록하고 route의 before_request에서 실행 시점 설정을 검사한다.
    # app.run(debug=True)가 create_app() 뒤에 DEBUG를 켜기 때문에 이 순서가 필요하다.
    app.register_blueprint(db_inspector)
    app.register_blueprint(user_switcher)
    # 데모 시작 데이터는 HTTP route가 아니라 명시적인 Flask CLI 명령으로만 만든다.
    register_seed_commands(app)

    # SQLite 파일을 둘 instance 폴더가 항상 존재하도록 한다.
    os.makedirs(app.instance_path, exist_ok=True)

    return app
