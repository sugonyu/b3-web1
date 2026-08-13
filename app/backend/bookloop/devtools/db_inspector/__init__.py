"""개발용 database inspector Blueprint를 공개한다.

Outline:
1. routes.db_inspector import
2. __all__ — package public export
"""

from .routes import db_inspector


__all__ = ["db_inspector"]
