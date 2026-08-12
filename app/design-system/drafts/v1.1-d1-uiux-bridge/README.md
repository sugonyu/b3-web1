# BookLoop Design System Draft v1.1 — UIUX Bridge

Draft v1.0을 복사해 B3 Applied UI/UX Design에서 실제로 배운 원리를 BookLoop에
명시적으로 연결한 두 번째 비교본이다.

> Selected direction: 병렬공부와 🧩 Deliverable 1 발표 준비에는 Draft v1.1을
> 사용한다. Draft v1.0은 비교 가능한 최초 기준선으로 보존한다.

## v1.1 changes

- 60/30/10을 `paper 60 / white surface 30 / green·orange action 10`으로 설명
- BookListing card에 Gestalt proximity와 figure-ground 적용 근거 추가
- Browse → Detail → Request → My Requests user flow 명시
- CSS token → React theme, repeated specimen → React component 이전 방향 기록
- 이전 UIUX 원문과 Web1 Class 2 브리핑을 source로 표시

## Presentation colour rationale

| 선택 | 결정 이유 |
| --- | --- |
| Warm paper `#fbf8ef` | 종이와 책의 촉감을 연상시키고 긴 목록의 시각적 피로를 줄인다. |
| White surface `#ffffff` | 책 카드와 폼을 배경에서 분리해 정보 구조를 명확하게 만든다. |
| Community green `#315c43` | 안전, 신뢰와 지역 커뮤니티 연결을 표현하며 primary action에 사용한다. |
| Bookmark orange `#c96f3b` | 책갈피를 연상시키며 중요한 보조 강조에만 제한적으로 사용한다. |
| Ink `#20251f` | 순수 검정보다 부드럽지만 본문 대비와 가독성을 유지한다. |

발표용 짧은 설명:

> I used a warm paper background to connect the interface with books, white
> surfaces to separate information, and community green for trusted actions.
> Orange is limited to bookmark-like accents so it does not compete with the
> primary request workflow.

## UIUX source references

- `/home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-uiux/uiux-final/README.md`
- `/home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-uiux/uiux-final/presentation/pt2-final-react-app-demo/bombom-games-react-store-vite-dev/UIUX_DESIGN_PRINCIPLES.md`
- `/home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-uiux/B3_UIUX_COURSE_CLOSEOUT_2026-07-24.md`
- `../../../../../classes/week01-jul27-30/class02-jul-28-tue/애자일 프로젝트 관리 및 디자인 시스템_ 종합 브리핑 문서.md`

## Boundary

이 연결은 디자인 개념의 재사용이다. Bombom Games의 dark palette, 게임 콘텐츠나
MUI 코드를 BookLoop에 복사하지 않는다. BookLoop는 warm paper와 privacy-conscious
community library라는 자체 제품 방향을 유지한다.

Draft v1.1은 Tony 확인 후 목요일 🧩 Deliverable 1에서 제시할
**Design System MVP v0.1 기준선**으로 채택되었다. 이는 영구적인 최종 디자인이
아니며 D2 이후에도 코드와 피드백에 따라 반복 개선한다.

## Iterative lifecycle

Web1은 Agile 방식으로 진행한다. 따라서 디자인 시스템도 매주 구현과 함께 변화한다.

- D1: Draft v1.1을 Design System MVP v0.1 기준선으로 제시
- D2: 데이터, 폼, validation과 API 상태를 반영
- D3: 실제 frontend integration과 responsive flow를 반영
- D4: 접근성, error handling과 컴포넌트 일관성을 보완
- Final: 당시 앱과 일치하는 안정 버전을 제시

D2에서 별도 디자인 시스템 발표가 없어도 iteration은 중단하지 않는다. 새로운
컴포넌트나 상태가 코드에서 확인되면 디시에 반영하고, 변경 이유와 버전을 기록한다.

## Browser URL

```text
http://localhost:8080/pub/b3-web1/app/design-system/drafts/v1.1-d1-uiux-bridge/
```
