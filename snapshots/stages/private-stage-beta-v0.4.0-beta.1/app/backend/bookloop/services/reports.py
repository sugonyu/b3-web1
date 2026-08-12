"""Report 생성 application service.

File: bookloop/services/reports.py
Role: BorrowRequest 당사자가 제출하는 Report의 권한·검증·저장을 담당한다.

Outline:
1. imports — database session, Report 관계 model과 category allow-list
2. ReportServiceError — 예상된 service 오류와 HTTP status 보관
3. create_report_service() — request 조회 → reporter 확인 → 상대방 결정
   → category/details 검증 → Report 저장

Flow:
caller route/form → create_report_service()
→ BorrowRequest/User 조회 → authorization
→ validation → Report(status="open") → SQLite commit → Report 반환

Behavior note: 이 파일은 service 구조를 명확히 보여주며, route/template 연결은
R3에서 별도로 구현한다.
"""

from ..db import db
from ..db.models import BorrowRequest, Report, REPORT_CATEGORIES, User


class ReportServiceError(Exception):
    """route가 HTTP 응답으로 변환할 수 있는 예상된 Report 오류."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def create_report_service(borrow_request_id, reporter_id, category, details):
    """관련 BorrowRequest 당사자가 신고를 생성하고 저장한다."""
    borrow_request = db.session.get(BorrowRequest, borrow_request_id)
    if borrow_request is None:
        raise ReportServiceError("borrow request not found", 404)

    if isinstance(reporter_id, bool) or not isinstance(reporter_id, int):
        raise ReportServiceError("reporter_id must be an integer", 400)

    reporter = db.session.get(User, reporter_id)
    if reporter is None:
        raise ReportServiceError("reporter not found", 404)

    if reporter.id == borrow_request.borrower_id:
        reported_user = borrow_request.listing.owner
    elif reporter.id == borrow_request.listing.owner_id:
        reported_user = borrow_request.borrower
    else:
        raise ReportServiceError("reporter is not a request party", 403)

    if reported_user.id == reporter.id:
        raise ReportServiceError("cannot report yourself", 409)

    if category not in REPORT_CATEGORIES:
        raise ReportServiceError("invalid report category", 400)

    if not isinstance(details, str):
        raise ReportServiceError("report details must be text", 400)

    cleaned_details = details.strip()
    if not 10 <= len(cleaned_details) <= 500:
        raise ReportServiceError(
            "report details must be between 10 and 500 characters",
            400,
        )

    report = Report(
        reporter=reporter,
        reported_user=reported_user,
        borrow_request=borrow_request,
        category=category,
        details=cleaned_details,
    )
    db.session.add(report)
    db.session.commit()
    return report


def list_reporter_reports_service(reporter_id):
    """제출자 본인의 Report만 최신순으로 반환한다."""
    return Report.query.filter_by(reporter_id=reporter_id).order_by(Report.id.desc()).all()


def get_reporter_report_detail_service(reporter_id, report_id):
    """제출자 본인에게만 해당 Report detail을 반환한다."""
    return Report.query.filter_by(id=report_id, reporter_id=reporter_id).first()
