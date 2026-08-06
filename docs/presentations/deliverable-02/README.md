# BookLoop Deliverable 2 Presentation Archive

> Created: 2026-08-02
> Status: v1.0 English presentation verified after W2-10 review
> Role: private preparation and presentation archive

## Presentation HTML

- [Current English presentation](presentation.html)
  - Versionless working copy; continue future presentation updates here
- [Code Defense Q&A](CODE_DEFENSE_QA.md)
  - 파일·route·service·DB 위치를 방어 형식으로 설명하는 발표 준비 문서
- [Presentation v1.0 — English](presentation-v1.0.html)
  - Frozen v1.0 baseline; W2-10 persistence review complete and LAB SLOT placeholders replaced with the verified D2 story
  - Flask startup, seed, shared service, Jinja browser flow, access boundary, restart persistence, and 67-test evidence summarized

- [Presentation v0.3 draft](presentation-v0.3-draft.html)
  - Kamyar의 privacy 피드백을 D2 authorization과 이후 Report/Admin 로드맵에 연결
  - Report와 Admin View는 future scope로 표시하며 D2 완료 기능으로 주장하지 않음
- [Presentation v0.3 draft — 한국어](presentation-v0.3-draft-ko.html)
  - 영어 원본의 00–11 구조, 기술 상태, LAB SLOT을 그대로 유지한 한국어 검토·발표 보조본
  - 기술 식별자와 HTTP 상태코드는 원형을 유지하고 설명 문장과 접근성 문구를 한국어화
- [Presentation v0.3 draft — 20-minute script](presentation-v0.3-draft-script.md)
  - v0.3 HTML과 동일한 순서의 발표문·진행 메모·privacy-feedback Q&A
- [Presentation v0.2 draft](presentation-v0.2-draft.html)
  - v0.3 생성 전 보존한 발표 구조와 vertical-slice 기준선
- [Presentation v0.2 draft — 20-minute script](presentation-v0.2-draft-script.md)
  - v0.2 HTML과 짝을 이루는 보존 원고

## Presentation Versioning Rule

`deliverable-02/`의 `02`는 수업의 두 번째 제출 단계를 뜻한다. 버전이 필요한
보존본은 `presentation-v1.0.html`처럼 번호를 붙이고, 현재 계속 수정하는 파일은
`presentation.html`로 유지한다. 따라서 브라우저 링크와 다음 발표 작업은 항상
번호 없는 최신본을 가리킨다.

```text
deliverable-02/                        # course delivery number
├── presentation.html                 # current working presentation
├── presentation-v1.0.html            # frozen baseline
└── presentation-v0.2-draft-script.md # historical matching script
```

HTML과 발표 원고는 항상 같은 version과 status를 가진 짝으로 보존한다. 의미 있는
내용 변경을 시작할 때 기존 짝을 덮어쓰지 않고 다음 버전의 두 파일을 함께 만든다.

| Version | Status | Intended evidence |
| --- | --- | --- |
| `v0.2-draft` | Preserved baseline | 발표 구조, vertical slice, architecture와 최초 20분 원고 |
| `v0.3-draft` | Current draft | Kamyar privacy 피드백과 D2→D4 로드맵 연결; setup·seed 증거는 여전히 pending |
| `v0.4-draft` | Planned integration revision | Jinja UI와 실제 browser flow |
| `v0.9-candidate` | Final rehearsal candidate | LAB SLOT 교체, 최신 테스트와 Git 증거 |
| `v1.0` | Verified English presentation | W2-10 persistence review와 Tony browser 검수 완료 |

파일 이름 규칙:

```text
presentation-v<version>-<status>.html
presentation-v<version>-<status>-ko.html
presentation-v<version>-<status>-script.md
```

- `draft`: 구성, 구현 또는 증거가 아직 변경 중이다.
- `candidate`: 발표 내용은 갖춰졌고 최종 검토와 리허설 중이다.
- `v1.0`: 실제 발표본으로 검증·확정됐다. 이 파일에는 status suffix를 생략한다.
- `-ko`: 같은 version과 status를 공유하는 한국어 언어본이며 새 revision을 뜻하지 않는다.
- 사소한 오탈자 수정은 현재 버전에 반영할 수 있지만, 발표 구조나 증거가 바뀌면
  다음 버전을 만든다.
