# BookLoop Private App

이 폴더는 Web1 공개 배달 전에 개발·검증하는 비공개 최신 코드 본진이다.

현재 단계:

```text
Private Stage A-2 — User, BookListing and BorrowRequest models
```

## App 시작 전 확인

앱 작업은 이 README만 읽고 바로 시작하지 않는다. 먼저 Web1 개인 brain과 상위
개인 본진 README를 확인해 오늘의 범위와 실험 경계를 맞춘다.

```text
1. /home/sugonyu/jd/b2/test/test_py/b3-web1/note/README.md
2. /home/sugonyu/jd/b2/test/test_py/b3-web1/note/TODO.md
3. /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/README.md
4. 이 app/README.md와 현재 코드
```

진행 순서는 다음과 같다.

```text
note brain의 오늘·이번 주 TODO
→ 상위 README의 개인 문서·실험 규칙
→ app의 현재 구현과 테스트
→ 작은 실험·검증
→ 검증된 결과만 공개 Deliverable로 승격
```

따라서 `app/`에서 새 기능을 시작하기 전에 quote, milestone 범위, 현재 blocker와
검증 기준을 먼저 확인한다.

## Structure

```text
app/
├── architecture/      # 반복 업데이트하는 model·API·기술 구조 evidence
├── backend/          # Flask JSON API, SQLAlchemy와 SQLite
├── backend-express/  # 🟨 health API + EJS 참고 화면 병렬공부 backend
├── design-system/    # HTML/CSS 디자인 증거와 low-fi 화면 초안
└── frontend/
    ├── js-vanilla/   # 🟨 독립 HTML/CSS/JavaScript API client
    └── react/        # ⚛️ 미래 React client의 문서 scaffold
```

`architecture/`는 model, API, authentication과 client/server boundary를 매주
실제 구현과 비교하며 갱신하는 기술 설계 evidence다. D1 한국어 기준선은
`drafts/v1.0-d1-foundation-ko/`, 영어 번역본은
`drafts/v1.1-d1-foundation-en/`이며 브라우저 인덱스는
[`architecture/index.html`](architecture/index.html)이다.

`design-system/`은 실제 제품 frontend가 아니라 🧩 Deliverable 1을 위한 정적
design evidence 실험실이다. `drafts/v1.0-d1-foundation/`은 최초 Web1 기준선,
`drafts/v1.1-d1-uiux-bridge/`는 B3 UIUX의 60/30/10, Gestalt와 user-flow 원리를
연결한 선택본이다. 병렬공부와 Deliverable 1 발표 준비에는 v1.1을 사용하고 v1.0은
비교 기준선으로 보존한다. Draft v1.1은 Tony 확인 후 D1 Design System MVP v0.1
기준선으로 채택됐으며 D2 이후에도 반복 개선한다.

두 versioned artifact의 공통 폴더·파일 이름은
[`ARTIFACT_NAMING_CONVENTION.md`](ARTIFACT_NAMING_CONVENTION.md)를 따른다.

현재 Vanilla frontend는 Flask API 연결을 가볍게 검증하는 Private Stage B0다.
`frontend/react/`는 미래 연결 위치와 API 계약만 기록하며, React/Vite package와
제품 구현은 Flask API 계약과 핵심 CRUD를 검증한 뒤 시작한다.

## 폴더를 필요 이상으로 늘리지 않는 원칙

`app/`의 상위 폴더는 기능 하나가 생길 때마다 추가하지 않는다. 새로운 관점의
증거나 독립 실행 영역이 실제로 필요할 때만 만든다. 기존 관점이 발전하는 경우에는
새 상위 폴더 대신 해당 폴더 안의 코드 또는 versioned draft를 업데이트한다.

```text
새로운 관점의 증거 또는 독립 실행 영역 → 새 상위 폴더 검토
기존 관점의 기능·설계 발전             → 기존 폴더 안에서 업데이트
아직 시작하지 않은 미래 기능            → 폴더를 미리 만들지 않음
```

현재 필요한 상위 구조는 다음으로 충분하다.

```text
app/
├── architecture/      # model·API·인증·데이터 흐름 설계 evidence
├── backend/           # Flask·SQLAlchemy·SQLite·CRUD 실제 구현
├── backend-express/   # 🟨 GET /api/health + /ejs/ 독립 Express spike
├── design-system/     # UI 규칙, component와 화면 상태 evidence
└── frontend/
    ├── js-vanilla/    # 🟨 Independent JS Vanilla :8080
    └── react/         # ⚛️ README-only future boundary
```

