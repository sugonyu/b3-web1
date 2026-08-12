"""일반 제품 화면과 개발 도구에서 분리된 보호된 Admin route."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..services.admin_dashboard import (
    AdminDashboardServiceError,
    get_admin_dashboard_service,
    get_admin_report_detail_service,
    update_admin_report_status_service,
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


@admin.get("/reports/<int:report_id>")
@login_required
def report_detail(report_id):
    """관리자에게만 Report 내용과 관계를 보여주는 read-only detail."""
    try:
        report = get_admin_report_detail_service(current_user.id, report_id)
    except AdminDashboardServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback={
                    "title": "Report unavailable",
                    "message": "This report does not exist." if error.status_code == 404 else "This page is available only to an authorized administrator.",
                    "status_code": error.status_code,
                    "tone": "error",
                    "icon": "🛡️",
                },
            ),
            error.status_code,
        )

    return render_template(
        "admin/report_detail.html",
        report=report,
        format_toronto_datetime=format_toronto_datetime,
    )


@admin.post("/reports/<int:report_id>/status")
@login_required
def update_report_status(report_id):
    """관리자가 Report 상태를 저장하고 detail 화면으로 돌아간다."""
    try:
        report = update_admin_report_status_service(
            current_user.id,
            report_id,
            request.form.get("status", ""),
        )
    except AdminDashboardServiceError as error:
        return (
            render_template(
                "bookloop/request_error.html",
                feedback={
                    "title": "Report update unavailable",
                    "message": (
                        "Choose a valid report status."
                        if error.status_code == 400
                        else "This report does not exist."
                        if error.status_code == 404
                        else "This page is available only to an authorized administrator."
                    ),
                    "status_code": error.status_code,
                    "tone": "error",
                    "icon": "🛡️",
                },
            ),
            error.status_code,
        )

    flash(f"Report #{report.id} status changed to {report.status.replace('_', ' ').title()}.", "success")
    return redirect(url_for("admin.report_detail", report_id=report.id))
