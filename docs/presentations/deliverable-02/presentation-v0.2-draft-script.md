# BookLoop Deliverable 2 — 20-Minute Presentation Script

> Based on: `presentation-v0.2-draft.html`
> Presenter: Tony Yu
> Target length: 20 minutes
> Status: rehearsal draft — update all `LAB SLOT` evidence after browser verification

## How to Use This Script

- **English script**: 실제 발표에서 말할 쉬운 영어 원고
- **한국어 진행 메모**: 클릭, 화면 지시와 강조점
- `Pending`으로 표시된 기능은 실제 검증 전까지 완료된 것처럼 말하지 않는다.
- 라이브 데모가 준비되면 Slide 07의 `Planned-demo version`을 `Verified live-demo version`으로 교체한다.

## Time Plan

| Time | Section | Duration |
| --- | --- | ---: |
| 00:00–01:00 | Title and goal | 1 min |
| 01:00–03:00 | 01 · D1 → D2 | 2 min |
| 03:00–04:30 | 02 · Setup | 1.5 min |
| 04:30–06:00 | 03 · Seed data | 1.5 min |
| 06:00–08:30 | 04 · Vertical slice | 2.5 min |
| 08:30–10:30 | 05 · Architecture | 2 min |
| 10:30–12:00 | 06 · Relational database | 1.5 min |
| 12:00–14:30 | 07 · Product demo | 2.5 min |
| 14:30–16:30 | 08 · Validation and authorization | 2 min |
| 16:30–18:00 | 09 · Verification and Git evidence | 1.5 min |
| 18:00–19:00 | 10 · Reusable architecture | 1 min |
| 19:00–20:00 | 11 · Next checkpoint and close | 1 min |

---

## 00:00–01:00 — Title and Goal

### English script

Hello everyone. My name is Tony Yu, and this is BookLoop Deliverable 2.

BookLoop is a privacy-focused book-sharing platform for the Korean community. In
Deliverable 1, I introduced the problem, the users, and the basic product workflow.
For Deliverable 2, I moved from design into a working backend and relational
database.

My goal is not to show many disconnected screens. My goal is to prove one complete
borrowing-request flow. A user requests a book, Flask validates the request,
SQLAlchemy saves it in SQLite, and only authorized users can read it again.

This is the backend vertical slice that the future interface will use.

### 한국어 진행 메모

- 제목과 `Backend vertical slice` 배지를 가리킨다.
- 핵심 문장: **one complete borrowing-request flow**.
- 아직 private draft이므로 완성된 최종 발표라고 말하지 않는다.

---

## 01:00–03:00 — 01 · From D1 to D2

### English script

Deliverable 1 answered the question, “What should BookLoop do?” I defined the
target users, the privacy problem, the data model, the API direction, and the
interface concept.

Deliverable 2 answers a different question: “Can one important workflow really
move through the system?”

The project progression is shown here. First, I defined the need. Then I designed
the workflow. Now I am building the backend, connecting the database, and verifying
one vertical slice.

I selected the borrowing request because it connects the main parts of BookLoop.
It needs a borrower, a book listing, an owner, validation rules, database
persistence, and privacy rules. Because of this, one small request can prove much
more than a collection of static pages.

For Deliverable 2, I am using a Python and Jinja client as the easiest verification
interface. For Deliverable 3, React can use the same backend rules through the JSON
API. The client will change, but the business rules should not be rebuilt.

So my main design decision is simple: one connected workflow is more valuable than
many unfinished CRUD screens.

### 한국어 진행 메모

- D1 카드에서 D2 카드로 손이나 포인터를 이동한다.
- `🐍 Python/Jinja now → Shared backend rules → 🟨 React next`를 천천히 읽는다.
- CRUD 전체를 포기한 것이 아니라, 먼저 재사용 가능한 기반을 검증한다는 점을 강조한다.

---

## 03:00–04:30 — 02 · Reproducible Setup

### English script

A backend demonstration must be reproducible. It should not work only on my
computer because of a hidden manual step.

