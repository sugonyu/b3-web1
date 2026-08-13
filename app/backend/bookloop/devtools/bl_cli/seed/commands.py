"""재현 가능한 BookLoop 데모 시작 데이터를 만드는 Flask CLI 명령.

이 명령은 Tony·Mina·Alex User 세 명과 BookListing 네 권을 준비한다. Alex는
책 목록이 없는 유일한 관리자이자 신고 검토 전용 계정이다. 발표에서 생성 과정을
증명해야 하는 BorrowRequest는 의도적으로 만들지 않는다.

Outline:
1. DEMO_USERS, DEMO_LISTINGS and legacy listing constants
2. ensure_user_admin_column() — local schema compatibility
3. seed_demo_data() — idempotent demo users and listings
4. reset_demo_requests() — safe demo request cleanup
5. register_seed_commands() — Flask CLI registration
"""

import os

import click
from flask import Flask
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash

from ....db import db
from ....db.models import BookListing, BorrowRequest, Report, User


DEMO_USERS = (
    {
        "username": "tony",
        "email": "tony.demo@bookloop.local",
        "general_area": "Montreal",
        "is_admin": False,
    },
    {
        "username": "mina",
        "email": "mina.demo@bookloop.local",
        "general_area": "Montreal",
        "is_admin": False,
    },
    {
        "username": "alex",
        "email": "alex.demo@bookloop.local",
        "general_area": "Montreal",
        "is_admin": True,
    },
)

DEMO_LISTINGS = (
    {
        "title": "The Odyssey",
        "author": "Homer",
        "owner_username": "tony",
    },
    {
        "title": "The Iliad",
        "author": "Homer",
        "owner_username": "tony",
    },
    {
        "title": "The Vegetarian",
        "author": "Han Kang",
        "owner_username": "mina",
    },
    {
        "title": "Human Acts",
        "author": "Han Kang",
        "owner_username": "mina",
    },
)

# W2-08 이전 demo DB를 다시 seed할 때 같은 listing row를 새 책으로 갱신한다.
LEGACY_DEMO_LISTING_TITLE = "Almond"


def ensure_user_admin_column():
    """기존 SQLite User table에 관리자 flag를 비파괴 방식으로 추가한다."""
    inspector = inspect(db.engine)
    if "user" not in inspector.get_table_names():
        return False

    column_names = {column["name"] for column in inspector.get_columns("user")}
    if "is_admin" in column_names:
        return False

    with db.engine.begin() as connection:
        connection.execute(
            text(
                'ALTER TABLE "user" ADD COLUMN '
                "is_admin BOOLEAN NOT NULL DEFAULT 0"
            )
        )
    return True


def seed_demo_data(password):
    """시작 데이터가 없을 때만 생성하고 생성·전체 개수를 반환한다."""
    ensure_user_admin_column()
    created_users = 0
    users_by_name = {}

    for user_data in DEMO_USERS:
        user = User.query.filter_by(username=user_data["username"]).one_or_none()
        if user is None:
            user = User(
                **user_data,
                password_hash=generate_password_hash(password),
            )
            db.session.add(user)
            created_users += 1
        else:
            # 로컬 데모 계정은 seed를 다시 실행할 때 같은 데모 암호로 동기화한다.
            # 실제 사용자 암호를 다루는 운영용 reset 기능으로 확장하지 않는다.
            user.password_hash = generate_password_hash(password)
            user.email = user_data["email"]
            user.general_area = user_data["general_area"]
            user.is_admin = user_data["is_admin"]
        users_by_name[user_data["username"]] = user

    # owner ID가 listing 조회에 필요하므로 먼저 flush한다. 아직 commit은 하지 않는다.
    db.session.flush()
    created_listings = 0
    for listing_data in DEMO_LISTINGS:
        owner = users_by_name[listing_data["owner_username"]]
        listing = BookListing.query.filter_by(
            title=listing_data["title"],
            owner_id=owner.id,
        ).one_or_none()

        # 이전 Mina demo book row는 한강의 The Vegetarian으로 재사용한다.
        if listing is None and listing_data["title"] == "The Vegetarian":
            listing = BookListing.query.filter_by(
                owner_id=owner.id,
            ).filter(
                BookListing.title.in_(("The Odyssey", LEGACY_DEMO_LISTING_TITLE))
            ).first()

        if listing is None:
            listing = BookListing(
                title=listing_data["title"],
                author=listing_data["author"],
                availability=True,
                owner=owner,
            )
            db.session.add(listing)
            created_listings += 1
        else:
            listing.title = listing_data["title"]
            listing.author = listing_data["author"]
            listing.availability = True

    db.session.commit()

    return {
        "created_users": created_users,
        "created_listings": created_listings,
        "total_users": User.query.count(),
        "total_listings": BookListing.query.count(),
        "total_requests": BorrowRequest.query.count(),
    }


