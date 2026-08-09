"""일반 제품 화면과 개발 도구에서 분리된 보호된 Admin route."""

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..services.admin_dashboard import (
    AdminDashboardServiceError,
    get_admin_dashboard_service,
)
from ..services.time_display import format_toronto_datetime


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.get("/")
@login_required
def dashboard():
    """관리자에게만 최소 통계와 read-only Report queue를 보여준다."""
    try:
        context = get_admin_dashboard_service(current_user.id)
    except AdminDashboardServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback={
                    "title": "Admin access denied",
                    "message": "This page is available only to an authorized administrator.",
                    "status_code": error.status_code,
                    "tone": "error",
                    "icon": "🛡️",
                },
            ),
            error.status_code,
        )

    return render_template(
        "admin/dashboard.html",
        format_toronto_datetime=format_toronto_datetime,
        **context,
    )
