# BookLoop User Manual

> 정식 사용자 매뉴얼 · v1.0-draft · 2026-08-06

## 1. 문서 범위

이 문서는 BookLoop에서 책을 등록한 owner와 책을 빌리려는 borrower가 현재
Python/Jinja MVP를 사용하는 방법을 설명한다. 서버 실행, seed data와 DB Inspector는
사용자 기능이 아니므로 개발용 `BOOKLOOP_LOCAL_USER_MANUAL.md`에서 다룬다.

현재 MVP에는 Report, Block, 신원 verification과 Admin moderation 화면이 없다.

## 2. 로그인과 내 정보

로그인 후 Books 화면에서 다음 항목을 사용할 수 있다.

- `👤 View my profile`
- `🙋 Sent requests`
- `📬 Received requests`
- `Log out`

내 Profile에서는 username, general area, member since, completed exchanges,
available books와 **내 account email**을 확인할 수 있다.

다른 사용자가 내 Profile을 볼 때는 email이 기본적으로 숨겨진다. 두 사용자 사이에
현재 `Approved` request가 있을 때만 상대 Profile과 Request detail에 email이 보인다.

## 3. 사용자 Profile 확인

Books, Sent, Received 또는 Request detail에서 사용자 이름을 누르면 Profile로 이동한다.

공개되는 기본 정보:

- username과 아이콘
- general area
- member since
- completed exchanges
- available books

공개되지 않는 정보:

- 권한 없는 다른 사용자의 email
- password와 password hash
- 정확한 주소
- unavailable/private listing
- 개별 request history

## 4. 책 요청하기

```text
Books
→ Available book 확인
→ Request
→ Request #ID · Pending
→ 🙋 Sent requests에서 확인
```

다음 경우에는 Request 버튼을 사용할 수 없다.

- 본인이 소유한 책
- unavailable 상태인 책
- 같은 책에 이미 `Pending` 또는 `Approved` request가 있는 경우

## 5. 보낸 요청 관리

`🙋 Sent requests`에는 내가 borrower로 만든 요청만 표시된다.

- `Pending`: owner의 결정을 기다림
- `Approved`: owner가 요청을 승인함
- `Rejected`: owner가 요청을 거절함
- `Cancelled`: owner 결정 전에 내가 요청을 취소함
- `Returned`: 반납이 완료됨

`Pending` 상태에서는 `Cancel request`를 사용할 수 있다. 승인 또는 거절 이후에는
취소할 수 없다.

## 6. 내 책에 들어온 요청 결정

`📬 Received requests`에는 내가 소유한 책에 들어온 요청만 표시된다.

```text
Received requests
→ Request #ID 또는 Review & decide
→ Decision Context 확인
→ Approve 또는 Reject
```

Decision Context는 request/member time, completed exchanges와 active requests만
보여준다. 승인 전에는 borrower email과 정확한 주소가 표시되지 않는다.

## 7. 승인 후 연락

BookLoop는 현재 내장 messaging을 제공하지 않는다.

```text
Pending
→ email 숨김

Approved
→ 두 당사자가 상대 Profile과 Request detail에서 상대 email 확인

Unrelated user
→ Profile email 숨김 · Request detail 403
```

Email을 확인할 수 있다는 것이 상대의 신원이나 안전을 보증한다는 뜻은 아니다.
금융정보, password, 신분증 전체 이미지와 집 출입 정보는 보내지 않는다.

## 8. Status 색상

| Status | 색상 | 의미 |
| --- | --- | --- |
| `Pending` | Amber | 결정 대기 |
| `Approved` | Green | 승인됨 |
| `Rejected` | Red | 거절됨 |
| `Cancelled` | Gray | borrower가 취소함 |
| `Returned` | Blue | 반납 완료 |

색상과 함께 Status 텍스트를 항상 확인한다.

## 9. 안전하게 책 교환하기

- 집 주소 대신 general area만 공유한다.
- 처음 만날 때는 낮 시간의 도서관이나 카페 같은 공개 장소를 사용한다.
- 지인에게 장소와 시간을 알린다.
- 카드, 은행정보와 현금 보증금을 주고받지 않는다.
- 불편하거나 의심스러우면 승인하거나 만날 의무가 없다.

자세한 내용은 `BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md`를 따른다.

## 10. 현재 한계

현재 MVP에는 다음 기능이 없다.

- 앱 내부 Report와 Block
- 사용자 신원 verification
- 운영자 Admin moderation
- 내장 messaging
- 결제와 보증금

이 기능들은 구현·테스트되기 전까지 사용할 수 있는 기능으로 간주하지 않는다.

## 11. 빠른 사용 체크리스트

- [ ] 내 Profile에서 내 email을 확인했다.
- [ ] 승인 전 상대 Profile에서 email이 숨겨지는 것을 확인했다.
- [ ] 요청을 보낸 뒤 같은 Request ID를 Sent에서 확인했다.
- [ ] owner가 같은 Request ID를 Received에서 확인했다.
- [ ] Approved 후 두 당사자가 상대 email을 확인했다.
- [ ] unrelated 사용자는 상대 email을 볼 수 없음을 확인했다.
- [ ] 실제 교환 전에 Safe Use & Privacy Guide를 확인했다.

## Related Documents

- [Safe Use & Privacy Guide](BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md)
- [Admin & Operator Manual](BOOKLOOP_ADMIN_OPERATOR_MANUAL.md)
- [Local Development User Manual](BOOKLOOP_LOCAL_USER_MANUAL.md)
- [Documentation Index](BOOKLOOP_DOCUMENTATION_INDEX.md)
