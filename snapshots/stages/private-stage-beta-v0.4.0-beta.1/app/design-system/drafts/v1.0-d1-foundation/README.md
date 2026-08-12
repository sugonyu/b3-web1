# BookLoop Design System Draft v1.0 — Web1 Foundation

이 폴더는 BookLoop 제품 UI를 구현하기 전, 디자인 결정을 HTML/CSS로 검토하는
비공개 evidence 초안이다.

## 현재 범위

- foundations: colour, typography, spacing, border와 layout
- components: button, field, status badge와 BookListing card
- states: loading, empty, success와 error
- low-fi screens: Browse Books, Book Detail / Request와 My Requests
- rationale: privacy, accessibility, consistency와 React 확장 방향

## Colour direction

- 60%에 가까운 기본 배경: warm paper `#fbf8ef`
- 카드와 specimen 표면: white `#ffffff`
- 신뢰·지역 커뮤니티 action: green `#315c43`
- 책갈피와 제한적 강조: orange `#c96f3b`
- 본문: ink `#20251f`

이 색은 책, 종이, 신뢰와 지역사회라는 BookLoop 제품 맥락에서 선택했다. 이
버전에서는 이전 UIUX 과목의 60/30/10이나 Gestalt 원리를 직접 근거로 연결하지
않으며, Web1 Class 2와 현재 API 모델에서 출발한 첫 기준선으로 보존한다.

현재 페이지는 mock data를 사용하는 정적 specimen이다. Flask API나 React와 아직
연결되지 않았으며 refined design으로 확정하지 않는다.

## 브라우저 경로

```text
http://localhost:8080/pub/b3-web1/app/design-system/drafts/v1.0-d1-foundation/
```

Tony가 데스크톱·모바일 화면을 확인한 후 수정하고, 검증된 결정만 🌐 Deliverable 1
design evidence로 승격한다.