This slide identifies three pieces of setup evidence. First, I need one documented
command that starts the Flask application. Second, I need to explain the environment
configuration and keep secrets outside the source code. Third, I need to show how
SQLite is created and how the expected tables are confirmed.

These cards are still lab slots in this draft. That is intentional. I will replace
them only with commands and evidence that I have actually verified. A placeholder
is a work location, not proof of completion.

For the final demonstration, another developer should be able to follow the same
startup instructions and reach the same database state.

### 한국어 진행 메모

- 세 개의 점선 카드를 차례로 가리킨다: startup, environment, database.
- 최종 버전에서는 실제 명령을 짧게 실행하거나 캡처를 보여준다.
- “placeholder is not evidence”를 분명하게 말한다.

---

## 04:30–06:00 — 03 · Reproducible Demo Starting Data

### English script

To make the demo repeatable, I need safe starting data.

Tony is the borrower. Mina owns the book listing. Alex is an unrelated user for
the authorization test. Almond is the available book listing.

The seed command will run through the Flask application context and SQLAlchemy
models, and then commit the records to SQLite. It should be idempotent. This means
that running it a second time must not create duplicate users or duplicate books.

There is one important boundary: I seed the starting point, but I do not seed the
result. The users and the Almond listing may exist before the demo, but the
BorrowRequest must not exist yet.

Tony must create that request through the real Jinja form. Otherwise, I would not
be proving form submission, server validation, database insertion, or the updated
screen.

The idempotent seed command is still planned in this draft and will be replaced
with verified evidence before the final presentation.

### 한국어 진행 메모

- 인물 순서를 항상 `Tony → Mina → Alex`, 마지막에 `Almond`로 유지한다.
- 핵심 대비: **seed starting data, never seed the BorrowRequest**.
- 아직 seed 명령이 구현되지 않았다면 명령이 존재하는 것처럼 말하지 않는다.

---

## 06:00–08:30 — 04 · Selected Vertical Slice

### English script

This is the selected vertical slice in detail.

Tony logs in as the borrower. He opens Mina’s Almond listing and submits a
borrowing request. The browser sends a POST request to Flask. Flask checks Tony,
the listing, and the request data. If the data is valid, SQLAlchemy inserts one
BorrowRequest into SQLite.

The application then reads the same request again. Jinja shows the saved status as
pending. This is important because the screen is not displaying temporary browser
data. It is displaying a record that came back from the database.

The table shows the same story across three technical areas. In the User and Jinja
column, Tony logs in, requests Almond, opens the result, and sees Pending. In the
Flask column, the server authenticates Tony, validates the request, checks access,
and returns the response. In the SQLite column, the application finds the user,
inserts the BorrowRequest, selects the saved row, and keeps the data persisted.

The backend foundation is already verified in this draft: create and read APIs,
database relationships, validation, privacy-safe serialization, and authorization
tests. The browser product demo is still being prepared. The remaining integration
is the real login flow, the shared service, and the Python/Jinja request screen.

This distinction is important. I am showing what is verified, and I am also making
the unfinished integration visible.

### 한국어 진행 메모

- 위 배지 흐름을 왼쪽에서 오른쪽으로 설명한 뒤 아래 3열 표로 내려간다.
- `POST → INSERT → GET → Pending`을 핵심 기술 흐름으로 강조한다.
- verified backend와 pending product demo 카드를 명확히 구분한다.

---

## 08:30–10:30 — 05 · Data Flow and Service Boundary

### English script

This architecture is designed for two clients without duplicating the backend
rules.

In Deliverable 2, the Python and Jinja interface calls a Flask page route. In
Deliverable 3, the React interface will call the Flask JSON API. Both paths should
converge on one shared BorrowRequest service, the same SQLAlchemy models, and the
same SQLite database.

Each layer has a focused role. The route receives HTTP input and chooses the
response format. The service owns the application rules, including validation and
authorization coordination. The model defines relationships and persists valid
data.

Currently, the validated backend behavior exists, but some validation still runs
inside the Flask API route. The target is to extract those create and read rules
into one shared service. Then Jinja and React can use the same logic without
copying it.

The orange items are planned integration work. I will change them to verified only
after the actual call path and browser behavior are tested.

