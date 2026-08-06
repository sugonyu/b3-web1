# BookLoop Flask Package — 개인 구조 참고

[최신 브라우저용 전체 코드 맵](README.html)
[v1.0 기준선 코드 맵](README-v1.0.html)

이 문서는 `bookloop/` 패키지를 다시 볼 때 실행 진입점과 세 client Blueprint의
차이를 빠르게 기억하기 위한 개인 코드 지도다.

## 1. 코드의 목적

BookLoop 백엔드는 하나의 Flask 애플리케이션 안에서 다음 책임을 분리한다.

```text
제품용 Python/Jinja 화면
개발용 client 비교 화면
독립 Vanilla 파일 제공
JSON API
SQLAlchemy + SQLite
개발 전용 DB 확인·시드 도구
```

Flask 정적 자산도 사용 주체가 바로 보이도록 소유권별로 구분한다.

```text
static/
├── bookloop/      # 현재 제품·인증·참고 화면의 공통 UI 자산
├── db_inspector/  # Inspector 전용 디자인이 생길 때 사용
└── shared/        # 둘 이상의 UI가 실제로 공유하는 범용 자산
```

현재 `db_inspector/`와 `shared/`는 향후 역할을 기록하는 README만 가진 예약 폴더다.
필요가 생기기 전에는 자산을 억지로 분리하거나 공용화하지 않는다.

`clients/client_jinja.py`, `clients/client_test.py`, `clients/client_vanilla.py`는 각각 서버를 새로 실행하는
파일이 아니다. 세 파일 모두 URL과 처리 함수를 묶은 **Flask Blueprint 정의 파일**이며,
실제 Flask 앱은 `create_app()`이 이 Blueprint들을 모아 완성한다.

## 2. 실제 진입점

### 실행 진입점 — `backend/run.py`

```text
python3 run.py
```

`run.py`의 역할:

1. `from bookloop import create_app`으로 application factory를 가져온다.
2. `app = create_app()`으로 Flask 앱을 만든다.
3. `db.create_all()`로 없는 SQLite 테이블을 준비한다.
4. `app.run(debug=True)`로 개발 서버를 실행한다.

따라서 서버 실행을 이해할 때는 `client_*.py`가 아니라 먼저 `run.py`를 본다.

### 조립 진입점 — `bookloop/__init__.py`

`create_app()`은 BookLoop의 연결 허브다.

```text
run.py
└── create_app()                    bookloop/__init__.py
    ├── 환경변수와 Flask 설정
    ├── db.init_app(app)
    ├── login_manager.init_app(app)
    ├── CORS 설정
    ├── api Blueprint 등록
    ├── 세 client Blueprint 등록
    ├── db_inspector Blueprint 등록
    └── seed-demo · reset-demo-requests CLI 명령 등록
```

서버와 관리 명령의 Python 진입점은 분리한다. 현재 코드 맵 v1.1(`README.html`)에서는
`backend/bl_cli.py → devtools/bl_cli/` 아래의 `commands.py`와 `seed/`가 같은 레벨에서
협력하는 별도 관리 도구 흐름으로 기록한다.

```text
source .venv/bin/activate           → BookLoop Python 환경 활성화
python3 run.py                    → Flask web server
python3 bl_cli.py --help          → BookLoop CLI command 목록
python3 bl_cli.py seed-demo       → demo 시작 데이터
python3 bl_cli.py reset-demo-requests → demo BorrowRequest 초기화
```

즉, 기존의 `python run.py`와 같은 방식으로 서버는 `python3 run.py`, 관리 작업은
`python3 bl_cli.py <command>`로 실행한다. 둘 다 동일한 가상환경의 Flask,
SQLAlchemy와 BookLoop application factory를 사용한다.

## 3. 세 client 파일의 차이

| 파일 | URL | 역할 | 화면의 실제 위치 |
| --- | --- | --- | --- |
| `clients/client_jinja.py` | `/`, `/jinja/` | Flask가 Jinja template을 렌더링 | `templates/bookloop/`, `templates/jinja_reference/` |
| `clients/client_test.py` | `/test`, `/test/` | client·API·도구 차이를 설명하는 개발 hub | `templates/test_hub/` |
| `clients/client_vanilla.py` | `/vanilla/` | 🐍🟨 Flask Vanilla 파일을 정적으로 제공 | `bookloop/flask_vanilla/` |

### `clients/client_jinja.py` — Python/Jinja 화면

두 화면의 책임을 구분한다.

```text
GET /
→ product_home()
→ templates/bookloop/index.html
→ D2 BorrowRequest 제품 UI로 확장할 홈

GET /jinja/
→ jinja_reference()
→ services/health.py의 Python data
→ templates/jinja_reference/index.html
→ Python/Jinja 구조를 설명하는 학습 참고 화면
```

핵심은 `/`가 제품 화면이고 `/jinja/`는 기술 참고 화면이라는 점이다.

### `clients/client_test.py` — 개발용 목차

```text
GET /test/
→ templates/test_hub/index.html
→ Jinja client
→ Vanilla via Flask
→ 독립 Vanilla client
→ JSON health API
→ DB Inspector
```

