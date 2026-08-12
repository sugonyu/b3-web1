# W3-07 API Handoff 복기 노트

> 목적: Python/Jinja로 검증한 BookLoop 요청 기능을 미래 React가 같은 규칙으로
> 사용할 수 있게 만든 과정을 쉬운 말로 다시 공부한다.

## 1. 한 문장 요약

Jinja는 Python service를 직접 호출하고, React는 JSON API를 거쳐 호출하지만,
**두 client 모두 같은 BorrowRequest service와 같은 SQLite 데이터를 사용한다.**

```text
🐍 Jinja route ────────────────┐
                              ↓
                    🧩 BorrowRequest service
                              ↓
                         🗄️ SQLite
                              ↑
🟨 React → 📤 api.py · JSON ──┘
```

React를 아직 만들지 않았어도 API 입구가 같은 service로 연결돼 있으면, Jinja에서
검증한 validation과 authorization을 다시 작성할 필요가 없다.

## 2. 이번 작업 전 무엇이 문제였나?

### 문제 A · client가 borrower ID를 선택할 수 있었다

예전 JSON 요청은 다음 값을 body로 보냈다.

```json
{
  "borrower_id": 2
}
```

서버가 이 값을 그대로 믿으면 로그인한 Tony가 Mina나 Alex의 ID를 넣어 다른 사람
이름으로 요청을 만들 수 있다.

```text
로그인한 사용자: Tony #1
보낸 JSON: borrower_id #3
잘못된 결과: Alex #3의 요청으로 저장 가능
```

이것은 단순 validation 문제가 아니라 **identity와 authorization 경계 문제**다.

### 해결 · session의 current_user만 신뢰한다

현재 route는 JSON의 사용자 ID를 읽지 않는다.

```python
@api.post("/listings/<int:listing_id>/requests")
@login_required
def create_borrow_request(listing_id):
    borrow_request = create_borrow_request_service(
        listing_id,
        current_user.id,
    )
```

핵심 원칙:

```text
client가 주장하는 ID  ❌ 신뢰하지 않음
로그인 session의 ID   ✅ 서버가 신뢰
```

body에 가짜 `borrower_id`가 들어와도 서버는 `current_user.id`를 사용한다.

## 3. Collection과 Single Resource 차이

기존에는 특정 요청 하나만 읽을 수 있었다.

```text
GET /api/requests/3
```

이 URL의 `3`은 BorrowRequest 한 개를 뜻한다.

React가 Sent와 Received 목록을 만들려면 여러 request를 반환하는 collection
endpoint도 필요하다.

```text
GET /api/requests
→ 현재 사용자가 보낸 request 목록

GET /api/listing-requests
→ 현재 사용자의 책에 들어온 request 목록
```

| 화면 | JSON endpoint | service 함수 | 필터 기준 |
| --- | --- | --- | --- |
| 📤 Sent requests | `GET /api/requests` | `list_borrower_requests()` | `borrower_id == current_user.id` |
| 📥 Received requests | `GET /api/listing-requests` | `list_listing_owner_requests()` | `listing.owner_id == current_user.id` |
| Request detail | `GET /api/requests/<id>` | `get_authorized_borrow_request()` | borrower 또는 owner |

같은 `/api/requests`라도 ID가 없으면 목록, ID가 있으면 한 개다.

## 4. 왜 Jinja와 React의 호출 경로가 다른가?

### Python/Jinja

Jinja route와 service는 같은 Flask/Python 서버 안에 있다.

```text
브라우저
→ jinja_product.py
→ services/borrow_requests.py
→ SQLAlchemy
→ SQLite
→ Jinja HTML 응답
```

따라서 Python 함수인 service를 바로 호출할 수 있다.

### React

React는 브라우저에서 JavaScript로 실행된다. Python 함수를 직접 호출할 수 없어서
HTTP와 JSON 경계가 필요하다.

```text
React fetch()
→ /api/requests
→ api.py
→ services/borrow_requests.py
→ SQLAlchemy
→ SQLite
→ JSON 응답
```

차이는 **입구와 응답 형식**이고 업무 규칙은 같다.

```text
Jinja 응답 = HTML
React 응답 = JSON
공통 규칙 = service
공통 저장소 = SQLite
```

## 5. privacy-safe JSON은 무엇인가?

React가 목록을 그리는 데 필요한 정보는 반환한다.

```json
{
  "id": 3,
  "status": "pending",
  "listing": {
    "id": 1,
    "title": "The Odyssey",
    "author": "Homer",
    "owner": {
      "id": 2,
      "username": "mina",
      "general_area": "Montreal"
    }
  },
  "borrower": {
    "id": 1,
    "username": "tony",
    "general_area": "Montreal"
  }
}
```

다음 private field는 반환하지 않는다.

- `email`
- `password_hash`
- password 원문
- 정확한 집 주소
- 전화번호

