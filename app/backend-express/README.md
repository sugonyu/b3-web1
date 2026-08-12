# BookLoop Express — Health API + EJS Reference

이 폴더는 D3 제품 backend를 교체하는 코드가 아니라, Flask에서 배운 구조를
Node.js/Express로 다시 구현하는 병렬공부용 독립 backend다.

현재 범위:

```text
GET /api/health
→ Express Router
→ framework-independent health service
→ JSON response

GET /ejs/
→ Express Router
→ 같은 health service
→ response.render()
→ EJS template
→ HTML response
```

`/ejs/`는 제품 UI가 아니라 Flask `/jinja/`와 server rendering을 비교하는
최소 병렬공부 화면이다.

## Flask ↔ Express 구조 비교

| 🐍 Flask | 🟨 Express | 역할 |
| --- | --- | --- |
| `run.py` | `src/server.js` | server 실행 entry point |
| `create_app()` | `createApp()` | application 조립 |
| Blueprint | Router | route module |
| `services/health.py` | `src/services/health.js` | framework-independent data/rule |
| `jsonify()` | `response.json()` | JSON HTTP response |
| `render_template()` | `response.render()` | server-rendered HTML 생성 |
| Jinja template | EJS template | 데이터를 HTML에 삽입 |
| pytest/unittest | `node:test` | 자동 검증 |

### Jinja ↔ EJS 같은 흐름

```text
🐍 Flask /jinja/
→ Jinja route
→ health service
→ render_template()
→ Jinja
→ HTML

🟨 Express /ejs/
→ Express Router
→ health service
→ response.render()
→ EJS
→ HTML
```

## 설치와 실행

```bash
cd app/backend-express
npm install
npm start
```

브라우저 또는 `curl`:

```text
http://127.0.0.1:3001/api/health
http://127.0.0.1:3001/ejs/
```

예상 응답:

```json
{
  "app": "BookLoop",
  "service": "express-api",
  "status": "ok",
  "version": "0.1.0"
}
```

자동 테스트:

```bash
npm test
```

## 현재 중단선

- EJS는 `/ejs/` health 참고 화면 하나에서만 사용한다.
- database, ORM, authentication과 CRUD를 추가하지 않는다.
- Flask backend를 교체하거나 D3 canonical backend로 취급하지 않는다.
- EJS 화면을 BookLoop 제품 UI나 React 대체물로 확장하지 않는다.
- 다음 API 단계는 Flask와 Express의 health contract를 같은 client에서 비교하는 것이다.

전체 단계는
[`BookLoop Flask ↔ Express API Parity Roadmap`](../../docs/planning/BOOKLOOP_FLASK_EXPRESS_API_PARITY_ROADMAP.md)을
따른다.