자동 테스트를 실행하는 파일이 아니다. 사람이 브라우저에서 각 실행 경로의 차이를
비교하는 **개발·학습용 링크 허브**다.

### `clients/client_vanilla.py` — 정적 파일 전달자

이 파일은 Python으로 Vanilla 화면을 만들지 않는다.

```text
clients/client_vanilla.py
→ bookloop/flask_vanilla/ 폴더를 찾음
→ index.html, CSS, JavaScript를 /vanilla/에서 제공
→ JavaScript는 브라우저에서 실행
→ 필요한 data는 Flask JSON API에 fetch
```

두 Vanilla client는 역할과 source가 분리되어 있다.

```text
http://127.0.0.1:5000/vanilla/
→ Flask가 bookloop/flask_vanilla/ 제공

http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/
→ WordPress Docker static server가 독립 source 제공
```

port `8080`에서 port `5000`의 API를 호출하면 origin이 다르므로 CORS가 필요하다.

## 4. 전체 연결 구조

```text
backend/run.py
└── bookloop.create_app()
    ├── clients/
    │   ├── client_jinja.py
    │   │   ├── /        → templates/bookloop/index.html
    │   │   └── /jinja/  → services/health.py → templates/jinja_reference/index.html
    │   ├── client_test.py
    │   │   └── /test/   → templates/test_hub/index.html
    │   └── client_vanilla.py
    │       └── /vanilla/ → bookloop/flask_vanilla/
    │
    ├── api.py
    │   └── /api/*   → HTTP parsing · JSON response
    │
    ├── services/borrow_requests.py
    │   └── create/read · validation · authorization · transaction
    │
    ├── auth.py
    │   └── Flask-Login session + current_user
    │
    ├── db/
    │   ├── database.py
    │   └── models.py
    │       └── User · BookListing · BorrowRequest → SQLite
    │
    └── devtools/
        ├── db_inspector/ → /dev/db/ read-only 확인
        └── bl_cli/       → seed-demo · reset-demo-requests
```

Vanilla client는 두 실행 경계를 구분한다. 독립 JavaScript client는
`app/frontend/js-vanilla/`에서 Port 8080으로 실행하고, Flask의 `/vanilla/`는
검수 편의를 위해 `bookloop/flask_vanilla/` 복사본을 제공한다.

## 5. 경로 관계

Tony가 사용하는 Web1 개인 실험실 기준 경로:

```text
~/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/
└── app/
    ├── backend/
    │   ├── run.py                 # 서버 실행 진입점
    │   └── bookloop/              # 현재 Flask package
    └── frontend/
        ├── js-vanilla/            # 독립 JavaScript source
        └── react/                 # 미래 React client
```

WSL에서 실제 물리 경로가 `/home/sugonyu/js_dev/block2/test/test_py/...`로 표시될 수
있지만, 이 문서에서는 Tony가 지정한 `~/jd/b2/...` Web1 경로를 기준으로 설명한다.

## 6. 다시 리뷰할 순서

```text
1. run.py                 서버가 어디서 시작되는가?
2. bookloop/__init__.py   어떤 모듈을 앱에 연결하는가?
3. clients/client_jinja.py   제품 화면과 Jinja 참고 화면은 어떻게 다른가?
4. clients/client_test.py    개발 링크 허브가 무엇을 비교하는가?
5. clients/client_vanilla.py 정적 source가 어디에 있고 누가 제공하는가?
6. api.py                 client가 사용하는 JSON 경계는 무엇인가?
7. auth.py                current_user는 어떻게 만들어지는가?
8. db/models.py           데이터 관계는 어떻게 저장되는가?
```

실제 제품 UI는 `templates/bookloop/`, Jinja 기술 참고 화면은
`templates/jinja_reference/`, 개발 링크 허브는 `templates/test_hub/`에 둔다.
기술명보다 BookLoop 도메인을 먼저 드러내면서 보조 화면의 목적도 구별하는 구조다.

현재 다음 구현 지점은 `templates/bookloop/index.html`을 공통 BorrowRequest service에
연결하는 것이다.

## 7. W2-07 공통 BorrowRequest service

API와 다음 Python/Jinja 제품 화면은 서로 다른 응답 형식을 사용하지만 같은 업무
규칙을 사용한다.

```text
api.py ─────────────────────┐
                            ├→ services/borrow_requests.py
clients/client_jinja.py (W2-08) ┘   ├── create_borrow_request()
                                ├── get_authorized_borrow_request()
                                ├── validation + authorization
                                └── SQLAlchemy commit/read
```

- route: HTTP 입력 parsing, 오류를 status code로 변환, JSON/Jinja 응답 선택
- service: create/read와 business validation·authorization·transaction
- model: 관계 정의와 SQLite 영속성

W2-07 검증에서는 service와 기존 API 집중 테스트 16개, 전체 backend 테스트 52개가
통과했다. 다음 W2-08은 같은 service를 제품 Jinja 화면에서 호출한다.
