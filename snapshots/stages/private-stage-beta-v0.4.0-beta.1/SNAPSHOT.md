# Beta Snapshot — BookLoop v0.4.0-beta.1

이 폴더는 BookLoop Beta `v0.4.0-beta.1`의 안전한 복습·비교용 동결본이다.
다음 기능 개발은 이 snapshot이 아니라 현재 `../../../app/`에서 계속한다.

## Snapshot identity

| 항목 | 값 |
| --- | --- |
| Product version | `BookLoop Beta v0.4.0-beta.1` |
| Stage | Beta checkpoint |
| Created | 2026-08-12 |
| Source commit | `352af2df` |
| Verification | backend automated tests `146 passed` |
| Public status | 공개 학습·검토용 Beta snapshot, 정식 배포본 아님 |

## Included checkpoint

- BookLoop Flask/Jinja MVP
- Demo login, book listings, borrow request와 승인·반납 흐름
- Admin `Received reports` review queue
- Admin Report 상태 변경: `Open`, `Under review`, `Resolved`, `Dismissed`
- Admin 외부 연락용 email link
- Reporter `My reports` 목록과 본인 Report detail/status 추적
- Admin dashboard의 sharing/request/member contact overview
- Code Map v1.7과 Beta workflow 문서

## Intentionally remaining after this snapshot

- 사용자 책 입력 및 기존 책 정보 수정
- DB Inspector의 Report 테이블 표시

## Excluded

- `backend/.env`
- `backend/.venv/`
- `backend/instance/`와 실제 SQLite database
- `backend-express/node_modules/`
- `.pytest_cache/`, `__pycache__/`, bytecode
- 실제 password, secret과 개인 사용자 data

## Continue development

```text
이 snapshot = BookLoop Beta v0.4.0-beta.1 frozen checkpoint
../../../app/ = 다음 책 관리·DB Inspector Report 기능을 개발하는 최신 작업 위치
```