- 새 버전의 HTML과 script를 만들 때 이 표에 핵심 변경 사항을 기록한다.

### Why v0.3 Was Created

Kamyar의 피드백은 발표의 장식 문구가 아니라 이후 구현 순서를 바꾸는 의미 있는
architecture requirement다. 따라서 v0.2를 덮어쓰지 않고 v0.3 짝을 새로 만들었다.

v0.3의 변화:

```text
D1 feedback: prove privacy meaningfully
→ D2: protected BorrowRequest access
→ D3: React + smallest Report entry
→ D4: role-protected Admin View
→ Final: verified privacy demonstration
```

- D2의 발표 중심은 여전히 하나의 BorrowRequest create/read vertical slice다.
- authorization boundary를 Kamyar 피드백에 대한 첫 기술적 응답으로 설명한다.
- Report와 Admin View가 동일한 backend pipeline을 재사용할 미래 모듈임을 표시한다.
- 성적과 gradebook 정보는 발표 파일과 이 README에 기록하지 않는다.
- 실제 setup, seed, login과 browser evidence는 검증 후 다음 revision에 반영한다.

### Placeholder Operating Rule — Historical Drafts

발표 HTML의 `LAB SLOT`은 이번 주 실험실 검증 위치다.

```text
LAB SLOT
→ 실제 명령·화면·테스트로 검증
→ 날짜와 결과 기록
→ placeholder를 verified evidence로 교체
```

- placeholder 자체를 Deliverable 증거로 취급하지 않는다.
- 하나의 검증 결과를 발표, milestone evidence와 실행 문서에 연결한다.
- v0.3에는 당시의 `LAB SLOT`을 보존한다. v1.0에서는 검수 완료된 사실만 표시하고
  placeholder를 남기지 않는다.

## Presentation Goal

Deliverable 2에서는 완성된 frontend를 과장해서 보여주지 않는다. BookLoop의 한 개
대여 요청이 browser에서 database까지 이동하고, 다시 안전하게 조회되는
**database-backed vertical slice**를 증명한다.

Easy-English core message:

> For Deliverable 2, I focused on one complete borrowing-request flow. The app
> validates the request, stores it in SQLite, protects private data, and reads
> the saved request only for authorized users.

발표 시간은 공식 수업 안내에 맞춰 조정한다. v1.0은 실제 검수된 Jinja UI, login,
persistence와 authorization 경계를 영어 발표 흐름으로 고정한다.

## Presentation Visual Vocabulary

발표 슬라이드와 발표 준비 문서에서는 같은 component, data entity와 client를 같은
아이콘으로 표시한다. 아이콘은 장식이 아니라 반복되는 architecture 용어의 약칭이다.
한 아이콘에는 한 의미만 부여하고, 새 슬라이드에서도 아래 의미를 재사용한다.

### Reusable Architecture Modules

| Icon | Module | Reused responsibility |
| --- | --- | --- |
| 🔐 | Authentication | 사용자의 로그인 상태와 신원을 확인한다. |
| 🛡️ | Authorization | 현재 사용자가 해당 작업을 수행할 수 있는지 확인한다. |
| ✅ | Validation | 입력값과 business rule이 유효한지 확인한다. |
| 🧩 | Shared Service | client와 route가 공유하는 application rule을 실행한다. |
| 🗄️ | Database Transaction | SQLAlchemy를 통해 데이터를 저장하거나 읽는다. |
| 📤 | API Response | 검증된 결과와 status code를 client에 반환한다. |

```text
🔐 Login → 🛡️ Authorize → ✅ Validate
→ 🧩 Shared Service → 🗄️ Database Transaction → 📤 Response
```

### Data Entities and Clients

| Icon | Meaning |
| --- | --- |
| 👤 | User |
| 📕 | BookListing |
| 📝 | BorrowRequest |
| 🐍 | Python/Jinja client |
| 🟨 | React client |

