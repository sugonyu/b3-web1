# BookLoop 코드 아웃라인 매뉴얼

이 문서는 PyCharm에서 BookLoop 코드를 처음 열 때 **목적 → 파일 연결 → 진입점
→ 파일 역할 → 다음 리뷰 포인트** 순서로 읽기 위한 학습용 지도다.

## 1. 전체 실행 흐름

```text
backend/run.py
→ bookloop.create_app()
→ Flask route / Jinja template
→ shared service
→ SQLAlchemy model
→ SQLite database
→ 화면 feedback 또는 JSON response
```

Reporting의 현재 흐름은 다음과 같다.

```text
BorrowRequest detail form (R3 예정)
→ bookloop.services.reports.create_report_service()
→ BorrowRequest/User 권한 확인
→ 상대방 자동 결정
→ category/details 검증
→ Report(status="open") 저장
→ Admin read-only report queue
```

## 2. 파일 역할

| 순서 | 파일 | 역할 |
| --- | --- | --- |
| 1 | `run.py` | 개발 서버 시작점 |
| 2 | `bookloop/__init__.py` | `create_app()` application factory |
| 3 | `bookloop/clients/jinja_product.py` | Python/Jinja 화면 route와 form adapter |
| 4 | `bookloop/services/borrow_requests.py` | BorrowRequest 업무 규칙 |
| 5 | `bookloop/services/reports.py` | Report 권한·검증·저장 규칙 |
| 6 | `bookloop/db/models.py` | User, BookListing, BorrowRequest, Report 관계 |
| 7 | `bookloop/admin/routes.py` | 보호된 Admin 화면 진입 |
| 8 | `bookloop/services/admin_dashboard.py` | Admin 통계, Report 상태 변경과 연락처 조회 |
| 9 | `bookloop/templates/bookloop/` | 사용자 화면 |
| 10 | `bookloop/templates/admin/` | Admin 화면 |
| 11 | `tests/` | service, route, model, authorization 검증 |

## 3. Reporting 파일 아웃라인

### `services/reports.py`

```text
module docstring
├── imports
├── ReportServiceError
│   └── message / status_code
└── create_report_service()
    ├── BorrowRequest 조회
    ├── reporter ID 형식·존재 확인
    ├── borrower 또는 listing owner인지 확인
    ├── reported user를 상대 당사자로 server-side 결정
    ├── category allow-list 확인
    ├── details trim + 10~500자 확인
    ├── Report(status="open") 생성
    ├── db.session.commit()
    └── Report 반환
```

### `tests/test_reports_service.py`

```text
setUp() — memory SQLite와 owner/borrower/unrelated/request fixture
tearDown() — session과 tables 정리
test_borrower_can_report_and_server_derives_owner()
test_owner_can_report_and_server_derives_borrower()
test_unrelated_user_is_forbidden()
test_self_report_is_rejected()
test_invalid_category_is_rejected()
test_details_must_be_between_10_and_500_characters()
test_unknown_request_is_not_found()
```

## 4. PyCharm 읽기 순서

1. `run.py`에서 application 시작점을 확인한다.
2. `bookloop/__init__.py`에서 factory와 blueprint 등록을 확인한다.
3. `clients/jinja_product.py`에서 화면 route가 어떤 service를 호출하는지 찾는다.
4. 해당 service 파일의 상단 Outline을 먼저 읽는다.
5. `db/models.py`에서 service가 저장하는 관계와 foreign key를 확인한다.
6. 대응하는 `tests/test_*.py`에서 성공·실패·권한 경계를 읽는다.
7. 마지막으로 template에서 사용자에게 보이는 feedback과 navigation을 확인한다.

## 5. 현재 리뷰 포인트

- R2: `reports.py` service와 focused tests 완료.
- R3: Jinja form → thin route → service 연결 필요.
- R4: 생성된 Report와 Admin queue의 동일 Report ID 브라우저 확인 필요.
- Admin queue에는 report details를 노출하지 않고, Report detail에서 검토 상태와
  외부 연락용 연락처를 제공하며, 별도 Member contact directory에서는
  관리자에게만 사용자 연락처를 제공하는 현재 privacy 경계를
  유지한다.

## 6. 검증 명령

```bash
cd app/backend
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider tests/test_reports_service.py
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider
```

현재 R3 검증 기록: Reporting/Jinja focused `32 passed`, 전체 backend `138 passed`.
