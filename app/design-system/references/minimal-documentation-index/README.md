# Minimal Documentation Index

Tony가 저장소, 수업, 버전, 진행 상태와 문서 링크를 설명할 때 재사용하는 개인용
HTML/CSS 스타일 참고본이다.

## 적합한 용도

- repository landing page
- course or project dashboard
- documentation index
- version selector
- journal, milestone 또는 Kanban navigation
- 비교표와 운영 절차 설명

## 핵심 특징

- 흰색 배경과 읽기 쉬운 system font
- 얇은 회색 border
- 섹션, 카드, 표와 목록 중심
- 색상은 링크·상태·주요 이동에만 제한
- JavaScript 없이 읽고 이동할 수 있음
- 한 파일을 사람이 직접 수정하기 쉬운 구조

## 사용하지 않는 곳

실제 제품 UI, 쇼핑 화면, BookLoop 카드와 사용자 workflow에는 이 스타일을 자동
적용하지 않는다. 제품 화면은 승인된 해당 앱의 디자인 시스템을 따른다.

## 파일 역할

- `index.html`: 구성 요소와 페이지 구조 예제
- `style.css`: 다른 문서형 페이지에서 복사해 조정할 수 있는 최소 CSS

## Implementation case

현재 실제 적용 사례는 BookLoop Design System Draft Index다.

```text
/home/sugonyu/jd/b2/test/test_py/wp-docker-lab/wordpress/pub/b3-web1/app/design-system/index.html
```

이 reference는 위 페이지에서 사용한 문서형 스타일을 개인 재사용 기준으로 분리한
것이다.

## Future application

검수 후 🌐 공개 BookLoop 저장소의 dashboard, milestone navigation과 관련 문서형
HTML에도 같은 패턴을 적용한다. 다만 공개 폴더의 내용과 링크 구조는 그대로
유지하고 표현 스타일만 재사용한다.

Status: planned — public BookLoop folder에는 아직 적용하지 않음.

## 브라우저 주소

```text
http://localhost:8080/pub/b3-web1/app/design-system/references/minimal-documentation-index/
```
