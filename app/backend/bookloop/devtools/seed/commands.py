"""재현 가능한 BookLoop 데모 시작 데이터를 만드는 Flask CLI 명령.

이 명령은 User 세 명과 BookListing 한 권만 준비한다. 발표에서 생성 과정을
증명해야 하는 BorrowRequest는 의도적으로 만들지 않는다.
"""

import os

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from ...database import db
from ...models import BookListing, BorrowRequest, User


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
    "title": "Almond",
    "author": "Sohn Won-pyung",
}


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

    created_listings = 0
    if listing is None:
        listing = BookListing(
            **DEMO_LISTING,
            availability=True,
            owner=mina,
        )
        db.session.add(listing)
        created_listings = 1

    db.session.commit()

    return {
        "created_users": created_users,
        "created_listings": created_listings,
        "total_users": User.query.count(),
        "total_listings": BookListing.query.count(),
        "total_requests": BorrowRequest.query.count(),
    }


def register_seed_commands(app: Flask):
    """애플리케이션에 개발용 seed-demo CLI 명령을 등록한다."""

    @app.cli.command("seed-demo")
    def seed_demo_command():
        """Tony, Mina, Alex와 Mina의 Almond listing을 준비한다."""
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
