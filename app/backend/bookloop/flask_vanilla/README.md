# BookLoop Flask Vanilla Client

이 폴더는 Flask의 `/vanilla/` route가 제공하는 전용 HTML/CSS/JavaScript source다.

```text
flask_vanilla/
├── index.html
├── style.css
└── app.js
```

## Flask Execution Boundary

```text
http://127.0.0.1:5000/vanilla/
```

- `backend/bookloop/clients/client_vanilla.py`가 이 폴더를 제공한다.
- Jinja를 사용하지 않고 브라우저에서 순수 JavaScript를 실행한다.
- 같은 origin의 Flask JSON API를 `fetch()`한다.

## Sibling Independent Vanilla

```text
http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/
```

- 독립 source는 `app/frontend/js-vanilla/`에 별도로 보관한다.
- 두 client는 서로 링크하지만 같은 파일을 공유하지 않는다.

```text
🐍🟨 Flask Vanilla :5000      → bookloop/flask_vanilla/
🟨 Independent JS Vanilla :8080 → app/frontend/js-vanilla/
```

## La Bella Vita CMS Theme

이 Flask 전용 복사본도 Vanilla UI 비교를 위해 La Bella Vita palette와 typography를
유지하지만, 실행 문맥과 상단 링크는 Flask port `5000`을 표시한다.

```text
Cream    #FAF9F5
Tomato   #A83226
Olive    #4A5A24
Charcoal #2F3320
Heading  Playfair Display
Body     Lato
```

화면 상단의 `← BookLoop Flask home`은 `http://127.0.0.1:5000/`으로 돌아간다.
이 client의 기술 정체성은 🐍🟨 Flask Vanilla다.

## Flask API

`app.js`는 현재 학습용으로 다음 API 주소를 명시적으로 사용한다.

```text
http://127.0.0.1:5000/api/health
```

따라서 이 client도 SQLite에 직접 접근하지 않고 Flask API를 호출한다.

## Development Server Checks

Vanilla 화면은 두 local development server의 도달 가능 여부를 확인한다.

| Check | URL | 확인 범위 |
| --- | --- | --- |
| Flask server + API | `http://127.0.0.1:5000/api/health` | HTTP status와 JSON 내용 |
| VS Code Live Preview | `http://127.0.0.1:3000/b3-web1/index.html?vscode-livepreview=true` | network 도달 가능 여부 |

Live Preview는 port `8080`과 다른 origin이며 CORS 응답을 전제로 하지 않는다.
따라서 `no-cors` fetch로 server reachability만 확인하고, 실제 page 내용은 `Open
Web1 Live Preview` 링크로 직접 연 뒤 확인한다.