Tony의 명시적 결정으로 `frontend/react/` 위치는 README-only scaffold로 먼저
예약했다. 실제 React/Vite 파일은 구현을 시작하는 시점에만 추가한다.
로그인, CRUD, trust rating 같은 기능명으로 `app/auth/`, `app/crud/`,
`app/rating/` 등의 상위 폴더를 따로 만들지 않는다.

| 새 내용 | 기존 또는 미래의 위치 |
| --- | --- |
| 로그인·인증 설계 | `architecture/drafts/v2.x-d2-.../` |
| 로그인 실제 코드 | `backend/bookloop/` |
| database migration | Flask-Migrate를 실제 도입할 때 `backend/migrations/` |
| API 자동 테스트 | `backend/tests/` |
| Express 병렬공부 | `backend-express/` — health API와 EJS 참고 화면 이후 제품 확장 금지 |
| React 화면 | React 작업을 시작할 때 `frontend/react/` |
| Docker·배포 설정 | 적용 대상에 따라 `app/` 또는 해당 실행 폴더 바로 아래 |
| 공개 발표·주간 배달 | 공개 저장소의 `milestones/` |
| 실험 단계 증거 | 기존 `snapshots/stages/` |

Deliverable이 진행되어도 `design-system/`과 `architecture/`는 새 상위 폴더로
복제하지 않고 각자의 `drafts/`에서 반복 개선한다.

```text
D1 → design-system + architecture 기준선
D2 → backend 구현 + architecture D2 draft
D3 → frontend/react 시작 + design-system/architecture D3 draft
D4 → tests·error handling 강화 + architecture D4 draft
```

폴더 생성 전에는 다음 한 문장으로 판단한다.

> 새로운 독립 영역인가, 아니면 기존 영역의 다음 버전인가?

후자라면 새 상위 폴더를 만들지 않는다.

Optional Jinja 비교 UI는 독립 frontend 폴더가 아니라 Flask package 안에 둔다.

```text
backend/bookloop/
├── clients/
│   ├── client_jinja.py
│   ├── client_test.py
│   └── client_vanilla.py
├── flask_vanilla/
├── templates/
│   ├── bookloop/         # 실제 BookLoop 제품 UI
│   ├── jinja_reference/  # Jinja 기술 참고 화면
│   └── test_hub/         # 개발 링크 허브
├── static/
│   ├── bookloop/       # 현재 BookLoop Flask UI 자산
│   ├── db_inspector/   # Inspector 전용 자산 예약
│   └── shared/         # 실제 범용 공통 자산 예약
└── services/health.py
```

JSON API와 Jinja UI는 같은 `get_health_status()` service를 사용한다.

개발 중 SQLite row와 model 관계를 확인하는 도구는 제품용 Admin UI와 분리한다.
BorrowRequest 제품 UI보다 먼저 허용하는 범위는 개발 전용 read-only inspector
v0.1뿐이며, 상세 범위와 중단선은
[`D2 Developer Database Inspector Roadmap`](../docs/planning/D2_DEV_DATABASE_INSPECTOR_ROADMAP.md)을
따른다.

```text
api.py ────────────> services/health.py ──> JSON
clients/client_jinja.py ───> services/health.py ──> Jinja HTML
clients/client_vanilla.py ─> flask_vanilla/ 정적 파일 제공
```

### Vanilla clients — two explicit execution boundaries

두 Vanilla client는 현재 학습과 실행 경계를 명확히 구분하기 위해 별도 source로
보관한다.

```text
🟨 Independent Vanilla :8080
└── app/frontend/js-vanilla/

🐍🟨 Flask Vanilla :5000
└── backend/bookloop/flask_vanilla/
    └── clients/client_vanilla.py → /vanilla/
```

- port `8080`: 독립 static client이며 Flask API 호출에 CORS가 필요하다.
- port `5000`: `clients/client_vanilla.py`가 Flask 전용 복사본을 제공한다.
- 두 화면 모두 `http://127.0.0.1:5000/api/health`를 호출한다.

상세 구조와 실행 주소는
[`frontend/js-vanilla/README.md`](frontend/js-vanilla/README.md)에서 확인한다.

React의 API 연결 계획과 구현 시작 조건은
[`frontend/react/README.md`](frontend/react/README.md)에서 확인한다.

### Express health-only parallel spike

`backend-express/`는 Flask 제품 backend를 교체하지 않는다. Flask의 Blueprint,
application factory, service와 JSON response 구조를 Express Router, `createApp()`,
service와 `response.json()`으로 다시 구현하는 병렬공부용 독립 실행 영역이다.

