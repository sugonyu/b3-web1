# D2 Demo Seed

`seed-demo`는 배달 2 브라우저 데모를 매번 같은 시작 상태에서 실행하기 위한
개발용 Flask CLI 명령이다.

생성 대상:

- 사용자 `tony` — borrower
- 사용자 `mina` — Almond listing owner
- 사용자 `alex` — authorization boundary 확인용 unrelated user
- Mina 소유의 대여 가능한 `Almond` BookListing

`BorrowRequest`는 만들지 않는다. 발표 중 Tony가 실제 Jinja 폼으로 생성해야
validation, SQLite persistence와 갱신된 화면을 증명할 수 있기 때문이다.

```bash
cd app/backend
export BOOKLOOP_DEMO_PASSWORD='local-demo-password'
.venv/bin/flask --app run seed-demo
```

현재 수업 데모에서는 Tony, Mina, Alex가 기억하기 쉬운 공통 암호 `1111`을 사용한다.
이 값은 로컬 데모 전용이며 실제 사용자 계정이나 운영 환경의 암호 정책이 아니다.

같은 명령을 다시 실행해도 같은 username과 Mina의 Almond listing을 중복 생성하지
않으며, 세 데모 계정의 password hash는 현재 환경변수 값으로 동기화한다. 이 명령은
기존 row를 삭제하거나 데이터베이스를 reset하지 않는다.