### 한국어 진행 메모

- 두 client가 하나의 service로 모이는 지점을 가리킨다.
- `Route ≠ Service ≠ Model` 역할을 짧고 분명하게 구분한다.
- service extraction이 아직 pending이라는 사실을 숨기지 않는다.

---

## 10:30–12:00 — 06 · Relational Database

### English script

The relational model has three main models: User, BookListing, and BorrowRequest.

One User can own many BookListings. A different User, acting as the borrower, can
create many BorrowRequests. Each BorrowRequest connects one borrower to one
BookListing. One listing can receive multiple requests over time.

This structure records three important facts: who owns the book, who requested it,
and which listing was requested. The relationships also support authorization.
When somebody reads a request, the application can compare the current user with
the borrower ID and the listing owner ID.

The API response does not need to expose private user fields such as an email or
password data. The relationship IDs and safe public fields are enough for this
workflow.

### 한국어 진행 메모

- SVG에서 `User → BookListing`, `User → BorrowRequest`,
  `BookListing → BorrowRequest` 관계를 순서대로 가리킨다.
- 관계형 모델이 단순 저장뿐 아니라 authorization 판단도 지원한다고 설명한다.

---

## 12:00–14:30 — 07 · Planned Product Demo

### English script — planned-demo version

This slide shows the exact product demo that I am preparing.

I will log in as Tony, open the Almond listing, and select “Request this book.” The
application will create a new BorrowRequest with the status pending. I will then
refresh or reopen the result and show the same request again.

The two areas on the screen represent two different database models. The left side
is the BookListing for Almond. The right side is the newly created BorrowRequest.
The successful message is useful, but the stronger evidence is that the same
request ID and status return after another database read.

The three evidence slots describe what I must prove. First, the form creates one
new BorrowRequest. Second, the application reads that same request. Third, the
record remains after a refresh or server restart.

This screen is still a planned interface in the current draft. I am not presenting
the mockup as a finished browser implementation.

### English script — verified live-demo replacement

I am now logged in as Tony. This is Mina’s Almond listing. I will click “Request
this book.” The server validates the form and creates this BorrowRequest with the
status pending. Notice the request ID.

Now I will refresh or reopen the request. The same ID and pending status still
appear. This proves that the screen read the saved record from SQLite instead of
keeping temporary data only in the browser.

### 한국어 진행 메모

- 현재는 위의 `planned-demo version`을 사용한다.
- 실제 브라우저 검증 후에는 `verified live-demo replacement`로 교체한다.
- 데모 중에는 설명을 줄이고 클릭과 결과가 보이도록 잠시 멈춘다.
- 실패 대비용 캡처는 보조 증거일 뿐, 성공한 라이브 흐름을 대체하지 않는다.

---

## 14:30–16:30 — 08 · Validation and Authorization Boundary

### English script

Saving data is not enough. BookLoop must also protect who can read it.

Tony created Request number 3, so Tony is allowed to read it and receives status
200. Mina owns the Almond listing, so she is also allowed to read the request and
receives 200.

Alex is an unrelated authenticated user. He is neither the borrower nor the book
owner, so he receives 403 Forbidden. A logged-out guest has no authenticated
session, so the result is 401 Login Required. If Tony requests an ID that does not
exist, the result is 404 Not Found.

These status codes represent different situations. A 401 means, “Please log in.” A
403 means, “We know who you are, but you are not allowed to access this record.” A
404 means the requested record does not exist.

I also plan to show one visible validation failure. For example, Tony can submit an
invalid or duplicate request. The server should explain the problem and must not
insert an extra BorrowRequest.

### 한국어 진행 메모

- 카드 순서 `Tony 200 → Mina 200 → Alex 403 → Guest 401`를 유지한다.
- 401과 403의 차이를 또렷하게 말한다. 이 부분은 좋은 질의응답 포인트다.
- validation failure UI는 아직 LAB SLOT이면 계획이라고 표현한다.

---

## 16:30–18:00 — 09 · Verification and Git Evidence

### English script

I tested the backend boundary before connecting the product interface to it.

