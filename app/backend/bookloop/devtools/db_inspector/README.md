# Developer Database Inspector v0.4

BookLoop의 `User`, `BookListing`, `BorrowRequest`, `Report` row와 관계 ID를 브라우저에서
빠르게 확인하는 **개발 전용 read-only 화면**이다.

전체 계획과 제품 UI 우선순위는
[`D2 Developer Database Inspector Roadmap`](../../../../../docs/planning/D2_DEV_DATABASE_INSPECTOR_ROADMAP.md)을
따른다.

## 실행 조건

`/dev/db`는 두 가지 개발 경로로 열린다.

```text
Main 로컬 DEBUG
→ ENABLE_DEV_DB_INSPECTOR=true
→ loopback 요청

Main → Rose LAN 검수
→ Flask DEBUG=false
→ ENABLE_DEV_DB_INSPECTOR=true
→ ENABLE_LAN_DEV_DB_INSPECTOR=true
→ 내부 network 요청
→ 관리자 로그인
```

로컬 `.env` 예시:

```env
ENABLE_DEV_DB_INSPECTOR=true
ENABLE_LAN_DEV_DB_INSPECTOR=true
```

LAN에서 비로그인 사용자는 `/login?next=/dev/db/`로 이동하고, 일반 회원은 `403`,
외부 source IP 또는 비활성 환경은 `404`를 반환한다. `.env.example`의 두 설정은
기본 `false`이며 실제 `.env`는 Git에 기록하지 않는다. Flask debugger는 LAN에서
계속 끈 상태로 유지한다.

Rose 접속 주소:

```text
http://MAIN_LAN_IP:5000/dev/db/
```

ChromeOS Wi-Fi 화면의 현재 Main LAN IP를 사용하며 `100.115.92.x` Crostini 내부 IP를
브라우저 주소로 사용하지 않는다.

## v0.4가 보여주는 값

| Model | 표시 필드 |
| --- | --- |
| User | `id`, `created_at`, `username`, `general_area` |
| BookListing | `id`, `created_at`, `title`, `author`, `availability`, owner ID + username |
| BorrowRequest | `id`, `created_at`, `status`, `listing_id`, `borrower_id` |
| Report | `id`, `created_at`, `reporter`, `reported user`, `category`, `details`, `status` |

BorrowRequest의 `status`는 제품 화면과 같은 색상 배지로 표시한다. 테이블 위 레전드에서
`Pending`(amber), `Approved`(green), `Rejected`(red), `Cancelled`(gray),
`Returned`(blue)를 한 번에 확인할 수 있다. 색상만으로 상태를 전달하지 않도록 각 배지의
텍스트 label도 항상 유지한다.

각 table은 `created_at DESC`, 같은 시각이면 `id DESC`로 표시해 최신 row가 가장
위에 온다. 모든 생성 시간은 지역명과 초를 생략한 `Aug 12 · 12:51 PM` 형식으로
통일한다.
timestamp 도입 전의 기존 row는 정확한 과거 생성 시점을 추측하지 않고 `Legacy row`로
표시한다.

기존 SQLite DB에는 table 삭제 없이 다음 명령으로 nullable timestamp column을
한 번 추가한다.

```bash
python3 bl_cli.py upgrade-created-at
```

새 DB는 `db.create_all()`이 처음부터 컬럼을 생성하므로 이 명령이 no-op이다.

`User.email`과 `User.password_hash`는 query 결과 객체에 존재하더라도 template에
전달된 화면에서 읽거나 출력하지 않는다. Report의 `details`는 moderation case
내용이므로 내부 Inspector에서만 표시하며, 제품 사용자 화면이나 공개 JSON API에는
추가하지 않는다.

## 파일 역할

```text
db_inspector/
├── README.md
├── __init__.py                 # Blueprint 공개
├── routes.py                   # 접근 gate와 read-only query
└── templates/db_inspector/
    └── index.html              # 네 model table과 empty state
```

## 업그레이드 포인트

v0.1 이후 개선은 BorrowRequest 제품 UI와 D2 evidence가 끝난 뒤 검토한다.

1. row가 많아졌을 때 pagination 추가
2. ID 또는 status 기반 filter 추가
3. 관계 row로 이동하는 read-only link 추가
4. 데이터 변경 명령은 Inspector에 넣지 않고 `devtools/bl_cli/seed/`로 분리
5. 수정·삭제는 Inspector가 아니라 권한과 감사 기록을 가진 별도 설계로 처리