```text
🟨 Express :3001
→ GET /api/health
→ Router
→ services/health.js
→ JSON + local client CORS
```

실행과 자동 테스트는
[`backend-express/README.md`](backend-express/README.md)를 따른다. Listing, database,
authentication과 CRUD는 D3 이후 parity roadmap 전까지 추가하지 않는다.

## Stage A-2 Model Contract

```text
User
├── id
├── username
├── email
├── password_hash
└── general_area

BookListing
├── id
├── title
├── author
├── availability
└── owner_id → User.id

BorrowRequest
├── id
├── status
├── listing_id → BookListing.id
└── borrower_id → User.id
```

관계:

```text
User 1 ── N BookListing
User 1 ── N BorrowRequest
BookListing 1 ── N BorrowRequest
```

`BorrowRequest.status`의 첫 허용 흐름은
`pending → approved/rejected`, `approved → returned`다. Rating과 trust history는
이번 model에 넣지 않고 optional backlog로 유지한다.

## Stage A-3 API Contract

React client와 Flask backend 사이의 7개 핵심 제품 endpoint 경계는
[`backend/API_CONTRACT.md`](backend/API_CONTRACT.md)에 정리한다.

첫 구현 범위는 다음 두 endpoint다.

```text
GET  /api/listings
POST /api/listings
```

나머지 BookListing CRUD와 BorrowRequest workflow는 같은 계약의 순서에 따라
작은 단계로 추가한다.

현재 7개 핵심 endpoint와 대응 테스트 코드 작성을 마쳤고, Tony 확인 후 전체
묶음을 일괄 실행해 통과했다.

```text
작성된 자동 테스트: 기존 8개 + 신규 API 16개 = 총 24개
검증 결과: 24 passed (2026-07-28)
```

## Deliverable 2 Sunday Preflight — 2026-08-02

Week 2 시작 전 현재 backend 기준선을 다시 실행했다.

```text
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider
→ 25 passed
```

`/tmp`의 임시 SQLite 파일로 `db.create_all()` 후 User를 commit하고, 새 app
instance가 같은 DB를 다시 열어 저장된 User를 조회하는 persistence 검증도 통과했다.
실제 프로젝트 DB와 사용자 데이터는 사용하지 않았다.

현재 확인된 범위:

- core model과 relationship
- BookListing CRUD
- BorrowRequest 생성과 상태 전환
- validation과 owner permission 검사
- SQLite 파일 생성과 재접속 persistence

아직 확인하거나 구현할 범위:

- Flask 개발 서버와 browser/API startup 확인
- BorrowRequest create와 연결할 read endpoint 선택
- 실제 로그인 기반 authentication과 authorization

현재 API의 `owner_id`·`borrower_id` 입력값 검사는 실제 로그인 인증으로 간주하지
않는다.

## Previous Stage Snapshot

Private Stage A-2를 시작하기 전 기준선은 Git에서 복원해 다음 위치에 동결했다.

```text
../snapshots/stages/private-stage-a1-v0.1.0/
```

이 snapshot은 `v0.1.0` health API와 Vanilla/Jinja client를 포함하며 automated test
6개가 통과한다. 이후 개발은 snapshot이 아니라 현재 `app/`에서만 계속한다.

## AWP 학습 참조

Web1 backend는 `/home/sugonyu/jd/b2/test/test_py/b3-awp`에서 배운 Flask 개념을
재사용한다. 관련 파일을 설명할 때 다음 실제 수업 경로를 함께 확인한다.

| Web1 파일·개념 | AWP 참조 |
| --- | --- |
| `run.py`, Flask 실행 | `b3-awp/classes/class18-jun-17-wed-flask-intro/01_basic_routes.py` |
| `api.py`, Blueprint | `b3-awp/classes/class19-jul-07-tue-flask-blueprints/` |
| `api.py`, JSON 응답 | `b3-awp/classes/class22-jul-15-wed-database-models-validation/ex/station_bike-1n-bi-nav-1.2-json-route.py` |
| `database.py`, `db = SQLAlchemy()` | `b3-awp/classes/lia/models.py` |
| `__init__.py`, app 설정과 `db.init_app()` | `b3-awp/classes/lia/app.py` |

BookLoop의 application factory와 React용 API 분리는 AWP의 학습 내용을 Web1
구조로 확장한 것이다. 참조 코드를 그대로 복사하기보다 같은 개념이 새 구조에서
어떤 역할을 맡는지 비교한다.

## 파일 이름 결정 — `database.py`

Flask에서 `extension`은 파일 확장자가 아니라 Flask에 기능을 추가하는 library를
뜻한다. 예를 들면 Flask-SQLAlchemy, Flask-Login, Flask-CORS와 Flask-Migrate가
있다.

