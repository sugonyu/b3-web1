# BookLoop Core JSON API Contract

> D3 React handoff contract · updated 2026-08-06

사람이 이 변경의 이유와 코드 흐름을 다시 공부할 때는
[W3-07 API Handoff 복기 노트](W3_07_API_HANDOFF_STUDY_NOTE.md)를 먼저 읽는다.

이 문서는 React client와 Flask backend 사이의 핵심 JSON 경계를 먼저 확정한다.
현재 구현된 운영 확인용 `GET /api/health`는 아래 10개 제품 endpoint 수에 포함하지
않는다.

## 이것은 Endpoint 계획인가?

그렇다. 이 문서는 코드를 작성하기 전에 다음 항목을 결정하는 **endpoint 계획이자
API contract**다.

- 어떤 URL을 사용할지
- 각 URL에서 어떤 HTTP method를 허용할지
- 목록과 데이터 1개를 어떻게 구분할지
- 어떤 JSON을 받고 반환할지
- 누가 접근할 수 있는지
- 오류일 때 어떤 status code를 반환할지

좋은 API 설계는 route를 즉흥적으로 추가하기보다 이 경계를 먼저 정하고 frontend와
backend가 같은 약속을 사용하게 한다.

## Collection과 Single Resource

API URL의 복수형 resource 이름은 **데이터 목록 또는 모음**을 뜻한다.

```text
/api/listings
```

목록에는 데이터가 0개, 1개 또는 여러 개 있을 수 있다. `listings`는 특정 책 한 권이
아니라 BookListing resource 전체 모음을 표현하므로 복수형을 사용한다.

복수형 URL 뒤에 ID가 붙으면 그 목록 안의 **특정 데이터 1개**를 뜻한다.

```text
/api/listings/12
```

위 URL에서 `12`는 listing 하나를 식별한다.

```text
복수형 URL      = 데이터 목록 또는 모음
복수형 URL + ID = 목록 안의 특정 데이터 1개
```

## HTTP Method와 단수·복수 관계

| Method | URL 형태 | 의미 | 데이터 수 관점 |
| --- | --- | --- | --- |
| `GET` | `/api/listings` | 목록 조회 | 0개 이상 반환 |
| `POST` | `/api/listings` | 목록에 새 항목 추가 | 새 데이터 1개 생성 |
| `GET` | `/api/listings/<listing_id>` | 특정 항목 조회 | 데이터 1개 반환 |
| `PATCH` | `/api/listings/<listing_id>` | 특정 항목 일부 수정 | 데이터 1개 변경 |
| `DELETE` | `/api/listings/<listing_id>` | 특정 항목 삭제 | 데이터 1개 제거 |

`POST`는 새 ID를 아직 모르는 상태에서 collection에 데이터 하나를 추가하므로
`/api/listings`를 사용한다. `PATCH`와 `DELETE`는 이미 존재하는 특정 대상을 알아야
하므로 `<listing_id>`가 포함된 URL을 사용한다.

중첩 URL도 같은 원리를 따른다.

```text
POST /api/listings/<listing_id>/requests
```

이는 특정 listing 1개 아래의 request 목록에 새 BorrowRequest 1개를 추가한다는
뜻이다.

```text
특정 책 1개 → 그 책의 요청 목록 → 새 요청 1개 추가
```

```text
PATCH /api/requests/<request_id>
```

이는 전체 request 목록 중 ID로 지정한 요청 1개의 상태를 수정한다는 뜻이다.

## Primary Workflow

```text
책 목록 조회
→ 소유자가 책 등록
→ 사용자가 책 상세 확인
→ 대여 요청 생성
→ 생성된 대여 요청 조회
→ 소유자가 요청 승인 또는 거절
→ 승인된 대여를 반납 완료로 변경
```

## Ten Core Endpoints

