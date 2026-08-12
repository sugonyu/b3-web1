# BookLoop Local User Manual

> 개인 로컬 데모와 브라우저 검수용 사용자 매뉴얼 · v0.1 · 2026-08-06

이 문서는 BookLoop를 개발한 뒤 “어떻게 실행하고 어떤 사용자로 무엇을 확인하지?”를
빠르게 복기하기 위한 Tony 개인용 안내서다. API 설계나 코드 구조 설명보다 실제
브라우저 사용 순서에 집중한다.

실제 사용자의 개인정보 보호와 안전한 대면 교환 방법은
[`BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md`](BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md)에서
별도로 다룬다.

## 1. 현재 범위

현재 Python/Jinja MVP에서 다음 기능을 사용할 수 있다.

- 데모 사용자 로그인·로그아웃
- 실제 SQLite 책 목록 확인
- 책 대여 요청 생성
- 내가 보낸 요청 확인
- owner 결정 전 pending 요청 취소
- 내 책에 들어온 요청 확인
- 책 소유자의 pending 요청 승인·거절
- borrower와 owner만 Request detail 접근
- 개발 전용 View-as-user로 세 사용자 관점 전환
- DB Inspector에서 저장된 row 확인

React client와 Admin View는 현재 사용자 매뉴얼 범위가 아니다. 신고 제출자는
`My reports`에서 자신이 보낸 신고의 현재 상태를 확인할 수 있다.

## 2. 서버 실행

터미널에서 기존 가상환경을 먼저 종료한 뒤 BookLoop용 가상환경을 활성화하고
Flask 개발 서버를 실행한다.

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
deact
webact
python3 run.py
```

실제 실행 순서는 다음과 같다.

```text
(.venv) sugonyu@penguin:~/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend (main ✎ 🚀4)$ deact
sugonyu@penguin:~/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend (main ✎ 🚀4)$ webact
(.venv) sugonyu@penguin:~/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend (main ✎ 🚀4)$ python3 run.py
 * Serving Flask app 'bookloop'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://<현재 LAN 또는 Tailscale IP>:5000
Press CTRL+C to quit
```

`webact`는 BookLoop 백엔드의 `.venv`를 활성화하는 개인 셸 명령이다.
서버를 종료할 때는 실행 중인 터미널에서 `Ctrl+C`를 누른다. 실제 접속 로그에는
브라우저 요청마다 `GET /`와 정적 파일 요청이 표시될 수 있다.

브라우저:

```text
http://127.0.0.1:5000/
```

`.env`에서 개발 도구를 사용할 때:

```text
ENABLE_DEV_DB_INSPECTOR=true
ENABLE_DEV_USER_SWITCHER=true
```

설정 변경 후에는 Flask 서버를 재시작한다.

## 3. 데모 사용자

| 사용자 | 아이콘 | 주요 관점 | 공통 로컬 암호 |
| --- | --- | --- | --- |
| Tony | 👨 | admin · Homer 책 두 권 owner | `1111` |
| Mina | 👩 | member · Han Kang 책 두 권 owner | `1111` |
| Alex | 🕵️ | unrelated user · empty state와 403 확인 | `1111` |

이 공통 암호는 로컬 수업 데모 편의를 위한 값이다. 실제 서비스 암호 정책이 아니다.

## 4. 데모 책

| 책 | 아이콘 | 소유자 |
| --- | --- | --- |
| The Odyssey | 🌊 | Tony 👨 |
| The Iliad | 🛡️ | Tony 👨 |
| The Vegetarian | 🌱 | Mina 👩 |
| Human Acts | 🕯️ | Mina 👩 |

Tony로 로그인하면 Homer의 두 책은 `Your book`으로 표시되고 Mina의 두 책을
요청할 수 있다.

## 5. 기본 요청 흐름

```text
👨 Tony
→ Books
→ 🌱 The Vegetarian · Request
→ Request #ID · Pending
→ 🙋 Sent requests에서 같은 #ID 확인

👩 Mina
→ 📬 Received requests
→ 같은 #ID 확인
→ Review & decide
→ privacy-safe Decision Context 확인
→ ✅ Approve 또는 ❌ Reject
→ #ID를 눌러 Request detail 확인

👨 Tony
→ 🙋 Sent requests
→ 같은 #ID의 Approved 또는 Rejected 결과 확인

신고를 제출한 뒤:

👨 Tony
→ 🚩 My reports
→ 본인이 제출한 Report의 Open / Under review / Resolved / Dismissed 상태 확인

또는 owner 결정 전:

👨 Tony
→ Pending request
→ ↩ Cancel request
→ Cancelled

🕵️ Alex
→ 같은 Request URL 접근
→ 403 Access denied 확인
```

Sent와 Received 테이블에는 필요한 정보가 이미 표시되므로 별도 `View` 열이 없다.
`Request #ID` 자체가 상세 페이지 링크다.