According to the current verified record from August 2, the Flask application
starts, the models and relationships work, the BorrowRequest create and read APIs
exist, authorization responses are tested, private fields are excluded, and the
full backend suite passes 30 tests.

There are still browser-level gates before the final Deliverable 2 demo. I need to
verify login and logout in the browser, connect Jinja through the shared service,
reopen the saved data after a restart, capture the final run commands, and confirm
the complete flow in my browser.

The final slide will also include concise test output, meaningful Git progression,
and reproducible run documentation. I will add those items as evidence, not as
decoration.

### 한국어 진행 메모

- 왼쪽 verified 카드부터 말하고 오른쪽 pending 카드로 이동한다.
- `30 tests passed`는 현재 HTML에 기록된 8월 2일 검증 결과라는 범위를 유지한다.
- 최종 발표 전에 최신 결과로 다시 확인하고 날짜를 갱신한다.

---

## 18:00–19:00 — 10 · Reusable Architecture

### English script

This first workflow creates a reusable production line.

The icons represent reusable modules: authentication, authorization, validation, a
shared service, a database transaction, and a safe response.

BookListing CRUD can reuse this pipeline with its own field and ownership rules.
BorrowRequest updates can reuse it while adding valid status transitions. React can
consume the verified JSON response without rebuilding the backend logic.

Later CRUD work becomes easier, but it is not automatic. Delete history, ownership,
roles, and status changes still require feature-specific rules and tests.

### 한국어 진행 메모

- 아이콘을 한 번씩 짚는다:
  `🔐 → 🛡️ → ✅ → 🧩 → 🗄️ → 📤`.
- “reuse the pipeline, add feature-specific rules”가 핵심이다.

---

## 19:00–20:00 — 11 · Next Checkpoint and Closing

### English script

My next checkpoint is to finish the Deliverable 2 browser flow.

I will connect the real login session, extract the shared BorrowRequest service,
connect the Python and Jinja product screen, and verify persistence through the
complete browser workflow.

After that backend gate passes, Deliverable 3 can connect React to the same JSON
API. React will reuse the verified models, status codes, validation rules, and test
cases.

The main lesson from this deliverable is: build the rule once in Python, verify it
through Jinja now, and reuse it from React next.

Thank you. I am ready for your questions.

### 한국어 진행 메모

- D2 남은 네 단계를 짧게 읽고 D3 카드로 이동한다.
- 마지막 문장은 슬라이드 callout과 동일하게 마무리한다.
- 질문을 받기 전에 1초 멈추고 청중을 본다.

---

## Short Q&A Preparation

### Why did you use seed data?

> Seed data gives me a safe and reproducible starting point. It avoids building an
> unrelated owner-entry screen for this narrow D2 slice. The BorrowRequest itself
> is never seeded; it must be created during the demo.

### Why can both Tony and Mina read the request?

> Tony is the borrower who created it. Mina owns the requested book listing. Both
> users are part of the transaction, so both are authorized.

### What is the difference between 401 and 403?

> A 401 response means the user is not logged in. A 403 response means the user is
> logged in but does not have permission for that request.

### Why use Jinja before React?

> Jinja is a smaller verification client for D2. It lets me test the complete Flask
> and database flow first. React can then reuse the verified JSON API in D3.

### Why extract a shared service?

> The service keeps business rules outside the response format. Jinja routes and
> JSON API routes can call the same create, read, validation, and authorization
> logic.

### Is the project finished?

> No. The backend foundation is verified, but the final browser login, shared
> service integration, Jinja product screen, restart persistence evidence, and
> final presentation evidence are still being completed.

## Final Rehearsal Gate

- [ ] Replace every visible `LAB SLOT` used in the final presentation.
- [ ] Update the setup, seed and run commands with verified output.
- [ ] Choose either the planned-demo script or verified live-demo script.
- [ ] Reconfirm the current backend test count and verification date.
- [ ] Test Tony, Mina, Alex and Guest authorization results.
- [ ] Confirm that no private user fields appear in the response.
- [ ] Rehearse once with a timer and record the actual duration.
- [ ] Keep 1–2 minutes available for a slow live demo or instructor interruption.
