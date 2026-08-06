# BookLoop static asset map

Flask가 `/static/` URL로 제공하는 CSS, JavaScript, 이미지와 favicon의 소유권을
폴더 이름으로 구분한다.

```text
static/
├── bookloop/      # 현재 BookLoop Flask 화면의 공통 자산
├── db_inspector/  # DB Inspector 전용 디자인이 생길 때 사용
└── shared/        # 둘 이상의 UI가 실제로 공유하는 범용 자산
```

새 파일은 사용 주체가 분명하면 해당 기능 폴더에 먼저 둔다. 여러 기능에서 실제로
재사용되는 것이 확인된 자산만 `shared/`로 이동한다.