| # | Method | Path | 역할 | 접근 경계 |
| --- | --- | --- | --- | --- |
| 1 | `GET` | `/api/listings` | 공개 가능한 책 목록 조회 | Public |
| 2 | `POST` | `/api/listings` | 소유자가 새 책 등록 | Authenticated |
| 3 | `GET` | `/api/listings/<listing_id>` | 책 한 권의 상세 정보 조회 | Public |
| 4 | `PATCH` | `/api/listings/<listing_id>` | 제목·저자·대여 가능 상태 수정 | Owner only |
| 5 | `DELETE` | `/api/listings/<listing_id>` | 소유자의 책 등록 삭제 | Owner only |
| 6 | `POST` | `/api/listings/<listing_id>/requests` | 사용자가 대여 요청 생성 | Authenticated borrower |
| 7 | `GET` | `/api/requests` | 로그인 사용자가 보낸 요청 목록 | Borrower only |
| 8 | `GET` | `/api/listing-requests` | 로그인 사용자의 책에 들어온 요청 목록 | Listing owner only |
| 9 | `GET` | `/api/requests/<request_id>` | 생성된 요청 하나 조회 | Borrower or listing owner |
| 10 | `PATCH` | `/api/requests/<request_id>` | 요청 승인·거절·반납 상태 변경 | Owner/workflow rule |

회원가입·로그인·로그아웃과 Flask-Login session은 D2에서 구현됐다. BorrowRequest
생성·단일 조회·두 목록 조회와 상태 변경은 모두 `current_user`를 사용하며, client가
JSON body로 borrower 또는 owner ID를 선택할 수 없다. BookListing mutation의 임시
`owner_id` body만 남아 있으며 이후 인증 정리 범위의 명시된 기술 부채다.

## BookListing JSON Shape

```json
{
  "id": 1,
  "title": "Almond",
  "author": "Sohn Won-pyung",
  "availability": true,
  "owner": {
    "id": 1,
    "username": "book_owner",
    "general_area": "NDG"
  }
}
```

공개 응답에는 사용자의 `email`, `password_hash`, 정확한 주소와 전화번호를 포함하지
않는다.

## BorrowRequest JSON Shape

```json
{
  "id": 1,
  "status": "pending",
  "listing_id": 1,
  "listing": {
    "id": 1,
    "title": "Almond",
    "author": "Sohn Won-pyung",
    "availability": true,
    "owner": {
      "id": 1,
      "username": "book_owner",
      "general_area": "NDG"
    }
  },
  "borrower": {
    "id": 2,
    "username": "reader",
    "general_area": "Verdun"
  }
}
```

첫 상태 흐름은 다음으로 제한한다.

```text
pending  → approved
pending  → rejected
pending  → cancelled  # borrower only
approved → returned
```

## First Implementation Slice

Private Stage A-3는 collection endpoint부터 시작해 BookListing CRUD 전체로
확장하고, A-4에서 BorrowRequest workflow를 연결한다.

현재 상태:

```text
A-3.1 GET /api/listings — 구현 및 테스트 통과
A-3.2 POST /api/listings — 구현 및 validation 테스트 통과
A-3.3 listing detail/update/delete — 구현 및 테스트 통과
A-4.1 BorrowRequest create — 구현 및 테스트 통과
A-4.2 request status workflow — 구현 및 테스트 통과
A-4.3 BorrowRequest detail read + authorization — 구현 및 테스트 통과
D3.1 borrower/owner request collections — 구현 및 테스트 통과
D3.2 request POST session identity — 구현 및 테스트 통과
```

### `GET /api/listings`

성공 응답:

```text
200 OK
```

```json
{
  "listings": []
}
```

### `POST /api/listings`

로그인한 listing owner의 request body:

```json
{
  "title": "Almond",
  "author": "Sohn Won-pyung",
  "owner_id": 1
}
```

성공 응답은 생성된 listing과 `201 Created`를 반환한다.

필수 validation:

- `title`, `author`, `owner_id`가 필요하다.
- title과 author는 공백만으로 구성될 수 없다.
- `owner_id`는 실제 `User` row를 가리켜야 한다.

### BookListing 단일 resource

```text
GET    /api/listings/<listing_id>
PATCH  /api/listings/<listing_id>
DELETE /api/listings/<listing_id>
```

- `GET`은 공개 가능한 listing 하나를 반환한다.
- `PATCH`는 임시 `owner_id`를 확인한 뒤 `title`, `author`, `availability`만 수정한다.
- `DELETE`는 임시 `owner_id`를 확인하고 request history가 없을 때 `204`로 삭제한다.
- 실제 인증 단계에서는 body의 `owner_id` 대신 session 사용자를 검사한다.

### BorrowRequest 생성

```text
POST /api/listings/<listing_id>/requests
```

