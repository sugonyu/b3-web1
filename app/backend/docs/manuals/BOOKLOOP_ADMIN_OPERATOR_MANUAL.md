# BookLoop Admin & Operator Manual

> 정식 관리자·운영자 매뉴얼 · v1.1-draft · 2026-08-10

## 1. 현재 상태

BookLoop에는 DB 기반 관리자 role과 보호된 Admin report review queue가 있다.
Tony demo 계정만 `/admin/`에 접근하며 일반 회원은 `403`, 비로그인 사용자는 로그인으로
이동한다. Admin은 Report detail에서 상태를 변경하고, 신고 당사자에게는 BookLoop 밖에서
별도로 연락한다.

```text
현재 운영자 도구
→ BL-CLI · DB Inspector · test suite

현재 제품 Admin
→ Report queue · status count · detail review · external contact links

미래 확장
→ email notification · moderation audit log · user suspension
```

개발용 View-as-user와 DB Inspector를 제품 Admin 기능으로 소개하거나 배포해서는 안 된다.

## 2. 역할과 권한 분리

| 역할 | 현재 허용 범위 |
| --- | --- |
| User | 자기 Profile, Sent/Received와 허용된 Request detail |
| Owner | 자기 책에 들어온 Pending request 승인·거절 |
| Local operator | 명시적인 CLI로 demo data 준비·초기화 |
| DB Inspector | safe field를 read-only로 확인 |
| Product Admin | DB role로 보호된 Report review queue와 상태 변경 |

현재 `/admin/`은 두 영역으로 구성한다.

```text
1. System Overview
→ users · member contact directory · listings · availability · request status · book sharing

2. Reports & Moderation
→ report status · detail review · 외부 연락처 · 상태 저장
```

## 3. 운영 전 점검

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
python3 bl_cli.py --help
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider
python3 run.py
```

확인 항목:

- test suite 통과
- 올바른 SQLite 경로 사용
- `.env`와 secret이 Git에 포함되지 않음
- 개발 도구는 명시적 feature flag와 요청별 접근 gate에서만 활성화
- demo password `1111`을 실제 서비스에서 사용하지 않음

## 4. Main → Rose LAN 데모 운영

현재 Main Chromebook의 ChromeOS Linux TCP `5000` 포트 포워딩은 설정된 상태다.
BookLoop의 기본 `python3 run.py`는 Crostini 안에서 `0.0.0.0:5000`에 bind하고
Werkzeug debugger를 끈 안전한 LAN 데모 프로필로 실행한다.

```text
Rose browser
→ http://MAIN_LAN_IP:5000/
→ ChromeOS TCP 5000 port forwarding
→ Main Crostini 0.0.0.0:5000
→ Flask BookLoop
```

### Main에서 서버 시작

```bash
cd /home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/backend
source .venv/bin/activate
python3 run.py
```

정상 실행 확인:

```bash
ss -ltnp | rg ':5000\b'
```

결과의 listen 주소가 `127.0.0.1:5000`이 아니라 `0.0.0.0:5000`이어야 한다.
기본 LAN 프로필에서는 `Debugger is active`와 debugger PIN이 나타나지 않아야 한다.

### Rose에서 접속

ChromeOS Wi-Fi 상세 화면에서 Main의 **현재 LAN IP**를 확인한 뒤 Rose에서 연다.

```text
http://MAIN_LAN_IP:5000/
http://MAIN_LAN_IP:5000/api/health
```

`100.115.92.x`는 Crostini 내부 주소이므로 Rose 접속 주소로 사용하지 않는다.
Main과 Rose는 같은 내부 네트워크에 있어야 한다. Chromebook 재부팅이나 DHCP 갱신 후에는
Main의 LAN IP가 달라질 수 있으며, ChromeOS Linux TCP `5000` 포트 포워딩도
`Disabled/OFF` 상태로 초기화될 수 있다. Rose 검수 전에 현재 Main LAN IP와 포트
포워딩의 ON 상태를 모두 다시 확인한다.

### Rose에서 DB Inspector 확인

Flask debugger는 끈 상태로 유지하면서 read-only DB Inspector만 Rose의 관리자에게
허용한다. 로컬 `.env`에는 다음 두 설정이 필요하다.

```env
ENABLE_DEV_DB_INSPECTOR=true
ENABLE_LAN_DEV_DB_INSPECTOR=true
```

Rose에서 Tony 관리자 계정으로 로그인한 뒤 연다.

```text
http://MAIN_LAN_IP:5000/dev/db/
```

접근 결과는 다음처럼 구분한다.

| 요청 | 결과 |
| --- | --- |
| 내부 network + Tony 관리자 | `200` |
| 내부 network + 비로그인 | 로그인 후 `/dev/db/` 복귀 |
| 내부 network + Mina/Alex | `403` |
| 외부 source IP 또는 feature flag OFF | `404` |

View-as-user는 계속 Main 로컬 전용이다. 필요한 경우 서버를 중지한 뒤 다음 프로필로
실행한다.

```bash
FLASK_RUN_HOST=127.0.0.1 FLASK_DEBUG=true python3 run.py
```

로컬 `.env`의 `ENABLE_DEV_USER_SWITCHER=true`는 DEBUG 조건과 함께 적용된다.
작업이 끝나면 서버를 중지하고 기본 `python3 run.py` LAN 프로필로 돌아간다.

### LAN 운영 안전선

- Flask development server는 내부 데모 전용이며 production 배포가 아니다.
- LAN 프로필에서는 `FLASK_DEBUG=false`를 유지한다.
- `/dev/db/`는 read-only field만 표시하고 관리자 session을 요구한다.
- debugger PIN, secret, password hash 또는 DB 파일을 공유하지 않는다.
- Rose 검수가 끝나면 서버를 중지하고 필요하면 ChromeOS TCP `5000` 포워딩도 끈다.
- 로컬 접속 성공만으로 완료하지 않고 Rose에서 실제 URL을 확인한다.

## 5. Demo data 준비

전체 demo 사용자와 책을 준비한다.

```bash
python3 bl_cli.py seed-demo
```

기존 demo BorrowRequest와 연결되거나 오래된 reset으로 남은 orphan Report를 초기화한다.

```bash
python3 bl_cli.py reset-demo-requests
```

이 명령은 User와 BookListing을 보존한다. 실행 후 `/dev/db/`를 Reload하여
`Borrow Requests · 0 rows`와 `Reports · 0 rows`를 확인한다.

## 6. DB Inspector read-only 원칙

Main 로컬의 `http://127.0.0.1:5000/dev/db/`와 보호된 Rose LAN 주소
`http://MAIN_LAN_IP:5000/dev/db/`는 데이터 확인 전용이다. LAN 접근은 두 feature
flag, 내부 source IP와 Tony 관리자 session을 모두 요구한다.

