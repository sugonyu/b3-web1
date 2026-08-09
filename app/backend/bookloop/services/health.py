"""BookLoop service 상태 데이터를 한곳에서 생성한다."""


def get_health_status_service():
    """JSON API와 Jinja template이 공유할 상태 데이터를 반환한다."""
    return {
        "app": "BookLoop",
        "service": "flask-api",
        "status": "ok",
        "version": "0.2.0",
    }
