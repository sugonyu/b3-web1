# BookLoop Safe Use & Privacy Guide

> 안전한 지역 도서 공유를 위한 사용자 안내서 · v0.1 · 2026-08-06

## 이 문서의 목적

BookLoop는 가까운 지역의 사용자끼리 책을 빌리고 돌려주는 서비스다. 이 가이드는
요청 전, 승인 후 연락, 실제 교환과 반납 과정에서 개인정보를 최소한으로 공개하고
안전하게 행동하는 방법을 설명한다.

현재 BookLoop는 수업용 MVP다. 신고, 차단, 사용자 인증 배지와 운영자 Admin View는
아직 구현되지 않았다. 이 문서는 존재하지 않는 보호 기능이 작동하는 것처럼 주장하지
않는다.

## 1. 핵심 안전 원칙

```text
필요하기 전에는 공개하지 않는다.
승인된 상대에게만 필요한 정보를 공개한다.
온라인 정보만으로 상대를 완전히 신뢰하지 않는다.
실제 교환은 공개된 장소에서 진행한다.
불편하거나 의심스러우면 거래를 중단한다.
```

## 2. Profile에서 보이는 정보

로그인한 회원은 다음 최소 정보만 확인할 수 있다.

- username과 아이콘
- general area
- member since
- completed exchanges
- 현재 available 상태인 책

Email은 다음 조건에서만 Profile에 표시된다.

- 본인이 자신의 Profile을 확인할 때
- 두 사용자 사이에 현재 `Approved` request가 있을 때 상대방에게

그 외 Profile에 표시되지 않는 정보:

- 권한 없는 다른 사용자의 email
- password 또는 password hash
- 집 주소와 정확한 위치
- unavailable/private 책
- 개별 request history

`General area`에는 동네나 도시 수준의 정보만 사용한다. 도로명, 번지, 아파트 번호와
같이 거주지를 특정할 수 있는 내용은 입력하지 않는다.

## 3. 책을 요청하기 전

1. 책 제목, 소유자와 general area를 확인한다.
2. 상대 profile의 가입 시점과 완료된 교환 수는 참고 정보로만 사용한다.
3. 완료 횟수가 많다고 안전을 보장한다고 판단하지 않는다.
4. Request를 보내는 것만으로 email이나 정확한 위치가 공개되지 않는지 확인한다.
5. 잘못 요청했다면 owner가 결정하기 전에 `Cancel request`를 사용한다.

## 4. Owner가 요청을 결정할 때

Owner는 privacy-safe Decision Context를 확인한 뒤 승인하거나 거절한다.

- request 생성 시각
- member since
- completed exchanges
- active requests

이 단계에서는 borrower의 email과 정확한 주소가 표시되지 않는다. 정보가 부족하거나
요청이 불편하게 느껴지면 승인할 의무가 없으며 `Reject`를 선택할 수 있다.

## 5. Approved 이후 연락처 공개

BookLoop는 현재 내장 메시징을 제공하지 않는다. 대신 request가 `Approved`가 된 뒤
해당 거래 당사자에게만 상대 email을 공개한다.

| Request 상태 / 사용자 | Profile | Request detail |
| --- | --- | --- |
| 본인이 자기 Profile 확인 | 자기 email 공개 | 해당 없음 |
| `Pending` borrower·owner | 숨김 | 숨김 |
| `Approved` borrower | book owner email 공개 | book owner email 공개 |
| `Approved` book owner | borrower email 공개 | borrower email 공개 |
| `Rejected`, `Cancelled`, `Returned` | 숨김 | 숨김 |
| unrelated user | 숨김 | `403` |
| logged-out visitor | login 필요 | login 필요 |

Email을 확인한 뒤에도 다음 정보는 보내지 않는다.

- password 또는 로그인 코드
- 신분증 전체 이미지
- 카드·은행 계좌 정보
- 불필요한 생년월일이나 법적 문서
- 집 출입 비밀번호

가능하면 BookLoop 연락에만 사용하는 별도 email alias를 이용한다.

## 6. 실제 책 교환

- 낮 시간의 도서관, 카페와 같은 공개된 장소를 선택한다.
- 처음 만나는 사람을 집 안으로 초대하거나 상대의 집 안으로 들어가지 않는다.
- 가족이나 지인에게 만나는 장소와 예정 시간을 알린다.
- 책 상태와 반납 예정 방식을 현장에서 함께 확인한다.
- 현금 보증금이나 카드 정보를 요구받으면 거래를 중단한다.
- 계획과 다른 사람이나 장소가 나타나면 책을 교환하지 않아도 된다.

## 7. 불편하거나 의심스러운 상황

현재 MVP에는 앱 내부 Report 또는 Block 기능이 없다. 따라서:

1. `Pending`이면 request를 취소하거나 거절한다.
2. 상대에게 추가 개인정보를 보내지 않는다.
3. 실제 만남을 진행하지 않는다.
4. 관련 email과 Request ID를 삭제하지 말고 상황 기록으로 보존한다.
5. 즉각적인 위험이 있다면 앱에 의존하지 말고 현지 긴급 지원 기관에 연락한다.

Report, verification과 Admin moderation은 후속 개발 범위다. 구현과 검증이 완료되기
전에는 사용할 수 있는 기능으로 안내하지 않는다.

## 8. BookLoop가 보호하는 것과 보호하지 못하는 것

현재 구현된 보호:

- 로그인 전용 profile
- request 당사자만 상세 조회
- unrelated user의 `403` 차단
- 승인 전 email 비공개
- 승인된 거래 상대에게만 email 공개
- JSON collection에서 email과 password hash 제외

현재 보장하지 못하는 것:

- 사용자의 실제 신원 검증
- email 외부에서 발생한 대화의 보안
- 책의 실제 상태나 반납 보장
- 사용자 행동의 실시간 모니터링
- 앱 내부 신고·차단과 운영자 조치

## 9. 빠른 안전 체크리스트

### Request 전

- [ ] Profile에 정확한 주소를 입력하지 않았다.
- [ ] 책과 general area를 확인했다.
- [ ] Request만으로 email이 공개되지 않는 것을 이해했다.

### Approved 후

- [ ] Request ID와 상대 username을 다시 확인했다.
- [ ] 상대 email이 해당 Approved detail에서만 보이는지 확인했다.
- [ ] 민감한 개인정보나 금융 정보를 보내지 않았다.

### 실제 교환

- [ ] 공개된 장소와 낮 시간을 선택했다.
- [ ] 지인에게 장소와 시간을 알렸다.
- [ ] 불편하면 즉시 거래를 중단할 준비가 되어 있다.

## 10. 개발·검증 문서와의 구분

이 문서는 실제 사용자 행동을 위한 안전 가이드다. 서버 실행, seed 사용자, DB Inspector와
브라우저 테스트 방법은 `BOOKLOOP_LOCAL_USER_MANUAL.md`에서 별도로 다룬다.

React client에서도 이 문서의 공개 범위와 안전 규칙을 동일하게 유지해야 한다.
