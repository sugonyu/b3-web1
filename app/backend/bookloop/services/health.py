"""BookLoop service 상태 데이터를 한곳에서 생성한다.

병렬공부 대응:
- Express service: app/backend-express/src/services/health.js
- 두 service 모두 HTTP request/response를 모르고 상태 dict/object만 반환한다.

Outline:
1. get_health_status_service() — shared status data for API and Jinja
"""


def get_health_status_service():
    """JSON API와 Jinja template이 공유할 상태 데이터를 반환한다."""
    # Express getHealthStatusService()의 object와 같은 view/API용 상태 dict다.
    return {
        "app": "BookLoop",
        "service": "flask-api",
        "status": "ok",
        "version": "0.2.0",
    }
