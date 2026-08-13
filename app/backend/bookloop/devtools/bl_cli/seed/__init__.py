"""BL-CLI의 demo seed 기능과 Flask CLI 호환 등록 지점.

Outline:
1. register_seed_commands import
2. __all__ — CLI registration public export
"""

from .commands import register_seed_commands


__all__ = ["register_seed_commands"]
