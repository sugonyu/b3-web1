# BookLoop Design System Drafts

이 폴더는 BookLoop UI를 확정하기 전 HTML/CSS로 비교하는 디자인 evidence
실험실이다. 각 버전은 독립 폴더로 보존하며 이전 draft를 덮어쓰지 않는다.

브라우저에서는 [`index.html`](index.html)을 먼저 열어 두 draft의 차이를 비교하고
각 버전으로 이동한다.

## Draft index

| 버전 | 기준 | 상태 | 브라우저 |
| --- | --- | --- | --- |
| [Draft v1.0](drafts/v1.0-d1-foundation/README.md) | Web1 Class 2와 BookLoop API 모델 | 기준선·보존 | [Open](drafts/v1.0-d1-foundation/index.html) |
| [Draft v1.1](drafts/v1.1-d1-uiux-bridge/README.md) | v1.0 + B3 Applied UI/UX 학습 | **D1 Design System MVP v0.1 기준선 채택** | [Open](drafts/v1.1-d1-uiux-bridge/index.html) |

## Version roles

폴더와 표준 파일 이름은 [BookLoop artifact naming convention](../ARTIFACT_NAMING_CONVENTION.md)을
따른다.

### Draft v1.0 — Web1 Foundation

- BookLoop foundations, components, states와 low-fi screens의 최초 기준
- warm paper, white surface, green action과 orange bookmark palette
- UIUX 과목 원문을 직접 연결하기 전의 독립 기준선

### Draft v1.1 — UIUX Bridge

- 60/30/10 색상 법칙을 BookLoop palette에 명시적으로 적용
- Gestalt proximity와 figure-ground를 BookListing 카드에 설명
- Browse → Detail → Request → My Requests 사용자 흐름 연결
- 현재 CSS token을 미래 React theme/component로 이전하는 경계 기록

병렬공부와 목요일 발표 준비에는 Draft v1.1을 사용한다. Draft v1.0은 최초 판단과
변경 이유를 비교할 수 있는 historical baseline으로 유지한다.

두 버전 모두 mock data를 사용하는 정적 evidence다. Draft v1.1은 목요일
🧩 Deliverable 1에서 **Design System MVP v0.1**로 제시하며, 이것을 영구적인
최종 디자인으로 확정하지 않는다.

## Agile design-system lifecycle

BookLoop 디자인 시스템(개인 약칭: `디시`)은 앱과 따로 끝나는 일회성 산출물이
아니다. 각 Deliverable에서 구현 결과와 피드백을 반영해 반복적으로 발전시킨다.

| 단계 | 디자인 시스템의 역할 |
| --- | --- |
| 🧩 Deliverable 1 | 색상, 서체, 컴포넌트, low-fi flow를 보여주는 MVP v0.1 기준선 |
| 🗄️ Deliverable 2 | 실제 데이터, 폼, validation과 API 상태에서 발견한 요구 반영 |
| 🔗 Deliverable 3 | frontend/backend 통합, 반응형 화면과 실제 사용자 흐름으로 검증 |
| ✅ Deliverable 4 | 접근성, error/loading/empty 상태와 컴포넌트 일관성 보완 |
| Final | 현재 앱과 일치하는 안정 버전을 제시하되 이후 변경 가능성은 유지 |

Deliverable 2에서 디시를 별도로 발표하지 않더라도 iteration은 계속한다. 코드에서
새 상태나 컴포넌트가 생기면 먼저 현재 디시와 비교하고, 결정 근거와 함께 다음
버전에 반영한다.

## References

- [Minimal Documentation Index](references/minimal-documentation-index/README.md)
  - 저장소·수업·버전·프로젝트 문서용 개인 HTML/CSS 참고본
  - BookLoop 제품 UI draft와 구분해서 사용
- [UI/UX Define → Ideate (HMW) Source Map](references/uiux-define-ideate-hmw-source-map/README.md)
  - 실제 B3 UI/UX 자료의 물리적 위치와 브라우저 링크
  - 수업 직접 근거와 PRD·FRD·개발 병렬 해석의 경계를 구분

## Direct browser URLs

```text
http://localhost:8080/pub/b3-web1/app/design-system/drafts/v1.0-d1-foundation/
http://localhost:8080/pub/b3-web1/app/design-system/drafts/v1.1-d1-uiux-bridge/
```

선택용 인덱스:

```text
http://localhost:8080/pub/b3-web1/app/design-system/
```
