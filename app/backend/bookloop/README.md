# BookLoop Flask Package — D3 구조 진입 지도

이 문서는 `bookloop/` package를 오랜 시간이 지난 뒤 다시 열어도 실행 진입점과
모듈 책임을 빠르게 복원할 수 있도록 만든 얇은 Markdown 지도다. 상세 diagram과
학습 설명은 최신 브라우저용 Code Map에서 관리한다.

## Current documentation

| 문서 | 역할 |
| --- | --- |
| [`README.html`](README.html) | 최신 `BookLoop D3 · Code Map v1.4` |
| [`README-v1.3-d3.html`](README-v1.3-d3.html) | D3 v1.3 frozen archive |
| [`README-v1.2-d2.html`](README-v1.2-d2.html) | D2 v1.2 frozen archive |
| [`README-v1.1-d2.html`](README-v1.1-d2.html) | D2 v1.1 frozen archive |
| [`README-v1.0-d2.html`](README-v1.0-d2.html) | D2 v1.0 frozen archive |
| [`CODE_OUTLINE_MANUAL.md`](CODE_OUTLINE_MANUAL.md) | PyCharm 학습용 파일 연결·함수 아웃라인 매뉴얼 |
| [`../BOOKLOOP_DOCUMENTATION_INDEX.md`](../BOOKLOOP_DOCUMENTATION_INDEX.md) | 사용자·운영자·개발자 문서 인덱스 |
| [`../API_CONTRACT.md`](../API_CONTRACT.md) | JSON API와 privacy boundary 계약 |

`README.html`은 계속 갱신하는 canonical latest Code Map이고, version suffix가 있는
HTML은 해당 시점의 구조를 보존하는 archive다. archive는 최신 코드에 맞춰 다시
쓰지 않는다.

현재 자동화 검증 기준은 **142 backend tests passed**다.

## 1. Code purpose

BookLoop backend는 하나의 Flask application 안에서 다음 책임을 연결한다.

```text
Python/Jinja product UI
Flask JSON API
authentication and authorization
shared application services
SQLAlchemy relational models
SQLite persistence
local-only developer tools and BL-CLI
```

## 2. Entry points

### HTTP server

```text
backend/run.py
→ bookloop.create_app()
→ db.create_all() for local development
→ Flask development server
```

실행:

```bash
python3 run.py
```

### Terminal commands

```text
backend/bl_cli.py
→ devtools/bl_cli/commands.py
→ bookloop.create_app()
→ shared database boundary
```

실행:

```bash
python3 bl_cli.py --help
python3 bl_cli.py seed-demo
python3 bl_cli.py reset-demo-requests
python3 bl_cli.py upgrade-created-at
```

웹과 CLI는 서로 다른 entry point지만 같은 application factory, models와 SQLite를
사용한다. CLI는 HTTP Blueprint를 호출하지 않는다.

## 3. Package map

```text
bookloop/
├── __init__.py              # create_app() application factory
├── auth.py                  # login/register/logout + Flask-Login
├── api.py                   # /api/* JSON HTTP adapter
├── admin/
│   └── routes.py            # protected read-only Admin UI
├── clients/
│   ├── jinja_product.py     # main Python/Jinja product routes
│   └── flask_vanilla.py     # /vanilla/ static client provider
├── db/
│   ├── database.py          # unbound SQLAlchemy extension
│   └── models.py            # User, BookListing, BorrowRequest, Report
├── services/
│   ├── borrow_requests.py   # request lifecycle rules
│   ├── reports.py            # Report authorization, validation and persistence
│   ├── user_profiles.py     # privacy-safe profile context
│   ├── admin_dashboard.py   # admin authorization and overview
│   ├── health.py            # health response data
│   └── time_display.py      # Toronto display formatting
├── devtools/
│   ├── test_hub/            # /test/ navigation and learning hub
│   ├── db_inspector/        # debug-only read-only DB viewer
│   ├── user_switcher/       # debug-only seed user perspective switch
│   └── bl_cli/              # terminal command implementation
├── templates/               # Jinja templates grouped by owner
├── static/                  # Flask-served UI assets
└── flask_vanilla/           # HTML/CSS/JS served by flask_vanilla.py
```

`templates/`, `static/`와 `flask_vanilla/`는 Python package가 아니라 runtime asset
folder다. Python package는 `__init__.py`가 있는 module boundary다.

## 4. Application assembly

[`__init__.py`](__init__.py)의 `create_app()`이 다음 순서로 앱을 조립한다.

```text
configuration and environment
→ db.init_app(app)
→ login_manager.init_app(app)
→ model metadata registration
→ API CORS boundary
→ product and developer Blueprints
→ seed/reset Flask CLI commands
→ instance directory
```

등록되는 주요 Blueprint:

