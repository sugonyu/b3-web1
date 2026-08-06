# BookLoop Vanilla Client

이 폴더는 Flask와 분리된 순수 HTML/CSS/JavaScript client의 독립 source다.

```text
frontend/js-vanilla/
├── index.html
├── style.css
└── app.js
```

## Independent Execution Boundary

```text
http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/
```

- Docker static server가 이 폴더의 파일을 직접 제공한다.
- Flask API와 port가 다르므로 다른 origin이다.
- `app.js`가 Flask JSON API를 `fetch()`하려면 Flask의 CORS 허용이 필요하다.

## Sibling Flask Vanilla

```text
http://127.0.0.1:5000/vanilla/
```

- Flask 전용 source는 `backend/bookloop/flask_vanilla/`에 별도로 보관한다.
- `backend/bookloop/clients/client_vanilla.py`가 Flask 전용 source를 제공한다.
- 두 실행 경계는 서로 링크하지만 같은 파일을 공유하지 않는다.

```text
🟨 Independent JS Vanilla :8080 → app/frontend/js-vanilla/
🐍🟨 Flask Vanilla :5000      → backend/bookloop/flask_vanilla/
```

## La Bella Vita CMS Theme

독립 static client는 La Bella Vita WordPress CMS와 같은 port `8080`에서 제공된다.
따라서 이 실행 문맥을 눈으로 구별하고 CMS 홈으로 쉽게 돌아갈 수 있도록 La Bella
Vita의 실제 palette와 typography를 재사용한다.

```text
Cream    #FAF9F5
Tomato   #A83226
Olive    #4A5A24
Charcoal #2F3320
Heading  Playfair Display
Body     Lato
```

화면 상단의 `← La Bella Vita CMS`는 `http://localhost:8080/news/`로 돌아간다.
테마는 hosting context를 설명하지만 client의 기술 정체성은 계속 🟨 Independent
Vanilla JavaScript다. Flask `/vanilla/`는 별도 Flask 전용 복사본과 🐍🟨 정체성을
사용한다.

## Flask API

`app.js`는 현재 학습용으로 다음 API 주소를 명시적으로 사용한다.

```text
http://127.0.0.1:5000/api/health
```

따라서 이 독립 client도 database에 직접 접근하지 않고 Flask API를 호출한다.

## Development Server Checks

Vanilla 화면은 두 local development server의 도달 가능 여부를 확인한다.

| Check | URL | 확인 범위 |
| --- | --- | --- |
| Flask server + API | `http://127.0.0.1:5000/api/health` | HTTP status와 JSON 내용 |
| VS Code Live Preview | `http://127.0.0.1:3000/b3-web1/index.html?vscode-livepreview=true` | network 도달 가능 여부 |

Live Preview는 port `8080`과 다른 origin이며 CORS 응답을 전제로 하지 않는다.
따라서 `no-cors` fetch로 server reachability만 확인하고, 실제 page 내용은 `Open
Web1 Live Preview` 링크로 직접 연 뒤 확인한다.
