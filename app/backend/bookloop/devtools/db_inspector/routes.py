"""BookLoop SQLite 내용을 안전하게 읽는 개발 전용 route.

이 모듈은 제품용 Admin 기능이 아니다. GET 요청으로 허용된 model field만 읽으며,
database를 변경하는 POST, PATCH, DELETE route를 의도적으로 제공하지 않는다.
"""

from flask import Blueprint, abort, current_app, render_template

from ...models import BookListing, BorrowRequest, User


db_inspector = Blueprint(
    "db_inspector",
    __name__,
    url_prefix="/dev/db",
    template_folder="templates",
)


@db_inspector.before_request
def protect_developer_tool():
    """DEBUG와 명시적 설정이 모두 켜진 로컬 개발 요청만 허용한다.

    Blueprint 자체는 app factory에서 항상 등록한다. `app.run(debug=True)`가 앱 생성
    뒤에 DEBUG를 활성화하기 때문에, 등록 시점이 아니라 실제 요청 시점에 검사해야
    로컬 실행과 테스트에서 같은 규칙을 사용할 수 있다.

    접근 조건을 만족하지 않을 때 403 대신 404를 반환해 운영 환경에서 내부 개발
    route의 존재와 database 구조를 불필요하게 알리지 않는다.
    """
    inspector_enabled = current_app.config.get(
        "ENABLE_DEV_DB_INSPECTOR",
        False,
    )

    if not current_app.debug or not inspector_enabled:
        abort(404)


@db_inspector.get("")
@db_inspector.get("/")
def index():
    """세 핵심 model을 ID 순서로 읽어 Inspector template에 전달한다.

    query 결과는 SQLAlchemy 객체이지만 template은 허용된 field만 명시적으로
    출력한다. 특히 User의 email과 password_hash는 절대로 화면에 표시하지 않는다.
    이 route에는 commit, flush, add, delete 호출이 없으므로 GET 전후 database
    상태가 바뀌지 않는다.
    """
    users = User.query.order_by(User.id).all()
    listings = BookListing.query.order_by(BookListing.id).all()
    borrow_requests = BorrowRequest.query.order_by(BorrowRequest.id).all()

    return render_template(
        "db_inspector/index.html",
        users=users,
        listings=listings,
        borrow_requests=borrow_requests,
    )
