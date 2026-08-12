# BookLoop Jinja → React Parity Replay Plan

## 목적

Python/Jinja에서 검증한 제품 기능을 React에서 임의로 재설계하지 않고, 구현된 순서와
privacy acceptance criteria를 그대로 재현한다. React는 SQLite에 직접 접근하지 않고
Flask JSON API와 공통 service 경계를 사용한다.

```text
🐍 Jinja route → shared service → SQLAlchemy → SQLite
⚛️ React fetch → Flask JSON API → shared service → SQLAlchemy → SQLite
```

## 2026-08-06 구현 순서

### 1. Status 의미와 시각적 구분

- `Pending`, `Approved`, `Rejected`, `Cancelled`, `Returned` 텍스트 유지
- amber, green, red, gray, blue 색상 배지 적용
- 색상만으로 상태를 전달하지 않음
- React 재현: 공통 `StatusBadge` component와 status-to-class mapping

### 2. DB Inspector 검증 레전드

- 제품 UI와 동일한 status 의미를 read-only Inspector에서 확인
- React 범위가 아니라 backend debugging evidence로 계속 유지

### 3. Approved Contact Exchange

- 승인 전에는 email 비공개
- 승인 후 borrower와 listing owner에게만 상대 email 공개
- unrelated user는 `403`, 비로그인은 `401` 또는 login redirect
- 본인은 자기 profile email을 확인할 수 있음
- approved 당사자는 상대 profile과 request detail에서 상대 email을 확인
- unrelated profile과 collection JSON에는 email을 포함하지 않음
- React 재현 전에 approved-contact 전용 API response contract 결정 필요
- 권한 없는 profile에는 email 대신 approved-only 공개 정책 안내를 표시

### 4. 역할 중심 request navigation

- `🙋 Sent requests` = 내가 borrower로 만든 요청
- `📬 Received requests` = 내가 owner인 책에 들어온 요청
- React 재현: 동일 문구, 아이콘과 count 유지

### 5. Privacy-safe User Profile

- route: `GET /users/<user_id>`
- 표시: username, general area, member since, completed exchanges, available books
- 조건부 표시: own email 또는 approved 상대 email
- 제외: unauthorized email, password hash, exact address, unavailable listing, request history
- 안내: 다른 사람의 email은 approved request의 두 당사자에게만 공개됨
- React 재현 전에 privacy-safe profile JSON endpoint를 별도 설계

### 6. W3-14 Two-step Return Confirmation

- 짧은 번호는 추적용 ID이며 기능 계약 자체가 아님
- 상태: `approved → return_pending → returned`
- borrower가 반납 확인을 시작하고 listing owner가 수령을 확정
- React는 `PATCH /api/requests/<id>`로 Jinja와 같은 service를 사용
- 상세 계약: [`W3_14_TWO_STEP_RETURN_CONFIRMATION.md`](../../../docs/planning/W3_14_TWO_STEP_RETURN_CONFIRMATION.md)

## React 구현 체크포인트

```text
[ ] API contract 먼저 작성
[ ] fetch service 작성
[ ] StatusBadge component
[ ] Sent / Received navigation
[ ] Approved contact conditional UI
[ ] UserProfile page
[ ] 401 / 403 / 404 / private-field tests
[ ] Jinja와 React의 같은 seed data 결과 비교
```

## 완료 기준

React 화면이 예쁘게 보이는 것만으로 parity 완료로 판단하지 않는다. 동일 사용자와 동일
BorrowRequest ID에서 Jinja와 React가 같은 status, count, 권한 결과와 private-field 제외를
보여줄 때 완료로 기록한다.

사용자 안전 안내도 기능 parity의 일부다. React 구현은
[`BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md`](../../backend/BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md)의
공개 범위, 승인 후 연락과 실제 교환 안전 원칙을 바꾸지 않는다.