request body는 필요하지 않다. 서버는 Flask-Login session의 `current_user.id`를
service에 전달한다. body에 `borrower_id`를 보내더라도 사용자 identity로 신뢰하지
않는다.

서버는 자기 책 요청, 대여 불가능한 책과 동일 사용자의 활성 중복 요청을 거절한다.
성공하면 `pending` request 하나와 `201 Created`를 반환한다.

### D3 BorrowRequest collection reads

```text
GET /api/requests
→ 현재 사용자가 보낸 request만 최신순으로 반환

GET /api/listing-requests
→ 현재 사용자가 소유한 책에 들어온 request만 최신순으로 반환
```

두 endpoint는 비로그인 사용자에게 JSON `401`을 반환한다. 각 row에는 React가
Books/Sent/Received 화면을 만들 수 있도록 safe `listing`, `owner`, `borrower` 정보가
포함되지만 email, password hash, 정확한 주소와 연락처는 포함되지 않는다.

### W2-03 BorrowRequest create/read vertical slice

```text
POST /api/listings/<listing_id>/requests
→ 201 Created + request ID
→ GET /api/requests/<request_id>
→ 200 OK + 같은 request
```

이 slice는 목록 전체 조회나 승인·반납까지 확장하지 않는다. 생성된 동일 resource를
다시 읽을 수 있는지와 database persistence를 가장 작은 end-to-end 흐름으로 증명한다.

최소 성공 조건:

- POST 응답의 `id`를 GET URL에 사용할 수 있다.
- GET은 같은 `id`, `status`, `listing_id`와 borrower 공개 정보만 반환한다.
- 존재하지 않는 request ID는 `404 Not Found`를 반환한다.
- email, password hash와 정확한 연락처는 응답하지 않는다.
- GET은 로그인한 borrower 본인 또는 관련 listing owner만 허용한다.
- 관계없는 로그인 사용자는 `403`, 비로그인 사용자는 JSON `401`을 받는다.

### BorrowRequest 상태 변경

```text
PATCH /api/requests/<request_id>
```

request body:

```json
{
  "status": "approved"
}
```

- listing owner는 `pending → approved/rejected`와 `approved → returned`를 변경한다.
- borrower 본인은 owner 결정 전 `pending → cancelled`만 변경할 수 있다.
- Flask-Login의 `current_user`로 역할을 판정한다.
- body에 보낸 `owner_id`는 신원 확인에 사용하지 않는다.
- `approved`가 되면 listing의 `availability`는 `false`가 된다.
- `returned`가 되면 listing의 `availability`는 다시 `true`가 된다.
- 허용되지 않은 상태 전환은 `409 Conflict`로 거절한다.

## Error Shape

모든 예상 가능한 client 오류는 같은 기본 구조를 사용한다.

```json
{
  "error": "Short explanation"
}
```

초기 status code 경계:

| Status | 의미 |
| --- | --- |
| `400` | JSON 또는 필수 입력값이 잘못됨 |
| `401` | 로그인이 필요함 |
| `403` | 로그인했지만 소유권이 없음 |
| `404` | listing, request 또는 user를 찾을 수 없음 |
| `409` | 현재 상태에서 허용되지 않는 요청 |

## Implementation Order

```text
A-3.1 GET /api/listings
→ A-3.2 POST /api/listings + validation
→ A-3.3 BookListing detail/update/delete
→ A-4.1 BorrowRequest create
→ A-4.2 approve/reject/return state transitions
→ A-4.3 GET one BorrowRequest for the W2-03 create/read slice
→ D3.1 GET borrower and listing-owner request collections
→ D3.2 lock request creation to Flask-Login current_user
→ React client integration
```

현재는 A-3.1부터 D3.2까지 코드와 테스트 케이스 작성을 마쳤다. Jinja route는
BorrowRequest service를 직접 호출하고, 미래 React client는 `api.py`를 거쳐 같은
service와 SQLite 규칙을 재사용한다.
# W3-14 return status transitions

```text
PATCH /api/requests/<request_id>
{"status": "return_pending"}  # approved request의 borrower만

PATCH /api/requests/<request_id>
{"status": "returned"}       # return_pending request의 listing owner만
```

`return_pending` 동안 listing은 unavailable이고 연락처는 두 당사자에게 유지된다.
owner가 `returned`를 확인하면 listing은 available로 돌아가며 상대 email 공개가 끝난다.
