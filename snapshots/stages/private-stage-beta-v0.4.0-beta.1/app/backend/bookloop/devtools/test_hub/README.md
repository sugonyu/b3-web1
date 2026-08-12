# BookLoop Test Hub

`/test/`는 제품 client가 아니라 **개발·학습용 링크 허브**다. Jinja template을
사용한다는 이유만으로 Python/Jinja 제품 client에 포함하지 않는다.

## 역할

```text
/test/
├── 🐍 Python/Jinja product client 링크
├── 🟨 Flask Vanilla client 링크
├── 📤 JSON API 링크
└── 🛠️ Developer tools 링크
```

- 제품 데이터를 직접 소비하거나 수정하지 않는다.
- 자동 테스트를 실행하지 않는다.
- client, API와 devtool의 실행 위치 차이를 브라우저에서 비교한다.
- `/test`와 `/test/` URL은 기존 북마크를 위해 유지한다.

## 왜 clients/ 밖에 두나?

폴더 소유권은 렌더링 기술이 아니라 **화면 목적**으로 결정한다.

```text
Jinja로 제품 화면 렌더링 → clients/jinja_product.py
정적 JavaScript client 제공 → clients/flask_vanilla.py
Jinja로 개발 링크 허브 렌더링 → devtools/test_hub/routes.py
```

따라서 Test Hub는 독립 Blueprint를 유지하되 `clients/`가 아니라 `devtools/`에서
관리한다. 제품 Jinja Blueprint에 `/test/`를 추가하면 제품 route와 개발 도구 route의
책임이 섞이므로 합치지 않는다.

## 파일 연결

```text
bookloop/__init__.py
→ devtools/test_hub/__init__.py
→ devtools/test_hub/routes.py
→ devtools/test_hub/templates/test_hub/index.html
```