허용:

- User, BookListing과 BorrowRequest의 safe field 확인
- 관계 ID와 표시 이름 비교
- 최신 row와 Toronto 시간 확인
- status 색상과 레전드 확인

주의:

- Reset은 demo BorrowRequest와 Report를 지우는 명시적인 로컬 개발 작업이다.
- 임의 Delete 버튼이나 개인 데이터 변경은 제공하지 않는다.
- 임의 SQL console
- email과 password hash 표시
- CRUD와 moderation action

### DB Inspector Reset 버튼의 범위

```text
/dev/db/ = 관찰 + 확인된 demo reset
BL-CLI   = 명시적인 seed/reset 변경
```

브라우저 Reset은 확인된 POST 요청으로만 실행되며, demo BorrowRequest와 관련 Report,
오래된 reset으로 남은 orphan Report를 삭제한다. User와 BookListing은 보존하고,
전체 데이터 삭제나 임의 SQL은 지원하지 않는다. 운영 데이터에 사용하지 않는다.

향후 브라우저 기반 데이터 변경이 꼭 필요해지면 Inspector가 아니라 별도 `Danger Zone`
도구로 분리하고 다음 조건을 모두 충족해야 한다.

- `DEBUG`와 별도 feature flag
- 인증된 operator
- CSRF가 적용된 `POST`
- 대상과 영향 범위 표시
- 2단계 확인
- 실행 결과와 audit log

## 7. 개인정보 운영 규칙

- password와 password hash를 화면, log 또는 export에 넣지 않는다.
- collection JSON에는 email을 넣지 않는다.
- 본인은 자기 Profile email을 확인할 수 있다.
- Approved 두 당사자만 상대 Profile과 Request detail에서 email을 확인한다.
- Pending, Rejected, Cancelled, Returned 또는 unrelated 관계에서는 상대 email을 숨긴다.

단, Product Admin은 예외적으로 `/admin/`의 Member contact directory와 사용자 Profile에서
모든 사용자의 email을 항상 확인할 수 있다. 이 연락처 열람은 관리자 운영·지원 목적이며,
일반 회원 화면과 collection JSON에는 계속 노출하지 않는다.
- DB 파일과 screenshot을 외부에 공유하기 전에 private field를 검토한다.

## 8. 문제 상황 대응

현재 Block과 자동 알림·감사 로그가 없으므로 실제 운영 서비스로 배포하지 않는다.
로컬 데모 중 문제가 발생하면 다음 순서를 따른다.