| Blueprint | URL boundary | 역할 |
| --- | --- | --- |
| `jinja_client` | `/`, `/requests/*`, `/users/*`, `/jinja/` | 제품 UI와 Jinja reference |
| `auth` | `/login`, `/register`, `/logout` | browser session |
| `admin` | `/admin/` | admin-only overview와 Report queue |
| `api` | `/api/*` | JSON adapter |
| `vanilla_client` | `/vanilla/` | Flask-hosted Vanilla assets |
| `test_hub` | `/test/` | 개발 링크 hub |
| `db_inspector` | `/dev/db/` | opt-in read-only DB inspection |
| `user_switcher` | `/dev/user-view/*` | opt-in seed user switch |

## 5. Main dependency flow

현재 핵심 BorrowRequest 흐름은 다음 경계를 지킨다.

```text
🐍 Jinja route ───────────────┐
                              ├→ services/borrow_requests.py
📤 JSON API route ────────────┘  → db/models.py
                                 → SQLite
```

- route: HTTP input parsing, login identity, redirect, JSON/Jinja response
- service: validation, authorization, lifecycle rule와 transaction
- model: relationship, constraint와 persisted state
- template/API serializer: 허용된 정보만 사용자에게 표시

제품 UI와 API는 응답 형식이 다르지만 같은 BorrowRequest service 규칙을 재사용한다.

## 6. Current D3 product flow

```text
Books
→ owner adds a book
→ owner reviews My books
→ owner edits title or author
→ owner changes availability
→ owner deletes a listing without request history
→ Tony sends request
→ Pending
→ Mina reviews Received request
→ Approve or Reject
→ approved contact visibility
→ borrower marks return
→ owner confirms receipt
→ Returned
→ listing Available
```

Admin UI는 system overview, book-sharing state와 read-only Report queue를 보여준다.
로그인 사용자는 `My books`에서 자신의 책을 등록·수정하고 availability를 전환할 수
있다. 사용자 책 관리와 Report workflow는 현재 Beta의 검증된 Jinja 흐름이다.

## 7. Intentional boundaries and known gaps

- `devtools/`는 제품 업무 규칙을 우회하지 않는 local-only 도구다.
- DB Inspector는 read-only이며 reset은 BL-CLI가 담당한다.
- `clients/jinja_product.py`와 `api.py`는 D3 동결 뒤 기능별 분할을 검토한다.
- `services/time_display.py`는 현재 service package에 있지만 이후 presentation utility
  경계로 이동할 수 있다.
- Listing API write route는 아직 request JSON의 `owner_id`를 사용한다. session-based
  authorization을 적용하기 전에는 React write consumer와 연결하지 않는다.
- 사용자 책 관리 Jinja route는 request body의 owner ID를 신뢰하지 않고
  `current_user.id`와 listing owner를 service에서 비교한다.
- React는 D3 필수 기능이 아니다. 시작할 경우 기존 API의 read-only consumer
  slice로 제한한다.

## 8. Current user book management boundary

```text
My books / Add a book / Edit
→ login_required Jinja route
→ services/book_listings.py
→ current_user ownership check
→ BookListing transaction
→ My books template
```

현재 화면 경로:

- `/my-books/` — 본인 책 목록
- `/my-books/new` — 책 등록
- `/my-books/<listing_id>/edit` — 제목·저자 수정
- `/my-books/<listing_id>/availability` — availability 전환
- `/my-books/<listing_id>/delete` — request history가 없는 본인 책 삭제

availability가 `Unavailable`인 책은 새로운 borrow request를 받을 수 없다. 기존
borrow request history는 삭제하지 않으며, 다른 회원의 listing은 수정하거나
availability를 바꿀 수 없다.
borrow request history가 있는 책은 기록 보존을 위해 삭제할 수 없다.

## 9. Next implementation boundary

Reporting logic을 기존 route나 Admin Dashboard에 섞지 않는다.

```text
Jinja Report form
→ thin Jinja route
→ services/reports.py
→ Report model
→ SQLite
→ Admin read-only queue
```

`services/reports.py`가 소유할 규칙:

- 관련 BorrowRequest 당사자만 신고 가능
- 자기 자신 신고 차단
- category와 details server-side validation
- Report transaction과 예상 가능한 service error

## 10. Review order

오래 뒤 다시 볼 때는 다음 순서로 읽는다.

```text
1. backend/run.py
2. bookloop/__init__.py
3. bookloop/clients/jinja_product.py
4. bookloop/services/borrow_requests.py
5. bookloop/db/models.py
6. bookloop/api.py
7. bookloop/auth.py
8. bookloop/admin/routes.py
9. bookloop/devtools/
10. backend/tests/
```

구조 diagram이나 client별 상세 연결이 필요하면 [`README.html`](README.html)을 연다.