다음 기능은 이 Inspector에 추가하지 않는다.

- 임의 SQL console
- password 또는 private field 편집
- 무제한 CRUD
- database reset
- 제품용 Admin 또는 moderation 기능

### BorrowRequest Reset 버튼을 두지 않는 이유

Inspector의 계약은 **관찰만 하고 변경하지 않는 것**이다. 브라우저 Reset 버튼은
실수로 demo evidence를 삭제할 수 있고, CSRF가 적용된 POST, 2단계 확인과 audit log가
필요해진다. 따라서 화면에는 명령을 안내하되 실제 변경은 다음 BL-CLI로만 실행한다.

```bash
python3 bl_cli.py reset-demo-requests
```

향후 브라우저 변경 도구가 필요하면 Inspector가 아닌 별도 Danger Zone으로 분리한다.
운영 원칙은 [`Admin & Operator Manual`](../../../BOOKLOOP_ADMIN_OPERATOR_MANUAL.md)을
따른다.

## 확인

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider tests/test_dev_db_inspector.py
```

자동 테스트는 비활성화 시 `404`, 로컬 DEBUG 활성화 시 `200`, LAN guest 로그인 이동,
일반 회원 `403`, 내부 network의 관리자 `200`, 외부 source IP `404`, 세 model 표시,
민감정보 제외와 GET 요청 전후 row 수 불변을 확인한다.

## 외부 수동 검수 도구

`/dev/db/`는 BookLoop 안에 포함된 read-only 브라우저 Inspector다. 전체 SQLite
schema와 raw row를 수동으로 비교해야 할 때는 **DB Browser for SQLite** 같은
외부 SQLite client를 보완 도구로 사용할 수 있다.

```text
DB Browser for SQLite
→ instance/bookloop.db 열기
→ tables / schema / row 확인
→ 필요하면 read-only 모드로 검수
```

확인 대상 파일:

```text
app/backend/instance/bookloop.db
```

역할은 다음처럼 나눈다.

| 도구 | 역할 | 데이터 변경 |
| --- | --- | --- |
| `/dev/db/` | BookLoop route와 화면에서 관계·표시 필드 확인 | 금지 |
| DB Browser for SQLite | 전체 SQLite 구조와 raw row를 GUI로 비교 | 검수 중 read-only 권장 |
| `inspect_sqlite.py` | 자동화된 터미널 schema·row 확인 | 금지 |
| `sqlite3 -readonly` | 실제 DB 파일의 schema·row를 CLI로 확인 | 금지 |
| `bl-cli` | 명시적인 seed/reset 실행 | 허용된 명령만 |

DB Browser는 제품 기능이나 Admin UI가 아니며, Deliverable 2에서 새 의존성으로
커밋하지 않는다. 로컬 DB를 열기 전 Flask 개발 서버의 현재 DB 경로를 확인하고,
실제 사용자 데이터나 password field를 외부 도구로 공유하지 않는다.

## 문제 해결

### `/dev/db`가 `404`인 경우

1. 로컬 `.env`에 `ENABLE_DEV_DB_INSPECTOR=true`가 있는지 확인한다.
2. Rose LAN 검수라면 `ENABLE_LAN_DEV_DB_INSPECTOR=true`도 확인한다.
3. Main에서 `ss -ltnp | rg ':5000\b'`가 `0.0.0.0:5000`인지 확인한다.
4. ChromeOS TCP `5000` port forwarding과 현재 Main LAN IP를 확인한다.
5. Tony 관리자 계정으로 로그인했는지 확인한다.
6. 설정을 바꾼 뒤 개발 서버를 재시작한다.

일반 회원으로 로그인해 `403`이 나오면 network 연결은 성공했지만 관리자 권한이 없는
상태다. 비로그인 상태에서는 로그인 후 원래 `/dev/db/` 주소로 돌아온다.

### `/jinja/`에서 `no such table: user`가 발생한 경우

새 SQLite 파일만 있고 model table이 아직 생성되지 않은 상태다. 로컬 개발 진입점
`run.py`는 첫 요청 전에 `db.create_all()`을 실행해 **없는 table만 생성**한다.
기존 table이나 row를 삭제하지 않는다.

```text
run.py
→ app context
→ db.create_all()
→ Flask development server
```

향후 Flask-Migrate를 도입하면 이 개발 초기화 단계는 migration 명령으로 교체한다.
