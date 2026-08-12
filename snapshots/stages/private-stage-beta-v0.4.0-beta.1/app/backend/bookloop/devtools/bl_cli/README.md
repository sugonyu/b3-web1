# BookLoop CLI (BL-CLI)

BL-CLI는 BookLoop의 로컬 개발·발표 준비 명령을 한 입구로 제공한다. 명령을 직접
구현하기보다 `bl_cli/seed/`처럼 책임이 분리된 하위 기능의 Python 함수를 조립한다.

코드 맵 버전은 다음처럼 관리한다.

- `bookloop/README-v1.0-d2.html`: D2 v1.0 기준선 — Flask package 중심의 원래 구조
- `bookloop/README.html`: v1.1 현재본 — `bl_cli.py`와 `bl_cli/seed/` 흐름 포함

따라서 v1.0은 과거 구조를 비교할 때 보존하고, 일상적인 현재 구조 확인은 항상
`README.html`에서 시작한다.

## 구조

```text
backend/bl_cli.py
└── bookloop/devtools/bl_cli/
    ├── commands.py
    │   ├── seed-demo → seed.seed_demo_data()
    │   ├── reset-demo-requests → seed.reset_demo_requests()
    │   └── upgrade-created-at → 기존 DB의 timestamp schema 보완
    └── seed/
        └── commands.py
```

- `backend/bl_cli.py`: 터미널에서 실행하는 얇은 진입점
- `commands.py`: Click command 이름, 출력과 Flask app context 조립
- `seed/`: `commands.py`와 같은 레벨의 기능 폴더
- `seed/commands.py`: 실제 seed/reset 데이터 작업

## 실행

```bash
cd app/backend
source .venv/bin/activate
python3 bl_cli.py --help
```

명령을 생략하고 `python3 bl_cli.py`만 실행해도 BL-CLI의 용도, 사용법과 현재 사용
가능한 명령을 출력하고 정상 종료한다. 처음 사용하는 사람은 명령 이름을 외울 필요가
없다.

```text
BL-CLI
├── seed-demo
├── reset-demo-requests
└── upgrade-created-at
```

기존 SQLite를 새 `created_at` model과 맞출 때 한 번 실행한다. table과 row를 삭제하지
않고 세 table에 nullable column만 추가한다. 가상환경을 활성화하지 않았다면 프로젝트
interpreter를 직접 사용한다.

```bash
.venv/bin/python bl_cli.py upgrade-created-at
```

Seed는 BL-CLI가 제공하는 기능이므로 `bl_cli/seed/`에 포함한다. 다만 상위
`commands.py`는 CLI 입력·출력을, `seed/commands.py`는 실제 DB 작업을 맡도록
한 단계 안에서도 책임을 분리한다.

제품 route나 `/dev/db/`에 쓰기 버튼을 추가하지 않고, 명시적으로 실행한 CLI만
개발 데이터를 변경하도록 경계를 유지한다.

## DB 검수 도구와의 관계

BL-CLI는 데이터를 준비하거나 명시적으로 reset하는 **변경 도구**다. 데이터가
정말 저장되었는지 확인하는 일은 별도 read-only 도구가 담당한다.

```text
bl-cli seed/reset
→ Flask application context
→ SQLAlchemy · SQLite
→ /dev/db/ 관계·표시 확인
→ DB Browser for SQLite raw schema·row 교차 확인
```

수동 검수용 SQLite 파일은 다음 위치다.

```text
app/backend/instance/bookloop.db
```

DB Browser for SQLite는 MySQL Workbench와 비슷한 GUI 확인 도구지만 BookLoop
runtime의 일부가 아니다. 따라서 설치 파일이나 GUI 설정을 프로젝트에 넣지 않고,
필요할 때 로컬 파일을 read-only로 열어 `/dev/db/`, `inspect_sqlite.py` 결과와
비교한다. row를 지우거나 다시 만들 때는 GUI가 아니라 명시적인 BL-CLI 명령을
사용한다.

## 간단한 확장 로드맵

```text
BL-CLI
├── seed/           ✅ 현재 · demo 생성과 선택적 request 초기화
├── export/         ⏳ 필요할 때 · 발표 증거와 익명화된 demo data 내보내기
└── diagnostics/    ⏳ 필요할 때 · 설정, DB 연결과 table 상태 점검
```

새 하위 기능은 실제 반복 작업이 생기고 테스트 범위를 정의할 수 있을 때만 추가한다.
제품 사용자용 기능, 전체 DB 삭제와 운영 관리자 기능은 BL-CLI의 범위에 넣지 않는다.

## CLI, Skill, MCP 중 현재 선택

```text
Tony 또는 Codex
→ Skill: 반복 작업의 순서·안전 규칙·검증 방법
→ BL-CLI: 실제 로컬 명령 실행
→ Flask application context
→ SQLAlchemy · SQLite
```

세 도구는 경쟁 관계가 아니라 서로 다른 층이다.

| 도구 | BookLoop에서의 역할 | 현재 판단 |
| --- | --- | --- |
| BL-CLI | Seed, reset, 향후 export·diagnostics를 실제 실행 | 지금 사용 |
| Codex Skill | 명령 전후 확인, 데모 준비와 문서화 절차 표준화 | 반복 작업이 쌓이면 작성 |
| MCP server | 외부 AI·앱이 구조화된 방식으로 BookLoop 도구를 호출 | Web1 이후 필요할 때 검토 |

WP-CLI처럼 BL-CLI가 실제 작업 엔진이고, Skill은 그 엔진을 안전하고 일관되게 쓰는
운영 설명서다. MCP는 여러 외부 클라이언트가 같은 기능을 호출해야 할 때 추가하는
연결 계층이다. Deliverable 2에서는 MCP가 범위를 불필요하게 키우므로 도입하지 않는다.

권장 발전 순서:

```text
BL-CLI 기능과 테스트 완성
→ 반복되는 운영 절차를 BL-CLI Skill로 정리
→ 외부 통합 요구가 확인되면 MCP 검토
```

### 병렬공부 왕복 참조

- [BookLoop BL-CLI ↔ CMS WP-CLI ↔ AI Skill/MCP 브리지](file:///home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/apps/ACS/parallel-study/mappings/bookloop-wpcli-ai-tooling-bridge.md)
- [B3 CMS WordPress Lab · WP-CLI](file:///home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-cms/README.md)
- [AI 공부 · CLI, Skill, MCP 선택 가이드](file:///home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/apps/ai-learning/openai-codex-cli/CLI_SKILL_MCP_DECISION_GUIDE.md)
