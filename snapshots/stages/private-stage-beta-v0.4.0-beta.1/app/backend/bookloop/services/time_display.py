"""UTC database timestamp를 BookLoop 화면용 Toronto 시간으로 변환한다."""

from datetime import timezone
from zoneinfo import ZoneInfo


TORONTO_TIME_ZONE = ZoneInfo("America/Toronto")


def to_toronto_time(value):
    """SQLite가 timezone을 제거한 경우에도 UTC 기준을 명시해 변환한다."""
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(TORONTO_TIME_ZONE)


def format_toronto_datetime(value, fallback="Legacy row"):
    """날짜와 시간을 Toronto timezone label과 함께 반환한다."""
    local_value = to_toronto_time(value)
    if local_value is None:
        return fallback
    return local_value.strftime("%Y-%m-%d · %I:%M:%S %p %Z")


def format_toronto_date(value, fallback="Unknown"):
    """가입 시점처럼 시간 정밀도가 필요 없는 값을 날짜로 반환한다."""
    local_value = to_toronto_time(value)
    if local_value is None:
        return fallback
    return local_value.strftime("%b %-d, %Y")


def format_short_local_datetime(value, fallback="Legacy row"):
    """개발 표에서 지역명·초를 생략한 짧은 현지 시간으로 표시한다."""
    local_value = to_toronto_time(value)
    if local_value is None:
        return fallback
    return local_value.strftime("%b %-d · %-I:%M %p")
