"""BookLoop developer CLI package.

하위 seed 기능은 Flask application factory에서도 등록한다. 패키지 초기화 단계에서
CLI 조립 모듈을 import하면 순환 참조가 생기므로 진입점이 `commands`를 직접 읽는다.

Outline:
1. package boundary only
2. commands module is imported by the application factory when CLI registration is needed
"""
