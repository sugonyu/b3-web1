"""제품용 Admin Dashboard의 최소 권한과 read-only 조회 규칙.

Outline:
1. AdminDashboardServiceError
2. require_admin_service()
3. get_admin_dashboard_service()
4. get_admin_report_detail_service()
"""

from ..db import db
from ..db.models import (
    BORROW_REQUEST_STATUSES,
    BookListing,
    BorrowRequest,
    Report,
    REPORT_STATUSES,
    User,
)


class AdminDashboardServiceError(Exception):
    """관리자 권한 또는 dashboard 조회 실패를 HTTP 의미와 함께 전달한다."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def require_admin_service(user_id):
    """DB에 저장된 role만 사용해 관리자 권한을 확인한다."""
    user = db.session.get(User, user_id)
    if user is None or not user.is_admin:
        raise AdminDashboardServiceError("admin permission required", 403)
    return user


def get_admin_dashboard_service(user_id):
    """시스템 현황, 사용자 연락처, 책 공유 현황과 Report queue를 반환한다."""
    require_admin_service(user_id)

    listings = BookListing.query.order_by(BookListing.id).all()
    borrow_requests = BorrowRequest.query.all()
    reports = Report.query.order_by(Report.created_at.desc(), Report.id.desc()).all()
    users = User.query.order_by(User.id).all()

    request_status_counts = {status: 0 for status in BORROW_REQUEST_STATUSES}
    for borrow_request in borrow_requests:
        if borrow_request.status in request_status_counts:
            request_status_counts[borrow_request.status] += 1

    report_status_counts = {
        status: 0 for status in ("open", "under_review", "resolved", "dismissed")
    }
    for report in reports:
        if report.status in report_status_counts:
            report_status_counts[report.status] += 1

    listing_rows = [
        {
            "listing": listing,
            "request_count": len(listing.borrow_requests),
            "latest_request_status": (
                max(listing.borrow_requests, key=lambda request: request.id).status
                if listing.borrow_requests
                else None
            ),
            "active_request_count": sum(
                request.status in ("pending", "approved", "return_pending")
                for request in listing.borrow_requests
            ),
            # availability 규칙상 active borrower는 한 listing에 최대 한 명이다.
            "current_borrower": next(
                (
                    request.borrower
                    for request in listing.borrow_requests
                    if request.status in ("pending", "approved", "return_pending")
                ),
                None,
            ),
        }
        for listing in listings
    ]

    return {
        "system_counts": {
            "users": len(users),
            "listings": len(listings),
            "available_listings": sum(listing.availability for listing in listings),
            "active_requests": sum(
                request.status in ("pending", "approved", "return_pending")
                for request in borrow_requests
            ),
            "open_reports": report_status_counts["open"],
        },
        "users": users,
        "listing_rows": listing_rows,
        "request_status_counts": request_status_counts,
        "reports": reports,
        "report_status_counts": report_status_counts,
    }


def get_admin_report_detail_service(user_id, report_id):
    """관리자에게만 Report 원문과 관계를 read-only로 반환한다."""
    require_admin_service(user_id)
    report = db.session.get(Report, report_id)
    if report is None:
        raise AdminDashboardServiceError("report not found", 404)
    return report


def update_admin_report_status_service(user_id, report_id, status):
    """관리자가 Report 상태를 변경한다. 외부 연락은 Admin이 별도로 진행한다."""
    require_admin_service(user_id)

    if status not in REPORT_STATUSES:
        raise AdminDashboardServiceError("invalid report status", 400)

    report = db.session.get(Report, report_id)
    if report is None:
        raise AdminDashboardServiceError("report not found", 404)

    report.status = status
    db.session.commit()
    return report
