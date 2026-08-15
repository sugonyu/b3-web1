# BookLoop User Manual

> 정식 사용자 매뉴얼 · Beta v0.4.0-beta.2 · 2026-08-12

## 1. 문서 범위

이 문서는 BookLoop에서 책을 등록한 owner와 책을 빌리려는 borrower가 현재
Python/Jinja MVP를 사용하는 방법을 설명한다. 서버 실행, seed data와 DB Inspector는
사용자 기능이 아니므로 개발용 `BOOKLOOP_LOCAL_USER_MANUAL.md`에서 다룬다.

현재 Beta에는 Report 제출과 제출자용 상태 확인이 포함되어 있다. Block과 신원
verification은 아직 제공하지 않는다. Admin moderation은 일반 사용자 화면과
분리된 관리자 기능이다.

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

## 5. 내 책 관리

로그인 후 `My books`에서 본인 책을 등록하고 목록을 확인할 수 있다. 책 제목, 저자,
설명과 availability를 수정할 수 있으며, 더 이상 공유하지 않는 책은 `Unavailable`로
바꿀 수 있다. 삭제 같은 변경 작업은 확인 창에서 다시 확인한다.

## 6. 보낸 요청 관리

`🙋 Sent requests`에는 내가 borrower로 만든 요청만 표시된다.

- `Pending`: owner의 결정을 기다림
- `Approved`: owner가 요청을 승인함
- `Rejected`: owner가 요청을 거절함
- `Cancelled`: owner 결정 전에 내가 요청을 취소함
- `Returned`: 반납이 완료됨

`Pending` 상태에서는 `Cancel request`를 사용할 수 있다. 승인 또는 거절 이후에는
취소할 수 없다.

## 7. 내 책에 들어온 요청 결정

`📬 Received requests`에는 내가 소유한 책에 들어온 요청만 표시된다.

```text
Received requests
→ Request #ID 또는 Review & decide
→ Decision Context 확인
→ Approve 또는 Reject
```

Decision Context는 request/member time, completed exchanges와 active requests만
보여준다. 승인 전에는 borrower email과 정확한 주소가 표시되지 않는다.

## 8. Report 제출과 상태 확인

문제 상황에서는 Report를 제출할 수 있다. 제출 후 `/reports/`의 `My reports`에서
본인이 보낸 Report의 상세 내용과 현재 상태를 확인한다. 상태는 `Open`, `Under review`,
`Resolved`, `Dismissed` 중 하나로 표시된다.

Beta에서는 자동 email 알림이나 앱 내부 messaging을 제공하지 않는다. Admin이 상태를
검토한 뒤 필요한 연락은 BookLoop 밖에서 별도로 진행한다.

Report를 제출했다고 해서 신고 대상 사용자에게 즉시 알림이 표시되지는 않는다.
먼저 Admin이 `Open` Report를 확인하고 `Under review`로 전환해야 한다. 공식 검토가
시작되면 신고 대상 사용자의 해당 Request detail에 `Admin review notice`가 표시된다.

```text
Open
→ 제출자: My reports에서 상태 확인
→ Admin: 내용과 당사자 관계를 먼저 확인
→ 신고 대상 사용자: 아직 notice 없음

Under review
→ 신고 대상 사용자: Admin review notice 확인
→ Report 상세 내용: Admin에게만 표시
```

BookLoop는 두 Request 당사자 사이에서 누가 Report를 제출했는지 추론할 수 없다고
약속하지 않는다. 대신 Report 상세 내용은 Admin 경계에 유지한다. Notice를 본 사용자는
상대방에게 Report에 관해 직접 연락하거나 따지지 말고 Admin의 별도 안내를 기다린다.
Admin review는 BorrowRequest의 Approve 또는 Reject를 자동으로 결정하지 않는다.

## 9. 승인 후 연락

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

## 10. Status 색상

| Status | 색상 | 의미 |
| --- | --- | --- |
| `Pending` | Amber | 결정 대기 |
| `Approved` | Green | 승인됨 |
| `Rejected` | Red | 거절됨 |
| `Cancelled` | Gray | borrower가 취소함 |
| `Returned` | Blue | 반납 완료 |

색상과 함께 Status 텍스트를 항상 확인한다.

## 11. 안전하게 책 교환하기

- 집 주소 대신 general area만 공유한다.
- 처음 만날 때는 낮 시간의 도서관이나 카페 같은 공개 장소를 사용한다.
- 지인에게 장소와 시간을 알린다.
- 카드, 은행정보와 현금 보증금을 주고받지 않는다.
- 불편하거나 의심스러우면 승인하거나 만날 의무가 없다.

자세한 내용은 `BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md`를 따른다.

## 12. 현재 한계

현재 Beta에는 다음 기능이 없다.

- Block
- 사용자 신원 verification
- 내장 messaging
- 결제와 보증금

이 기능들은 구현·테스트되기 전까지 사용할 수 있는 기능으로 간주하지 않는다.

## 13. 빠른 사용 체크리스트

- [ ] 내 Profile에서 내 email을 확인했다.
- [ ] 승인 전 상대 Profile에서 email이 숨겨지는 것을 확인했다.
- [ ] 요청을 보낸 뒤 같은 Request ID를 Sent에서 확인했다.
- [ ] owner가 같은 Request ID를 Received에서 확인했다.
- [ ] Approved 후 두 당사자가 상대 email을 확인했다.
- [ ] 필요하면 Report를 제출하고 `/reports/`에서 상태를 확인했다.
- [ ] unrelated 사용자는 상대 email을 볼 수 없음을 확인했다.
- [ ] 실제 교환 전에 Safe Use & Privacy Guide를 확인했다.

## Related Documents

- [Safe Use & Privacy Guide](BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md)
- [Admin & Operator Manual](BOOKLOOP_ADMIN_OPERATOR_MANUAL.md)
- [Local Development User Manual](BOOKLOOP_LOCAL_USER_MANUAL.md)
- [Documentation Index](../../BOOKLOOP_DOCUMENTATION_INDEX.md)
