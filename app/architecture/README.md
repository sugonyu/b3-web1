# BookLoop Architecture

이 폴더는 BookLoop의 model, API, authentication, frontend/backend boundary와
프로젝트 구조를 반복적으로 관리하는 기술 설계 evidence 본진이다.

브라우저에서는 [`index.html`](index.html)을 먼저 열어 현재 architecture 버전과
이후 iteration 계획을 확인한다.

폴더와 표준 파일 이름은 [BookLoop artifact naming convention](../ARTIFACT_NAMING_CONVENTION.md)을
따른다.

## 현재 버전

| 버전 | Deliverable | 범위 | 상태 |
| --- | --- | --- | --- |
| [v1.0 D1 Foundation](drafts/v1.0-d1-foundation-ko/README.md) | 🧩 D1 | 모델 관계, 현재 tree, 목표 구조 | 한국어 기준선 |
| [v1.1 English Translation](drafts/v1.1-d1-foundation-en/README.md) | 🧩 D1 | v1.0과 동일한 기술 내용을 영어로 번역 | 현재 발표용 번역본 |

v1.1은 기능이나 architecture 변경이 아니다. v1.0의 같은 D1 evidence를 영어로
옮긴 언어 버전이다.

## Architecture와 다른 폴더의 경계

- `architecture/`: 기술 구조와 결정 이유
- `design-system/`: 색상, typography, UI components와 화면 상태
- `backend/`: 실제 Flask, SQLAlchemy와 API 구현
- `frontend-*`: 실제 browser client 구현
- `docs/planning/`: 일정, handoff, 의사결정과 다음 행동

Architecture 문서는 구현을 대신하지 않는다. 매 Deliverable에서 실제 코드와 맞는지
확인한 뒤 새 버전에 차이를 기록한다.

## Iterative lifecycle

```text
D1 v1.0: Korean architecture baseline
→ D1 v1.1: English translation of the same evidence
→ D2 v2.x: authentication + database workflow
→ D3 v3.x: React–Flask data flow
→ D4 v4.x: testing + errors + deployment structure
→ Final v5.x: stable architecture matching the current app
```

## Browser URL

```text
http://localhost:8080/pub/b3-web1/app/architecture/
```