Mina에게만 pending request의 `Approve`와 `Reject` 버튼이 보인다. 승인하면 request가
`Approved`가 되고 해당 책은 unavailable 상태가 된다. 거절하면 request는 `Rejected`가
되며 책은 계속 available 상태를 유지한다. 이미 결정된 요청에서는 버튼이 사라지고
`Decision complete`가 표시된다.

결정 버튼은 Received 목록에 직접 노출되지 않는다. Mina는 `Review & decide`로 상세
화면을 열고 request 시간, 가입 시점, 완료 교환 횟수와 활성 요청 수를 먼저 확인한다.
email, 정확한 주소와 다른 책의 활동은 보여주지 않는다.

Tony에게는 본인의 request가 `Pending`일 때만 `Cancel request`가 보인다. Mina가 이미
승인하거나 거절한 뒤에는 취소할 수 없다. 취소된 요청은 history에 `Cancelled`로
남고 책은 available 상태를 유지한다.

### Approved Contact Exchange

내장 메시징 대신 request가 `Approved`가 된 뒤 두 당사자의 상세 화면에서만 상대방
이메일을 공개한다.

```text
Pending / Rejected / Cancelled / Returned
→ contact email 숨김

Approved + Tony
→ Mina의 email만 표시

Approved + Mina
→ Tony의 email만 표시

Alex 또는 비로그인 사용자
→ 기존 403 / login 경계 적용
```

이메일은 collection JSON API에 추가하지 않는다. 본인은 자기 profile에서 확인할 수
있고, 승인된 두 당사자는 상대 profile과 `Request detail`에서 상대 email을 확인한다.
password hash는 모든 화면과 응답에서 계속 제외한다.

### Privacy-safe User Profile

로그인 사용자는 Books, Sent, Received와 Request detail의 사용자 이름을 눌러
`/users/<user_id>` 읽기 전용 profile을 열 수 있다.

표시 정보:

- username과 demo icon
- general area
- member since
- completed exchanges
- 현재 available 상태인 소유 책

숨김 정보:

- 권한 없는 다른 사용자의 email과 모든 password hash
- 정확한 주소
- unavailable/private listing
- 개별 request history

본인에게는 자기 email을 표시한다. 다른 사용자의 email은 두 사람 사이에 현재
`Approved` request가 있을 때만 profile과 Request detail에서 표시한다.

#### Email visibility policy

| Request status / viewer | Profile | Request detail |
| --- | --- | --- |
| 본인이 자기 profile 확인 | 자기 email 공개 | 해당 없음 |
| `Pending` 당사자 | 숨김 | 숨김 |
| `Approved` borrower | book owner email 공개 | book owner email 공개 |
| `Approved` book owner | borrower email 공개 | borrower email 공개 |
| `Rejected`, `Cancelled`, `Returned` 당사자 | 숨김 | 숨김 |
| unrelated user | 숨김 | `403` |
| logged-out visitor | login 필요 | login 필요 |

현재 MVP에는 모든 회원에게 profile email을 공개하는 설정을 두지 않는다. 본인과
`Approved` 거래 상대만 허용한다.

### Status 색상 배지

요청 상세 화면과 두 요청 목록은 상태를 다음 색상으로 구분한다.

| Status | 색상 | 의미 |
| --- | --- | --- |
| `Pending` | Amber | 책 주인의 결정을 기다리는 요청 |
| `Approved` | Green | 책 주인이 승인한 요청 |
| `Rejected` | Red | 책 주인이 거절한 요청 |
| `Cancelled` | Gray | borrower가 결정 전에 취소한 요청 |
| `Returned` | Blue | 대여 후 반납이 완료된 요청 |

색상은 빠른 식별을 돕는 보조 정보다. 접근성과 정확성을 위해 각 배지에는
`Pending`, `Approved` 같은 상태 텍스트도 항상 함께 표시한다.

## 6. View-as-user 개발 도구

### 목적

Discord의 `View Server As Role`처럼 로그인 폼을 반복하지 않고 seed 사용자 관점을
빠르게 바꾼다.

```text
👨 Tony  → 보낸 요청과 소유 책
👩 Mina  → 받은 요청과 소유 책
🕵️ Alex → 관계없는 사용자 권한
```

이 기능은 실제 제품의 impersonation 또는 Admin 기능이 아니다.

### 현재 구현

`DEBUG=true`와 `ENABLE_DEV_USER_SWITCHER=true`가 모두 충족되면 제품 화면에 다음
패널이 표시된다.

```text
DEV · Viewing as tony 👨
[👨 Tony] [👩 Mina] [🕵️ Alex]
```

