# BookLoop Vanilla Client

이 폴더는 Flask와 분리된 순수 HTML/CSS/JavaScript client의 단일 source다.

```text
frontend-vanilla/
├── index.html
├── style.css
└── app.js
```

클라이언트 코드가 두 벌 있는 것이 아니다. 이 실제 폴더 하나를 서로 다른 두
web server가 제공하므로 두 주소로 확인할 수 있다.

## One Codebase, Two Entrances

### 1. 독립 static client

```text
http://localhost:8080/pub/b3-web1/app/frontend-vanilla/
```

- Docker static server가 이 폴더의 파일을 직접 제공한다.
- Flask API와 port가 다르므로 다른 origin이다.
- `app.js`가 Flask JSON API를 `fetch()`하려면 Flask의 CORS 허용이 필요하다.

### 2. Flask 보조 제공 경로

```text
http://127.0.0.1:5000/vanilla/
```

- `backend/bookloop/client_vanilla.py`가 같은 폴더를 찾아 제공한다.
- HTML/CSS/JavaScript를 backend 안으로 복사하지 않는다.
- 이 경로는 독립 client를 Flask에서도 비교·확인하기 위한 보조 입구다.

## Shared Folder Map

```text
localhost:8080 static server ───────────┐
                                        ├─> app/frontend-vanilla/
Flask client_vanilla.py on port 5000 ──┘
```

어느 주소로 열어도 실행되는 실제 파일은 이 폴더의 `index.html`, `style.css`,
`app.js`다.

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
테마는 hosting context를 설명하지만 client의 기술 정체성은 계속 🟨 독립 Vanilla
JavaScript다. 같은 source를 Flask `/vanilla/`에서도 제공하므로 두 입구의 화면은
동일하며, favicon도 두 경로 모두 🟨을 유지한다.

## Flask API

`app.js`는 현재 학습용으로 다음 API 주소를 명시적으로 사용한다.

```text
http://127.0.0.1:5000/api/health
```

따라서 두 입구 중 어느 쪽으로 화면을 열어도 같은 Flask API를 호출한다.

## Development Server Checks

Vanilla 화면은 두 local development server의 도달 가능 여부를 확인한다.

| Check | URL | 확인 범위 |
| --- | --- | --- |
| Flask server + API | `http://127.0.0.1:5000/api/health` | HTTP status와 JSON 내용 |
| VS Code Live Preview | `http://127.0.0.1:3000/b3-web1/index.html?vscode-livepreview=true` | network 도달 가능 여부 |

Live Preview는 port `8080`과 다른 origin이며 CORS 응답을 전제로 하지 않는다.
따라서 `no-cors` fetch로 server reachability만 확인하고, 실제 page 내용은 `Open
Web1 Live Preview` 링크로 직접 연 뒤 확인한다.