1. 서버와 demo 진행을 중단한다.
2. 관련 Request ID와 시간을 기록한다.
3. DB Inspector 또는 read-only SQLite 도구로 row를 확인한다.
4. 원인을 검증하기 전 임의로 DB row를 수정하지 않는다.
5. 재현 가능한 테스트를 먼저 추가한다.
6. 수정 후 전체 test suite를 실행한다.

## 9. 현재 MVP와 미래 Product Admin 요구사항

Admin MVP는 일반 사용자 화면과 분리하고 최소 권한으로 설계한다.

### Report triage와 신고 대상 사용자 notice

```text
Report submitted · Open
→ reporter는 My reports에서 상태 확인
→ Admin이 Report detail, Request와 당사자 관계를 먼저 검토
→ 신고 대상 사용자에게는 아직 notice를 표시하지 않음

Admin changes status to Under review
→ 신고 대상 사용자의 해당 Request detail에 Admin review notice 표시
→ reporter, category와 details는 Admin 화면에만 유지
→ 당사자끼리 Report를 직접 논의하지 않도록 안내
```

현재 Request는 borrower와 owner 두 당사자로 구성되므로 신고 대상 사용자가 제출자를
추론할 수 있다. 따라서 Admin은 익명성을 보장한다고 설명하지 않는다. 시스템이 신고자
이름을 notice에 직접 표시하지 않는 이유는 익명성 연출이 아니라 직접 충돌을 줄이고
moderation 상세정보를 Admin 경계에 유지하기 위해서다.

`Under review` 전환은 단순한 분류 변경이 아니라 사용자 notice를 활성화하는 운영
결정이다. Admin은 Request 관계와 최소 사실관계를 먼저 확인한 뒤 전환한다. 이 상태
변경은 BorrowRequest의 Approve/Reject를 자동 실행하지 않는다.

- admin 전용 인증과 authorization
- Report 생성·조회·상태 변경
- 상태 변경 후 Admin이 BookLoop 밖에서 신고 당사자에게 별도 연락
- 신고 대상 request와 당사자 관계 확인
- verification 상태 확인
- 제한된 user suspension 또는 restoration
- 모든 moderation action의 actor, time, reason audit log (Future Request)
- 자동 email notification과 발송 기록 (Future Request)
- email 열람 사유와 접근 기록
- unrelated private activity의 기본 비노출

Admin이 “모든 것을 볼 수 있다”는 이유만으로 전체 private data를 기본 노출하지 않는다.
업무에 필요한 정보만 단계적으로 공개한다.

## 10. 배포 금지선

다음 조건에서는 실제 사용자 대상 배포를 완료로 판단하지 않는다.

- demo password가 남아 있음
- DEBUG 또는 developer switcher가 활성화됨
- Block, 자동 알림과 실제 운영 대응 절차가 없음
- privacy policy와 retention 규칙이 없음
- production database backup과 recovery가 검증되지 않음
- HTTPS와 secure session 설정이 검증되지 않음

## 11. 운영 체크리스트

- [ ] 변경 전 DB와 Git 상태를 확인했다.
- [ ] 데이터 변경은 제한된 Reset 또는 명시적인 BL-CLI 명령으로 실행했다.
- [ ] `/dev/db/`는 read-only로 유지된다.
- [ ] private field가 화면·JSON·screenshot에 포함되지 않았다.
- [ ] 실행한 명령과 결과를 기록했다.
- [ ] 전체 test suite를 통과했다.
- [ ] 브라우저 결과를 별도로 검수했다.
- [ ] LAN 데모에서는 `0.0.0.0:5000` bind와 `FLASK_DEBUG=false`를 확인했다.
- [ ] Rose에서 `http://MAIN_LAN_IP:5000/`와 `/api/health`를 직접 확인했다.
- [ ] Rose의 `/dev/db/`는 Tony 관리자만 `200`, 일반 회원은 `403`인지 확인했다.

## Related Documents

- [Admin Dashboard Information Architecture](../../docs/planning/ADMIN_DASHBOARD_INFORMATION_ARCHITECTURE.md)
- [D3 Report → D4 Admin Roadmap](../../docs/planning/D3_REPORT_TO_D4_ADMIN_ROADMAP.md)
- [Post-MVP Security Hardening Backlog](../../docs/planning/POST_MVP_SECURITY_HARDENING_BACKLOG.md)
- [User Manual](BOOKLOOP_USER_MANUAL.md)
- [Safe Use & Privacy Guide](BOOKLOOP_SAFE_USE_AND_PRIVACY_GUIDE.md)
- [Local Development User Manual](BOOKLOOP_LOCAL_USER_MANUAL.md)
- [BL-CLI](bookloop/devtools/bl_cli/README.md)
- [Database Inspector](bookloop/devtools/db_inspector/README.md)
- [Documentation Index](../../BOOKLOOP_DOCUMENTATION_INDEX.md)
