"""BookLoop 제품용 관리자 Blueprint 공개 경계.

Outline:
1. routes.admin import
2. __all__ — package public export
"""

from .routes import admin

__all__ = ["admin"]
