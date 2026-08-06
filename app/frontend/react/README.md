# BookLoop React Client

이 폴더는 BookLoop의 미래 독립 React client를 위한 확장 경계다. 현재는 위치와
API 연결 계약만 확정한 문서 scaffold이며, React 또는 Vite package는 아직 설치하지
않았다.

## Current Status

```text
⚛️ frontend/react/          문서 scaffold만 준비
🟨 frontend/js-vanilla/     현재 독립 JavaScript 참고 구현
🐍 backend/bookloop/        Flask JSON API와 공통 service
```

Deliverable 2의 현재 데모와 검증은 Python/Jinja 및 Flask backend를 중심으로
유지한다. React 구현은 현재 D2 완료 기능으로 주장하지 않는다.

## Planned Connection

```text
⚛️ React client
→ fetch()
→ Flask api.py · /api/*
→ services/borrow_requests.py
→ SQLAlchemy
→ SQLite
```

React는 SQLite에 직접 접근하지 않는다. 🟨 Independent Vanilla와 마찬가지로
Flask JSON API를 호출하고, Jinja와 같은 validation·authorization·transaction
규칙을 공유한다.

## Planned Source Shape

실제 React 작업을 시작할 때 필요한 최소 구조다. 현재는 이 하위 파일과 폴더를
미리 만들지 않는다.

```text
frontend/react/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│       └── api.js
├── package.json
└── README.md
```

## Activation Gate

다음 조건을 확인한 뒤 React/Vite scaffold를 시작한다.

1. Deliverable 2의 Flask vertical slice가 검증되고 보존된다.
2. 현재 Vanilla UI에서 재사용할 화면 흐름과 API endpoint를 정한다.
3. React client가 사용할 인증 방식과 CORS 범위를 확인한다.
4. Tony가 React 구현 시작을 명시적으로 결정한다.

그전까지 이 폴더는 Vanilla → React 전환 계획을 보여주는 문서 경계로만 유지한다.