이 vocabulary는 특히 D2 vertical slice, authorization boundary, reusable CRUD
pipeline과 D2 → D3 client 전환을 설명할 때 동일하게 사용한다.

## Keep the Vertical Slice Narrow

BorrowRequest를 시연하기 위해 owner의 책 입력 UI와 borrower의 요청 UI를 동시에
완성할 필요는 없다. D2에서는 owner, borrower와 책 한 권을 재현 가능한 seed data로
준비하고, **BorrowRequest create/read만 UI에서 끝까지 증명**한다.

```text
Seeded owner + seeded borrower + seeded BookListing
                          ↓
                   borrower login
                          ↓
                  Request this book
                          ↓
             validation → SQLite INSERT
                          ↓
               same request ID 다시 조회
                          ↓
                 updated Jinja screen
```

### D2 UI Scope

| Include now | Do not build for this slice |
| --- | --- |
| borrower login | owner book-entry UI |
| seeded available book display | complete BookListing CRUD UI |
| `Request this book` form | approve/reject/return UI |
| pending request result | two simultaneous browser sessions |
| saved request read | complete lending cycle |
| visible validation error | frontend Admin View |

두 사용자 역할은 data와 authorization에 존재해야 하지만, 두 사용자의 전체 제품
화면을 모두 구현해야 한다는 뜻은 아니다. borrower 중심의 browser flow를 시연하고,
owner·unrelated user·guest의 read boundary는 자동 테스트로 보완한다. 시간이 허용되면
owner 계정으로 한 번 전환해 동일 request 조회만 추가로 보여준다.

## Demo Seed Data Strategy

Detailed implementation and verification checklist:

- [D2 Demo Seed Data Plan](../../planning/D2_DEMO_SEED_DATA_PLAN.md)

Seed data는 **터미널에서 실행하는 재현 가능한 Python/Flask 명령**으로 SQLite에
준비 데이터를 넣는 방식이 가장 적합하다. raw `sqlite3` SQL을 매번 손으로 입력하지
않고 SQLAlchemy model을 사용한다.

현재 backend에는 전용 seed 명령이 아직 없으므로 아래는 구현 목표다.

```text
terminal command
→ Flask app context
→ db.create_all()
→ SQLAlchemy models로 demo users/listing 생성
→ commit
```

권장 demo seed:

| Record | Purpose |
| --- | --- |
| Tony · borrower | 발표에서 로그인하고 요청을 생성할 사용자 |
| Mina · owner | `Almond` listing의 owner |
| Alex · unrelated user | `403 Forbidden` 자동 테스트용 |
| Almond · available listing | D2 요청 흐름의 시작점 |

다음 원칙을 지킨다.

- `BorrowRequest`는 seed하지 않는다. 발표 중 UI에서 실제로 생성해야 한다.
- password는 평문으로 저장하지 않고 실제 login과 같은 hash 규칙을 사용한다.
- 같은 명령을 다시 실행해도 중복 row가 계속 생기지 않도록 idempotent하게 만든다.
- 실제 개인정보나 개인 password는 사용하지 않는다.
- seed 명령, 예상 결과와 demo account 안내를 실행 문서에 기록한다.

발표 직전 준비 흐름:

```text
demo database 준비/reset
→ seed 명령 실행
→ owner, borrower, listing 확인
→ Flask server 실행
→ borrower가 browser에서 BorrowRequest 생성
```

Seed는 BookLoop의 출발 상태를 재현하기 위한 fixture다. 발표 핵심 증거인 요청 생성,
validation, persistence와 updated interface를 대신하지 않는다.

## Recommended Presentation Order