여러 extension 객체를 한 파일에 모으면 `extensions.py`가 자연스럽다.

```python
db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()
migrate = Migrate()
```

현재 BookLoop는 SQLAlchemy database 객체 하나만 관리한다. 초보 학습 단계에서
파일 역할이 바로 보이도록 `extensions.py` 대신 `database.py`를 사용한다.

```text
현재: DB 객체 하나 → database.py
미래: 여러 Flask extension을 한곳에 모음 → extensions.py 재검토 가능
```

현재 파일 역할:

```text
__init__.py  = Flask 앱 조립
api.py       = JSON API route
database.py  = SQLAlchemy database 객체
```

## 실행 방법

### 1. Backend 폴더로 이동

어느 위치에서 시작해도 아래 명령으로 이동할 수 있다.

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
```

### 2. 최초 1회 환경 준비

`.venv`가 이미 있으면 이 단계는 반복하지 않는다.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

실제 secret을 사용할 때만 `.env.example`을 참고해 Git에서 제외되는 `.env`를
만든다. 현재 health endpoint는 `.env` 없이도 개발 기본값으로 실행된다.

### 3. 평소 Flask 서버 실행

```bash
.venv/bin/python run.py
```

터미널에 다음 주소가 나타나면 서버가 실행된 것이다.

```text
http://127.0.0.1:5000
```

이 주소는 Jinja가 아닌 정적 Vanilla HTML/CSS/JavaScript 화면을 보여준다. 화면이
열리면 `Check API` 버튼과 API 상태를 확인한다.

### 4. Vanilla frontend 확인 경로

Flask backend를 먼저 실행한 상태에서 다음 세 경로를 사용할 수 있다.

| 방식 | Frontend 주소 | 용도 |
| --- | --- | --- |
| D2 product home | `http://127.0.0.1:5000/` | 독립 `Hello BookLoop` 기준점; 이후 제품 UI 확장 |
| 🐍 Python/Jinja reference | `http://127.0.0.1:5000/jinja/` | Flask server-rendered 기술·학습 화면 |
| 🧪 Test Hub | `http://127.0.0.1:5000/test` | Clients·API·Developer Tools 분류와 실행 경계 비교 |
| VS Code Live Preview | `http://127.0.0.1:3000/wp-docker-lab/wordpress/pub/b3-web1/app/frontend/js-vanilla/index.html?vscode-livepreview=true` | HTML/CSS/JS 편집 확인 |
| 🟨 JavaScript/Vanilla | `http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/` | WordPress Docker static client |

세 화면 모두 같은 Flask API를 사용한다.

```text
http://127.0.0.1:5000/api/health
```

현재 Private Stage B0 테스트에서는 `app.js`에 이 주소를 명시적으로 고정한다.

```javascript
const healthApiUrl = "http://127.0.0.1:5000/api/health";
```

Live Preview와 WordPress Docker는 frontend와 API의 port가 다르므로 browser의
same-origin 정책상 CORS 허용이 필요하다.

```text
Frontend 3000 또는 8080
→ fetch http://127.0.0.1:5000/api/health
→ Flask-Cors가 허용된 local origin인지 검사
→ JSON 반환
→ app.js가 상태·확인 횟수·시간 표시
```

개발용 허용 origin:

```text
http://127.0.0.1:3000
http://localhost:3000
http://127.0.0.1:8080
http://localhost:8080
```

### CORS란?

`CORS`는 **Cross-Origin Resource Sharing**의 약자이며 보통 한국 개발 현장에서는
`코어스`라고 읽는다.

브라우저의 origin은 다음 세 값의 조합이다.

```text
protocol + host + port
```

하나라도 다르면 다른 origin이다. 같은 물리 폴더에 있는지는 브라우저의 판단 기준이
아니다.

```text
http://localhost:8080
http://127.0.0.1:5000
```

위 두 주소는 host와 port가 다르므로 cross-origin이다.

#### Jinja가 별도 CORS 없이 작동하는 경우

Flask가 Jinja HTML과 API를 모두 port `5000`에서 제공하면 브라우저 기준으로 같은
origin이다.

```text
Jinja HTML: http://127.0.0.1:5000/
Flask API:  http://127.0.0.1:5000/api/health
```

```text
같은 protocol + host + port
→ same-origin
→ CORS 허용 불필요
```

Jinja와 Flask가 같은 폴더에 있어서가 아니라 브라우저 URL의 origin이 같아서
작동한다.

#### 독립 Vanilla 또는 React client

