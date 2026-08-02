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
http://127.0.0.1:3000/b3-web1/app/frontend-vanilla/
```

- VS Code Live Preview 같은 static server가 이 폴더의 파일을 직접 제공한다.
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
Live Preview static server ─────────────┐
                                        ├─> app/frontend-vanilla/
Flask client_vanilla.py on port 5000 ──┘
```

어느 주소로 열어도 실행되는 실제 파일은 이 폴더의 `index.html`, `style.css`,
`app.js`다.

## Flask API

`app.js`는 현재 학습용으로 다음 API 주소를 명시적으로 사용한다.

```text
http://127.0.0.1:5000/api/health
```

따라서 두 입구 중 어느 쪽으로 화면을 열어도 같은 Flask API를 호출한다.
