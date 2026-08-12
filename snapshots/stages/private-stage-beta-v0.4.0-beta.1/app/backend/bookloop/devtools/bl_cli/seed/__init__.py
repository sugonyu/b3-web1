"""BL-CLI의 demo seed 기능과 Flask CLI 호환 등록 지점."""

from .commands import register_seed_commands


__all__ = ["register_seed_commands"]
