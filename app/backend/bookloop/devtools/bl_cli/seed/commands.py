"""재현 가능한 BookLoop 데모 시작 데이터를 만드는 Flask CLI 명령.

이 명령은 User 세 명과 BookListing 한 권만 준비한다. 발표에서 생성 과정을
증명해야 하는 BorrowRequest는 의도적으로 만들지 않는다.
"""

import os

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from ....db import db
from ....db.models import BookListing, BorrowRequest, User


DEMO_USERS = (
    {
        "username": "tony",
        "email": "tony.demo@bookloop.local",
        "general_area": "Montreal",
    },
    {
        "username": "mina",
        "email": "mina.demo@bookloop.local",
        "general_area": "Montreal",
    },
    {
        "username": "alex",
        "email": "alex.demo@bookloop.local",
        "general_area": "Montreal",
    },
)

DEMO_LISTING = {
    "title": "The Odyssey",
    "author": "Homer",
}

# W2-08 이전 demo DB를 다시 seed할 때 같은 listing row를 새 책으로 갱신한다.
LEGACY_DEMO_LISTING_TITLE = "Almond"


def seed_demo_data(password):
    """시작 데이터가 없을 때만 생성하고 생성·전체 개수를 반환한다."""
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
        users_by_name[user_data["username"]] = user

    # Mina의 id가 listing 조회에 필요하므로 먼저 flush한다. 아직 commit은 하지 않는다.
    db.session.flush()
    mina = users_by_name["mina"]
    listing = BookListing.query.filter_by(
        title=DEMO_LISTING["title"],
        owner_id=mina.id,
    ).one_or_none()

    if listing is None:
        listing = BookListing.query.filter_by(
            title=LEGACY_DEMO_LISTING_TITLE,
            owner_id=mina.id,
        ).one_or_none()

    created_listings = 0
    if listing is None:
        listing = BookListing(
            **DEMO_LISTING,
            availability=True,
            owner=mina,
        )
        db.session.add(listing)
        created_listings = 1
    else:
        listing.title = DEMO_LISTING["title"]
        listing.author = DEMO_LISTING["author"]
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
    """Mina의 demo listing에 연결된 BorrowRequest만 삭제한다."""
    mina = User.query.filter_by(username="mina").one_or_none()
    if mina is None:
        return {"deleted_requests": 0, "remaining_requests": BorrowRequest.query.count()}

    listing = BookListing.query.filter(
        BookListing.owner_id == mina.id,
        BookListing.title.in_(
            (DEMO_LISTING["title"], LEGACY_DEMO_LISTING_TITLE)
        ),
    ).first()
    if listing is None:
        return {"deleted_requests": 0, "remaining_requests": BorrowRequest.query.count()}

    deleted_requests = BorrowRequest.query.filter_by(
        listing_id=listing.id,
    ).delete(synchronize_session=False)
    db.session.commit()

    return {
        "deleted_requests": deleted_requests,
        "remaining_requests": BorrowRequest.query.count(),
    }


def register_seed_commands(app: Flask):
    """애플리케이션에 D2 demo 준비·초기화 CLI 명령을 등록한다."""

    @app.cli.command("seed-demo")
    def seed_demo_command():
        """Tony, Mina, Alex와 Mina의 The Odyssey listing을 준비한다."""
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
        """Mina의 The Odyssey demo 요청만 삭제하고 시작 상태로 되돌린다."""
        db.create_all()
        result = reset_demo_requests()
        click.echo(
            "Demo BorrowRequest reset complete: "
            f"deleted={result['deleted_requests']}; "
            f"remaining BorrowRequests={result['remaining_requests']}."
        )
