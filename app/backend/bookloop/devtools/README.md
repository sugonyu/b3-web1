# BookLoop Developer Tools

이 폴더는 BookLoop 제품 기능이 아니라 **로컬 개발과 디버깅을 돕는 내부 도구**를
분리해 둔다.

## 경계

```text
bookloop/api.py, client_*.py, services/  → 사용자가 사용하는 제품 코드
bookloop/devtools/                       → 개발자가 로컬에서만 사용하는 보조 코드
```

- 개발도구 route는 기본적으로 비활성화한다.
- 운영·공개 환경에서는 존재를 드러내지 않고 `404`를 반환한다.
- 제품의 로그인·권한·service 규칙을 우회하는 관리 기능을 만들지 않는다.
- private field, password, secret과 실제 사용자 데이터를 노출하지 않는다.
- 도구마다 독립 폴더와 README를 두어 목적과 중단선을 기록한다.

## 현재 도구

| 폴더 | 역할 | 상태 |
| --- | --- | --- |
| [`db_inspector/`](db_inspector/README.md) | 세 핵심 SQLAlchemy model을 읽기 전용으로 확인 | v0.1 |
| [`seed/`](seed/README.md) | D2 데모 시작 데이터를 재현하는 Flask CLI 명령 | v0.1 |

## 미래 확장 규칙

새 도구는 실제 디버깅 필요가 생겼을 때만 추가한다. 예를 들어 seed 또는 reset이
필요해져도 `db_inspector`에 섞지 않고 별도 책임으로 설계한다. 수정·삭제 기능은
개발 편의보다 데이터 안전성과 D2 제품 범위를 먼저 검토한 뒤 결정한다.