독립 frontend는 보통 Flask와 다른 port에서 실행된다.

```text
Vanilla static: http://localhost:8080
React/Vite:     http://localhost:5173
Flask API:      http://127.0.0.1:5000
```

이때 `fetch()` 요청이 Flask에 도착하고 Flask가 HTTP 200을 반환하더라도, 허용
header가 없으면 브라우저가 JavaScript에 응답 내용을 넘기지 않는다.

```text
CORS 적용 전
JavaScript → Flask → JSON 응답 → browser가 차단 → JS가 읽지 못함
```

Flask가 다음 header를 반환하면 해당 frontend origin이 응답을 읽을 수 있다.

```http
Access-Control-Allow-Origin: http://localhost:8080
```

```text
CORS 적용 후
JavaScript → Flask → JSON + 허용 header → browser 허용 → 화면 표시
```

`Access-Control-Allow-Origin`은 모든 사이트를 허용한다는 뜻이 아니다. 현재 설정은
개발에 사용하는 local origin만 명시적으로 허용한다.

독립 React frontend에서도 같은 문제가 발생한다. 개발 단계에서는 제한된 CORS나
Vite proxy를 사용하고, 배포에서는 frontend와 API를 같은 origin으로 제공하는 방법도
사용할 수 있다.

`index.html`은 다음 상대경로로 CSS와 JavaScript를 불러온다. 따라서 Flask,
Live Preview와 WordPress Docker 경로에서 같은 파일을 사용할 수 있다.

```html
<link rel="stylesheet" href="./style.css">
<script type="module" src="./app.js"></script>
```

정상 화면 예:

```text
Endpoint: http://127.0.0.1:5000/api/health
Check #1: ok — flask-api 0.2.0 at 6:00:00 PM
```

두 기본 client 주소:

```text
🐍 Python / Jinja:       http://127.0.0.1:5000/
🟨 JavaScript / Vanilla: http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/
```

Jinja 화면은 browser `fetch()` 없이 Flask가 공유 service 데이터를 읽고 HTML을
render한다. Vanilla 화면은 고정된 Flask health API를 `fetch()`한다. Flask가
Vanilla 파일을 제공하는 보조 확인 경로는 `http://127.0.0.1:5000/vanilla/`이다.

### 5. Health API 직접 확인

브라우저에서 다음 주소를 연다.

```text
http://127.0.0.1:5000/api/health
```

또는 별도 터미널에서 확인한다.

```bash
curl http://127.0.0.1:5000/api/health
```

정상 응답:

```json
{
  "app": "BookLoop",
  "service": "flask-api",
  "status": "ok",
  "version": "0.2.0"
}
```

### 6. 자동 테스트 실행

서버를 따로 실행하지 않아도 된다.

```bash
.venv/bin/python -m unittest discover -s tests -v
```

성공 기준:

```text
Ran 8 tests
OK
```

### 7. 문제 해결

버튼이 반응하지 않으면 다음 순서로 확인한다.

1. Flask server가 port `5000`에서 실행 중인지 확인한다.
2. `http://127.0.0.1:5000/api/health`가 직접 열리는지 확인한다.
3. `Ctrl+Shift+R`로 JavaScript cache를 무시하고 다시 읽는다.
4. 브라우저 개발자 도구 Console에서 CORS 또는 `app.js` 404를 확인한다.

### 8. 서버 종료

서버를 실행한 터미널에서 다음 키를 누른다.

```text
Ctrl+C
```

## 빠른 재실행

최초 설치가 끝난 뒤에는 다음 두 명령만 사용한다.

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
.venv/bin/python run.py
```

## Current Success Condition

- Flask application factory가 앱을 생성한다.
- SQLAlchemy extension이 앱에 연결된다.
- `User`, `BookListing`, `BorrowRequest` table을 생성할 수 있다.
- owner, borrower와 listing 관계를 양방향으로 탐색할 수 있다.
- `/api/health`가 HTTP 200과 JSON을 반환한다.
- 전체 automated test 8개가 통과한다.
- `/`에서 독립 `Hello BookLoop` 제품 홈이 열리고 `/jinja/`는 기술 참고 화면으로 분리된다.
- `/vanilla/`에서 공유 Vanilla client가 열린다.
- `/api/health`에서 JSON API 응답을 확인할 수 있다.

검수 기록:

```text
2026-07-28 — Tony reviewed
8 automated tests passed
/          Jinja client
/jinja/    Jinja client
/vanilla/  shared Vanilla client
/api/health JSON API
```

다음 체크포인트는 5–8개 endpoint 계약과 최소 BookListing JSON CRUD다.
