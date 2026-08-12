# BookLoop Model Diagram and Project Structure

> Version: Architecture v1.0 — Korean baseline
> Week 1 · 🧩 Deliverable 1 — Definition and Design
> Evidence status: private presentation draft
> Verified against: `app/backend/bookloop/models.py` and the current `app/` tree

브라우저용 문서: [BookLoop Model Diagram and Project Structure HTML](index.html)

## 목적

이 문서는 BookLoop의 세 데이터 모델이 왜 필요한지, 서로 어떻게 연결되는지와
현재 코드가 어떤 폴더로 나뉘는지를 Deliverable 1 발표용으로 간단히 보여준다.

## Model relationship diagram

```text
User (owner)       1 ─────────── many BookListing
User (borrower)    1 ─────────── many BorrowRequest
BookListing        1 ─────────── many BorrowRequest
```

다르게 읽으면 다음과 같다.

```text
한 User는 여러 BookListing을 소유한다.
한 User는 여러 BorrowRequest를 만든다.
한 BookListing은 여러 BorrowRequest를 받을 수 있다.
각 BorrowRequest는 책 1개와 요청자 1명을 연결한다.
```

## Core model fields

### User

| Field | 역할 |
| --- | --- |
| `id` | 사용자를 구분하는 primary key |
| `username` | 공개 화면에서 사용할 고유 이름 |
| `email` | 로그인·연락용 비공개 정보 |
| `password_hash` | 평문 비밀번호 대신 저장하는 인증 정보 |
| `general_area` | 정확한 주소 대신 공개하는 일반 지역 |

### BookListing

| Field | 역할 |
| --- | --- |
| `id` | 책 등록을 구분하는 primary key |
| `title` | 책 제목 |
| `author` | 저자 |
| `availability` | 현재 대여 요청 가능 여부 |
| `owner_id` | 책 등록을 소유한 User foreign key |

### BorrowRequest

| Field | 역할 |
| --- | --- |
| `id` | 대여 요청을 구분하는 primary key |
| `status` | `pending`, `approved`, `rejected`, `returned` 상태 기록 |
| `listing_id` | 요청한 BookListing foreign key |
| `borrower_id` | 요청을 만든 User foreign key |

## BorrowRequest가 supporting model인 이유

`User + BookListing`만 있으면 사용자는 책과 소유자의 일반 정보만 보고 외부에서
연락해야 한다. `BorrowRequest`를 추가하면 요청, 승인·거절과 반납 완료를 앱 안에서
기록할 수 있다. 이 완료 기록은 이후 optional trust rating의 근거로 확장할 수 있다.

## Privacy boundary

공개 책 목록에는 `username`과 `general_area`만 표시한다. `email`, `password_hash`,
정확한 주소와 전화번호는 공개 JSON에 포함하지 않는다. 연락 정보 공개 시점과
방식은 인증·승인 workflow를 구현하면서 다시 결정한다.

## Current project structure

아래는 현재 실제로 존재하는 private 실험 구조다.

```text
app/
├── README.md                         # 전체 실험실 시작점과 실행 안내
├── architecture/                     # model·API·기술 구조 version evidence
│   ├── index.html                    # architecture 버전 인덱스
│   └── drafts/
│       ├── v1.0-d1-foundation-ko/    # 한국어 기준선
│       └── v1.1-d1-foundation-en/    # 영어 번역본
├── backend/
│   ├── run.py                        # Flask 실행 진입점
│   ├── requirements.txt              # Python dependency
│   ├── API_CONTRACT.md               # 7개 핵심 JSON endpoint 약속
│   ├── bookloop/
│   │   ├── __init__.py               # app factory와 Blueprint 연결
│   │   ├── database.py               # SQLAlchemy 객체
│   │   ├── models.py                 # User, BookListing, BorrowRequest
│   │   ├── api.py                    # health와 제품 JSON API
│   │   ├── client_jinja.py           # Flask/Jinja 비교 client
│   │   ├── client_vanilla.py         # 공유 Vanilla client route
│   │   ├── services/health.py        # health response data
│   │   ├── templates/web/            # Jinja client template
│   │   └── static/web/               # Flask가 제공하는 Vanilla assets
│   └── tests/                         # model, API와 client 자동 검사
├── frontend-vanilla/                  # Flask와 분리된 독립 browser client
└── design-system/
    ├── index.html                     # draft 선택·비교·Agile lifecycle
    └── drafts/
        ├── v1.0-d1-foundation/        # 최초 디자인 기준선
        └── v1.1-d1-uiux-bridge/       # 채택한 D1 Design System MVP v0.1
```

`.venv`, `instance`, cache와 생성 파일은 발표용 구조에서 제외한다.

## Chosen frontend track and current boundary

선택한 목표 stack은 다음과 같다.

```text
React client
    ↓ JSON over HTTP
Flask JSON API
    ↓ SQLAlchemy ORM
SQLite relational database
```

현재는 Flask API·database models·Vanilla/Jinja 비교 client와 디자인 시스템이
존재한다. React client는 아직 구현하지 않았으며, D2 이후 독립 frontend로 추가한다.
Jinja와 Vanilla client는 구조와 API를 학습·비교하기 위한 private evidence이지
최종 React 화면이라고 발표하지 않는다.

## 발표용 짧은 설명

> BookLoop uses three related models. A user can own many book listings and can
> create many borrow requests. Each borrow request connects one borrower to one
> listing and records the borrowing status. The current Flask API and SQLAlchemy
> models are separated from the browser clients, so the future React client can
> consume the same JSON API without changing the database model.

## Source evidence

- [`models.py`](../../../backend/bookloop/models.py)
- [`API_CONTRACT.md`](../../../backend/API_CONTRACT.md)
- [Design System MVP v0.1](../../../design-system/drafts/v1.1-d1-uiux-bridge/README.md)
- [Authentication implementation roadmap](../../../../docs/planning/AUTHENTICATION_IMPLEMENTATION_ROADMAP.md)

## 다음 iteration

- D1: 이 diagram과 현재·목표 구조를 발표 evidence로 사용
- D2: 로그인과 `current_user`를 연결한 뒤 인증 경계를 갱신
- D3: React folder와 실제 frontend/backend data flow를 tree에 추가
- D4: 배포·테스트·접근성 구조를 최종 architecture evidence에 반영