`general_area`는 책을 주고받을 대략적인 지역 정보라서 공개 가능한 최소 정보로
유지한다.

## 6. 로그인하지 않거나 관계없는 사용자는 어떻게 되는가?

### 목록 endpoint

```text
비로그인
→ GET /api/requests
→ 401 authentication required
```

로그인 사용자는 SQLAlchemy query 자체가 자기 관계의 row만 선택하므로 다른 사람의
목록이 섞이지 않는다.

### 단일 request endpoint

```text
Tony borrower → 200
Mina owner    → 200
Alex unrelated → 403
Guest          → 401
없는 ID        → 404
```

이 경계가 Kamyar의 privacy 피드백에 대한 현재 기술적 응답이다.

## 7. 관련 파일 지도

| 파일 | 다시 볼 내용 |
| --- | --- |
| `bookloop/api.py` | JSON route, serializer, `current_user`, 두 collection endpoint |
| `bookloop/services/borrow_requests.py` | create/read/list 업무 규칙과 authorization |
| `bookloop/clients/jinja_product.py` | Jinja route가 같은 service를 직접 호출하는 방식 |
| `bookloop/auth.py` | Flask-Login session과 API `401` 응답 |
| `bookloop/db/models.py` | User, BookListing, BorrowRequest 관계 |
| `tests/test_borrow_requests_api.py` | session identity, scope, private field 자동 검증 |
| `API_CONTRACT.md` | React와 Flask가 지킬 공식 JSON 약속 |

복기 순서:

```text
auth.py current_user
→ api.py route
→ services/borrow_requests.py
→ db/models.py
→ test_borrow_requests_api.py
```

## 8. 핵심 자동 테스트가 증명하는 것

### 가짜 body ID 무시

```text
session = Tony
body borrower_id = Mina
결과 borrower = Tony
```

### Sent 목록 scope

```text
Tony 로그인
→ GET /api/requests
→ Tony가 만든 request만 반환
```

### Received 목록 scope

```text
Mina 로그인
→ GET /api/listing-requests
→ Mina 소유 책의 request만 반환
```

### private field 제외

테스트는 key가 없는지만 보는 것이 아니라 실제 이메일 문자열이 전체 응답에 없는지도
검사한다.

## 9. 직접 다시 검증하는 명령

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider tests/test_borrow_requests_api.py
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider
```

W3-07 완료 시점 결과:

```text
focused API/Jinja tests → 30 passed
full backend suite      → 84 passed
```

## 10. 아직 남은 기술 부채

이번 작업으로 모든 API authorization이 끝난 것은 아니다.

아직 일부 BookListing create/update/delete와 BorrowRequest status PATCH는 임시
`owner_id` body를 사용한다. W3-07은 React가 요청 목록을 읽고 요청을 생성하는
handoff 경계까지만 고정했다.

```text
완료: request create/read/list session identity
남음: listing mutation과 request status mutation session identity
```

이 차이를 숨기지 않고 `API_CONTRACT.md`에도 명시했다.

## 11. 발표·코드 디펜스용 짧은 답변

### Q. 왜 React가 service를 직접 호출하지 않나요?

React는 브라우저의 JavaScript이고 service는 서버의 Python 함수라서 직접 호출할 수
없습니다. React는 JSON API를 사용하고 `api.py`가 같은 service를 호출합니다.

### Q. 왜 borrower ID를 JSON으로 받지 않나요?

client가 다른 사용자 ID를 주장할 수 있기 때문입니다. 서버가 관리하는 로그인
session의 `current_user.id`만 identity로 사용합니다.

### Q. Sent와 Received endpoint를 왜 나눴나요?

같은 BorrowRequest라도 사용자의 역할과 query scope가 다릅니다. 하나는 borrower가
만든 요청이고 다른 하나는 owner의 책에 들어온 요청입니다.

### Q. 개인정보 보호는 어디서 확인하나요?

service query가 관계있는 row만 선택하고, serializer는 email과 password hash를
제외하며, API 테스트가 401·403과 private field 부재를 검증합니다.

## 12. 다음 복기 체크리스트

- [ ] Collection URL과 single-resource URL 차이를 말할 수 있다.
- [ ] body의 user ID보다 `current_user`가 안전한 이유를 설명할 수 있다.
- [ ] Jinja와 React가 service를 사용하는 경로 차이를 그릴 수 있다.
- [ ] Sent와 Received query scope 차이를 설명할 수 있다.
- [ ] privacy-safe JSON에 포함·제외되는 field를 구분할 수 있다.
- [ ] 아직 남은 `owner_id` 기술 부채를 솔직하게 설명할 수 있다.

## Related Documents

- [Core JSON API Contract](API_CONTRACT.md)
- [BookLoop Flask Package Code Map](bookloop/README.md)
- [D2 Python/Jinja to D3 React Roadmap](../../docs/planning/D2_PYTHON_JINJA_TO_D3_REACT_ROADMAP.md)