def reset_demo_requests():
    """네 demo listing에 연결된 BorrowRequest와 Report를 삭제한다."""
    mina = User.query.filter_by(username="mina").one_or_none()
    tony = User.query.filter_by(username="tony").one_or_none()
    if mina is None and tony is None:
        return {
            "deleted_requests": 0,
            "deleted_reports": 0,
            "remaining_requests": BorrowRequest.query.count(),
        }

    demo_listing_ids = []
    if mina is not None:
        demo_listing_ids.extend(
            listing.id
            for listing in BookListing.query.filter(
                BookListing.owner_id == mina.id,
                BookListing.title.in_(
                    ("The Vegetarian", "Human Acts", "The Odyssey", LEGACY_DEMO_LISTING_TITLE)
                ),
            ).all()
        )
    if tony is not None:
        demo_listing_ids.extend(
            listing.id
            for listing in BookListing.query.filter(
                BookListing.owner_id == tony.id,
                BookListing.title.in_(("The Odyssey", "The Iliad")),
            ).all()
        )

    if not demo_listing_ids:
        return {
            "deleted_requests": 0,
            "deleted_reports": 0,
            "remaining_requests": BorrowRequest.query.count(),
        }

    demo_request_ids = [
        request.id
        for request in BorrowRequest.query.filter(
            BorrowRequest.listing_id.in_(demo_listing_ids)
        ).all()
    ]
    deleted_reports = 0
    if demo_request_ids:
        deleted_reports = Report.query.filter(
            Report.borrow_request_id.in_(demo_request_ids)
        ).delete(synchronize_session=False)
    deleted_requests = BorrowRequest.query.filter(
        BorrowRequest.listing_id.in_(demo_listing_ids)
    ).delete(synchronize_session=False)
    # 이전 reset 버전이 남긴 연결 대상 없는 Report도 함께 정리한다.
    deleted_orphan_reports = Report.query.filter(
        Report.borrow_request_id.notin_(db.session.query(BorrowRequest.id))
    ).delete(synchronize_session=False)
    # 승인 데모 뒤에도 다음 리허설이 같은 available 상태에서 시작되게 한다.
    BookListing.query.filter(BookListing.id.in_(demo_listing_ids)).update(
        {BookListing.availability: True},
        synchronize_session=False,
    )
    db.session.commit()

    return {
        "deleted_requests": deleted_requests,
        "deleted_reports": deleted_reports + deleted_orphan_reports,
        "remaining_requests": BorrowRequest.query.count(),
    }


def register_seed_commands(app: Flask):
    """애플리케이션에 BookLoop demo 준비·초기화 CLI 명령을 등록한다."""

    @app.cli.command("seed-demo")
    def seed_demo_command():
        """Tony·Mina·Alex와 Homer·Han Kang demo listing을 준비한다."""
        password = os.getenv("BOOKLOOP_DEMO_PASSWORD")
        if not password:
            raise click.ClickException(
                "Set BOOKLOOP_DEMO_PASSWORD before running seed-demo."
            )

        db.create_all()
        result = seed_demo_data(password)
        click.echo(
            "Demo seed complete: "
            f"created users={result['created_users']}, "
            f"listings={result['created_listings']}; "
            f"totals users={result['total_users']}, "
            f"listings={result['total_listings']}, "
            f"BorrowRequests={result['total_requests']}."
        )

    @app.cli.command("reset-demo-requests")
    def reset_demo_requests_command():
        """네 demo listing의 요청만 삭제하고 시작 상태로 되돌린다."""
        db.create_all()
        result = reset_demo_requests()
        click.echo(
            "Demo BorrowRequest reset complete: "
            f"deleted={result['deleted_requests']}; "
            f"Reports deleted={result['deleted_reports']}; "
            f"remaining BorrowRequests={result['remaining_requests']}."
        )
