"""BookLoop에서 공유하는 SQLAlchemy database 객체.

AWP 참조:
/home/sugonyu/jd/b2/test/test_py/b3-awp/classes/lia/models.py

Outline:
1. db — shared SQLAlchemy extension object
2. application factory initializes the extension and models use it
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
