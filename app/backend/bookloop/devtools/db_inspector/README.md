# Developer Database Inspector v0.1

BookLoop의 `User`, `BookListing`, `BorrowRequest` row와 관계 ID를 브라우저에서
빠르게 확인하는 **개발 전용 read-only 화면**이다.

전체 계획과 제품 UI 우선순위는
[`D2 Developer Database Inspector Roadmap`](../../../../../docs/planning/D2_DEV_DATABASE_INSPECTOR_ROADMAP.md)을
따른다.

## 실행 조건

다음 두 조건이 모두 참일 때만 `/dev/db`가 열린다.

```text
Flask DEBUG = true
ENABLE_DEV_DB_INSPECTOR = true
```

로컬 `.env` 예시:

```env
ENABLE_DEV_DB_INSPECTOR=true
```

그 외 환경에서는 같은 주소가 `404`를 반환한다. `.env.example`의 기본값은
`false`이며 실제 `.env`는 Git에 기록하지 않는다.

## v0.1이 보여주는 값

| Model | 표시 필드 |
| --- | --- |
| User | `id`, `username`, `general_area` |
| BookListing | `id`, `title`, `author`, `availability`, `owner_id` |
| BorrowRequest | `id`, `status`, `listing_id`, `borrower_id` |

`User.email`과 `User.password_hash`는 query 결과 객체에 존재하더라도 template에
전달된 화면에서 읽거나 출력하지 않는다.

## 파일 역할

```text
db_inspector/
├── README.md
├── __init__.py                 # Blueprint 공개
├── routes.py                   # 접근 gate와 read-only query
└── templates/db_inspector/
    └── index.html              # 세 model table과 empty state
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

## 확인

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider tests/test_dev_db_inspector.py
```

자동 테스트는 비활성화 시 `404`, 활성화 시 `200`, 세 model 표시,
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
| `bl-cli` | 명시적인 seed/reset 실행 | 허용된 명령만 |

DB Browser는 제품 기능이나 Admin UI가 아니며, Deliverable 2에서 새 의존성으로
커밋하지 않는다. 로컬 DB를 열기 전 Flask 개발 서버의 현재 DB 경로를 확인하고,
실제 사용자 데이터나 password field를 외부 도구로 공유하지 않는다.

## 문제 해결

### `/dev/db`가 `404`인 경우

1. 로컬 `.env`에 `ENABLE_DEV_DB_INSPECTOR=true`가 있는지 확인한다.
2. Flask가 debug mode로 실행됐는지 확인한다.
3. 설정을 바꾼 뒤 개발 서버를 재시작하거나 reloader 반영을 확인한다.

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
