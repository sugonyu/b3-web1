# BookLoop Versioned Artifact Naming Convention

이 문서는 `app/design-system/`과 `app/architecture/`가 같은 폴더·파일 이름 원칙을
사용하도록 관리하는 공통 기준이다.

## Version folder format

```text
vMAJOR.MINOR-dNN-topic[-lang]
```

예시:

```text
v1.0-d1-foundation
v1.1-d1-uiux-bridge
v1.0-d1-foundation-ko
v1.1-d1-foundation-en
```

| 부분 | 의미 | 규칙 |
| --- | --- | --- |
| `v1.0` | artifact version | `v` + major.minor |
| `d1` | official Deliverable | lowercase `d` + number |
| `foundation` | version purpose | lowercase kebab-case |
| `ko`, `en` | language variant | 번역본이 따로 있을 때만 추가 |

## Naming rules

- 폴더 이름은 모두 lowercase kebab-case를 사용한다.
- 공백, underscore, 날짜와 `final`, `latest`, `new` 같은 상대적 표현을 사용하지 않는다.
- 상위 폴더가 artifact 종류를 알려주므로 하위 이름에 `design-system`이나
  `architecture`를 반복하지 않는다.
- 구조나 내용이 바뀌면 version을 올린다.
- 내용은 같고 언어만 다르면 같은 stage/topic 뒤에 `-ko`, `-en`을 붙인다.
- historical version folder는 덮어쓰지 않고 새 버전을 만든다.

## Standard files inside a version folder

```text
version-folder/
├── README.md   # 목적, 변경 이유, 상태, 근거와 다음 iteration
├── index.html  # 브라우저에서 보는 완성형 evidence
└── style.css   # CSS가 길거나 재사용될 때 사용; inline CSS도 허용
```

| 파일 | 역할 |
| --- | --- |
| `README.md` | 사람이 읽는 source note와 version rationale |
| `index.html` | 폴더 URL로 바로 열리는 browser entry point |
| `style.css` | HTML presentation style; 필요할 때만 분리 |

추가 evidence 파일은 역할이 드러나는 lowercase kebab-case를 사용한다.

```text
model-diagram.svg
api-flow.png
browser-verification.md
```

## Root folder contract

```text
artifact-root/
├── README.md   # 전체 목적, 버전 목록과 운영 원칙
├── index.html  # 버전 선택과 현재 상태
├── drafts/     # 독립적으로 보존하는 version folders
└── references/ # 선택 사항; 학습·스타일 참고 자료
```

## Current application

```text
design-system/drafts/
├── v1.0-d1-foundation/
└── v1.1-d1-uiux-bridge/

architecture/drafts/
├── v1.0-d1-foundation-ko/
└── v1.1-d1-foundation-en/
```

Design System은 두 버전의 내용이 달라 language suffix를 사용하지 않는다.
Architecture v1.0과 v1.1은 같은 내용을 한국어·영어로 보존하므로 language suffix를
사용한다.
