# Dev User Switcher

실제 브라우저 사용 순서는 [BookLoop Local User Manual](../../../BOOKLOOP_LOCAL_USER_MANUAL.md)을
참고한다.

Discord의 `View Server As Role`처럼 BookLoop의 seed 사용자 관점별 화면과 권한을
빠르게 비교하는 **로컬 디버깅 도구**다. 실제 로그인, 사용자 관리 또는 제품용
Admin impersonation 기능이 아니다.

## 사용 목적

```text
👨 Tony  → 보낸 요청과 The Iliad 소유자 관점
👩 Mina  → 받은 요청과 The Odyssey 소유자 관점
🕵️ Alex → 관계없는 사용자, 빈 목록과 403 경계 확인
```

제품 화면의 `DEV · View as user` 배너에서 버튼을 누르면 Flask-Login session이
해당 seed 사용자로 바뀌고 Books 화면으로 돌아간다.

## 활성화

로컬 `.env`에 다음 설정을 명시한다.

```text
ENABLE_DEV_USER_SWITCHER=true
```

route는 `DEBUG=true`와 위 설정이 **모두** 충족될 때만 동작한다. 조건이 하나라도
꺼지면 `/dev/user-view/<username>`은 `404`를 반환하고 배너도 렌더링하지 않는다.

## 안전 경계

- POST 요청만 허용한다.
- allowlist는 `tony`, `mina`, `alex`뿐이다.
- seed 사용자가 DB에 없으면 `404`를 반환한다.
- 이메일, password와 password hash를 읽거나 표시하지 않는다.
- 운영 환경, 실제 사용자, 범용 impersonation으로 확장하지 않는다.
- 실제 인증과 privacy 테스트를 대신하지 않고 반복적인 관점 전환만 단축한다.

## 검증 항목

1. 비활성 설정 또는 non-debug 환경에서 `404`
2. 허용된 seed 사용자 전환 후 해당 사용자 화면 표시
3. allowlist 밖의 username은 `404`
4. 제품 화면에 현재 DEV 관점이 명확히 표시
