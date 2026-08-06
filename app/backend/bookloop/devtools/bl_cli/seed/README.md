# Seed Tool · D2 Demo Data

배달 2 브라우저 데모의 시작 데이터와 BorrowRequest 초기화를 HTTP 버튼이 아닌
명시적인 Python CLI 명령으로 관리한다. `/dev/db/`는 계속 read-only다.

## BL-CLI entry point

Seed의 데이터 작업은 BL-CLI 아래의 이 폴더에 두고, 상위 `commands.py`가 터미널
명령으로 조립한다. 터미널 진입점만 Flask 서버 진입점 옆에 둔다.

```text
app/backend/
├── run.py       # python3 run.py
├── bl_cli.py    # 얇은 python3 실행 진입점
└── bookloop/devtools/bl_cli/
    ├── commands.py  # command 조립
    └── seed/        # 실제 데이터 작업
```

권장 실행법:

```bash
cd app/backend
source .venv/bin/activate
python3 bl_cli.py --help
python3 bl_cli.py seed-demo
python3 bl_cli.py reset-demo-requests
```

가상환경을 활성화한 뒤에는 Flask CLI 문법 없이 `python3`만 사용하면 된다. 시스템
기본 Python에 Flask 의존성이 설치되어 있지 않다면 활성화 없이 실행할 수 없다.
가상환경을 활성화하지 않을 때는 `python3` 대신 `.venv/bin/python`을 사용한다.

기존 `flask --app run ...` 명령도 같은 Python 함수를 사용하므로 호환용으로 계속
지원하지만, 일상적인 실행은 `python3 bl_cli.py ...`를 권장한다.

사용자에게 Seed는 BL-CLI 아래의 명령으로 보이고 코드 위치도 같은 포함 관계를
따른다. `seed/` 하위 폴더에서는 CLI 화면과 데이터베이스 작업 로직을 분리하여
테스트하고, 향후 다른 명령에서도 같은 함수를 재사용할 수 있다.

## Current commands

| 명령 | 역할 | 삭제 범위 |
| --- | --- | --- |
| `seed-demo` | Tony·Mina·Alex와 The Odyssey를 준비 | 삭제하지 않음 |
| `reset-demo-requests` | live request 시연 전 demo 요청 초기화 | Mina의 The Odyssey 요청만 삭제 |

## 1. Seed the starting data

생성 대상:

- 사용자 `tony` — borrower
- 사용자 `mina` — The Odyssey listing owner
- 사용자 `alex` — authorization boundary 확인용 unrelated user
- Mina 소유의 대여 가능한 `The Odyssey` BookListing

`BorrowRequest`는 만들지 않는다. 발표 중 Tony가 실제 Jinja 폼으로 생성해야
validation, SQLite persistence와 갱신된 화면을 증명할 수 있기 때문이다.

```bash
cd app/backend
export BOOKLOOP_DEMO_PASSWORD='local-demo-password'
python3 bl_cli.py seed-demo
```

현재 수업 데모에서는 Tony, Mina, Alex가 기억하기 쉬운 공통 암호 `1111`을 사용한다.
이 값은 로컬 데모 전용이며 실제 사용자 계정이나 운영 환경의 암호 정책이 아니다.

같은 명령을 다시 실행해도 같은 username과 Mina의 The Odyssey listing을 중복 생성하지
않으며, 세 데모 계정의 password hash는 현재 환경변수 값으로 동기화한다. 이 명령은
기존 row를 삭제하거나 데이터베이스를 reset하지 않는다.

## 2. Reset only the demo BorrowRequests

```bash
cd app/backend
python3 bl_cli.py reset-demo-requests
```

이 명령은 Mina의 `The Odyssey` listing에 연결된 BorrowRequest만 삭제한다. User,
BookListing과 다른 책의 BorrowRequest는 유지한다. 같은 명령을 다시 실행해도 오류가
나지 않으며 `deleted=0`을 출력한다.

예상 출력:

```text
Demo BorrowRequest reset complete: deleted=1; remaining BorrowRequests=0.
```

발표 전 권장 순서:

```text
seed-demo
→ reset-demo-requests
→ /dev/db/에서 Borrow Requests 0 rows 확인
→ Tony 로그인
→ Request this book
→ /dev/db/에서 Borrow Requests 1 row 확인
```

이 CLI는 local classroom demo 도구이며 제품 Admin 기능이나 전체 database reset
기능으로 확장하지 않는다.