사용자 버튼을 누르면 Flask-Login session이 해당 seed 사용자로 바뀌고 Books
화면으로 돌아간다.

### 숨김 패널과 footer 토글 · 구현 완료

DEV 패널이 제품 navigation과 본문 흐름을 방해하지 않도록 다음 interaction으로
개선했다.

```text
[DEV · Viewing as tony 👨]  ← 제목 위, 기본 감춤

BookLoop
제품 내용
────────────────────────
🧪 Test Hub · 🐍 Jinja · ↻ · ◦
                            ↑ DEV 패널 토글
```

동작:

1. DEV 패널을 페이지 제목 위로 이동한다.
2. 기본 상태에서는 패널을 숨긴다.
3. footer의 Refresh 오른쪽에 작은 `◦` 버튼을 둔다.
4. `◦`를 누르면 현재 `DEV · Viewing as ...`와 세 사용자 버튼을 표시한다.
5. 다시 누르면 감춘다.
6. `localStorage`에 마지막 표시 상태를 기억한다.
7. 시각적으로 작은 버튼이어도 `aria-label`을 제공한다.

숨김 버튼은 보안 기능이 아니다. 실제 접근 경계는 계속 다음 조건이 담당한다.

```text
DEBUG
+ ENABLE_DEV_USER_SWITCHER
+ Tony/Mina/Alex allowlist
```

## 7. Footer 개발 링크

현재 Books 화면 하단에서 다음 경로를 사용할 수 있다.

- `🧪 Test Hub` — client, API와 개발 도구 링크 비교
- `🐍 Jinja Reference` — Python/Jinja 학습 참고 화면
- `↻` — 현재 Books 화면 다시 불러오기
- `◦` — DEV 사용자 전환 패널 표시·감춤

`◦`는 `DEBUG + ENABLE_DEV_USER_SWITCHER` 조건을 만족할 때만 표시된다.

## 8. 데모 요청 초기화

기존 demo BorrowRequest만 지우고 User와 BookListing은 보존한다.

```bash
python3 bl_cli.py reset-demo-requests
```

초기 상태를 다시 준비할 때:

```bash
python3 bl_cli.py seed-demo
```

## 9. SQLite 확인

브라우저 DB Inspector:

```text
http://127.0.0.1:5000/dev/db/
```

자주 보는 순서:

```text
Borrow Requests
→ Book Listings
→ Users
```

Inspector는 read-only 개발 도구다. 제품 Admin View가 아니다.

## 10. 관련 로컬 경로

| 목적 | URL |
| --- | --- |
| BookLoop 제품 | `http://127.0.0.1:5000/` |
| Sent requests | `http://127.0.0.1:5000/requests/` |
| Received requests | `http://127.0.0.1:5000/listing-requests/` |
| My reports | `http://127.0.0.1:5000/reports/` |
| Test Hub | `http://127.0.0.1:5000/test/` |
| Flask Vanilla | `http://127.0.0.1:5000/vanilla/` |
| Health API | `http://127.0.0.1:5000/api/health` |
| DB Inspector | `http://127.0.0.1:5000/dev/db/` |

## 11. 빠른 검수 체크리스트

- [ ] Flask 서버가 실행된다.
- [ ] Tony·Mina·Alex 전환이 된다.
- [ ] 🌊 The Odyssey와 🛡️ The Iliad가 표시된다.
- [ ] Tony가 The Odyssey를 요청할 수 있다.
- [ ] 같은 Request ID가 Tony Sent와 Mina Received에 표시된다.
- [ ] Alex가 같은 상세 URL에서 403을 받는다.
- [ ] mobile 폭에서 Books·Sent·Received 테이블이 row card로 바뀐다.
- [ ] DB Inspector에서 같은 Request row가 보인다.
- [ ] 사용자 이름에서 privacy-safe profile을 열 수 있다.
- [ ] profile에는 email이 없고 Approved Request detail에만 상대 email이 보인다.

## Related Documents

- [Documentation Index](BOOKLOOP_DOCUMENTATION_INDEX.md)
- [Formal User Manual](BOOKLOOP_USER_MANUAL.md)
- [Admin & Operator Manual](BOOKLOOP_ADMIN_OPERATOR_MANUAL.md)
- [Safe Use & Privacy Guide](BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md)
- [W3-07 API Handoff 복기 노트](W3_07_API_HANDOFF_STUDY_NOTE.md)
- [Core JSON API Contract](API_CONTRACT.md)
- [BookLoop Flask Package Code Map](bookloop/README.md)
- [Dev User Switcher](bookloop/devtools/user_switcher/README.md)
- [Test Hub](bookloop/devtools/test_hub/README.md)
- [Jinja → React parity replay plan](../frontend/react/JINJA_PARITY_REPLAY_PLAN.md)