| Order | Section | What to Show | Current State |
| ---: | --- | --- | --- |
| 1 | Title and D2 goal | BookLoop, Deliverable 2, one vertical slice | Ready to draft |
| 2 | D1 → D2 transition | definition/prototype에서 backend/database 증명으로 이동 | Documented |
| 3 | Architecture | Jinja/API → service → SQLAlchemy → SQLite | Planned; service extraction pending |
| 4 | Data model | User, BookListing and BorrowRequest relationships | Implemented |
| 5 | Live flow | login → book → request → pending result → read again | Planned; UI/login pending |
| 6 | Authorization | borrower/owner 200, other user 403, guest 401 | API implemented and tested |
| 7 | Validation and privacy | invalid input rejected; private user fields excluded | API evidence available |
| 8 | Persistence | saved request remains readable from SQLite | Backend exists; restart proof pending |
| 9 | Test evidence | focused tests and full backend suite | 30 backend tests passed on Aug 2 |
| 10 | Next step | reuse service/API in D3 React, without rebuilding rules | Roadmap documented |

## Planned Live Demo Sequence

The final live demo should follow one story instead of jumping between files.

```text
1. Start the Flask application.
2. Log in as the borrower.
3. Open one available book listing.
4. Create a borrowing request.
5. Show the saved request with status: pending.
6. Refresh or reopen the request to prove database persistence.
7. Show that the borrower and listing owner can read it.
8. Show that another user receives 403 and a guest receives 401.
9. Run the focused tests, then show the full backend test result.
```

Steps 2–6 are the target product demo and remain pending until the real login flow,
shared service and Python/Jinja UI are completed and verified in Tony's browser.

## Minimal Slide Structure

### 1. Title

- **BookLoop — Deliverable 2: Backend and Database**
- Subtitle: *A private, database-backed borrowing request flow*

### 2. What Changed Since Deliverable 1?

- D1: problem, users, workflow and prototype
- D2: running backend, relational database, validation, authorization and persistence

### 3. One Vertical Slice

```text
👤 Borrower action
→ 🐍 Python/Jinja screen
→ 🧩 BorrowRequest service
→ 🗄️ SQLAlchemy / SQLite
→ 📤 protected result
```

### 4. Relational Data

- 👤 `User` owns a 📕 `BookListing`.
- Another 👤 `User` creates a 📝 `BorrowRequest`.
- The request connects borrower and listing without exposing private fields.

### 5. Live Product Demo

- Create one request.
- Read the same saved request.
- Show its `pending` state.

### 6. Safety Boundary

- borrower: `200`
- listing owner: `200`
- unrelated user: `403`
- unauthenticated user: `401`
- missing request: `404`

### 7. Validation, Persistence and Tests

- Explain where validation happens.
- Restart/reopen and read the same database row.
- Show focused tests and the full backend suite.

### 8. What Comes Next?

- Reuse the shared service pattern for later CRUD.
- Connect React to the verified JSON API in Deliverable 3.
- Do not duplicate backend business rules in React.

## Evidence Checklist Before Presentation

- [x] Flask application starts.
- [x] SQLAlchemy models and relationships exist.
- [x] BorrowRequest create API exists.
- [x] Protected BorrowRequest read API exists.
- [x] authorization and privacy response tests pass.
- [x] full backend suite passed with 30 tests on 2026-08-02.
- [ ] actual register/login/logout browser flow works.
- [ ] BorrowRequest create/read rules use one shared service.
- [ ] Python/Jinja product screen works in Tony's browser.
- [ ] request persists across a server restart and is shown again.
- [ ] final data-flow diagram and run commands are captured.
- [ ] meaningful D2 Git progression is ready to show.
- [ ] Tony confirms the final demo order.

## Demo Failure Fallback

Live browser evidence remains the primary demo. Before class, also keep:

- one successful create/read screenshot;
- one authorization error screenshot;
- the exact run commands;
- the latest focused and full test output.

These are recovery evidence only, not a substitute for completing the live product flow.

## Source Roadmap

- [D2 Python/Jinja → D3 React Roadmap](../../planning/D2_PYTHON_JINJA_TO_D3_REACT_ROADMAP.md)
- [D2 Demo Seed Data Plan](../../planning/D2_DEMO_SEED_DATA_PLAN.md)

## Promotion Rule

```text
private draft
→ implementation completed
→ Tony browser verification
→ teacher-facing presentation draft
→ Tony confirmation
→ scoped commit and push
```
