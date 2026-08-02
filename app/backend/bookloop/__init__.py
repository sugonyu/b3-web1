"""BookLoop Flask application factory."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .api import api
from .auth import login_manager
from .database import db
from .client_jinja import jinja_client
from .client_vanilla import vanilla_client


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
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    # db.create_all()이 세 model을 찾을 수 있도록 metadata에 등록한다.
    from . import models  # noqa: F401

    # Allow the documented local static clients to call the Flask API.
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
    app.register_blueprint(vanilla_client)
    app.register_blueprint(jinja_client)

    # SQLite 파일을 둘 instance 폴더가 항상 존재하도록 한다.
    os.makedirs(app.instance_path, exist_ok=True)

    return app
