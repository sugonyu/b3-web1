"""BookLoop 개발·데모 관리 명령을 조립한다."""

import os

import click
from sqlalchemy import inspect, text

from bookloop import create_app
from bookloop.db import db
from bookloop.devtools.bl_cli.seed.commands import (
    reset_demo_requests,
    seed_demo_data,
)


CREATED_AT_TABLES = ("user", "book_listing", "borrow_request")


def upgrade_created_at_columns():
    """기존 SQLite table에 nullable created_at 컬럼을 비파괴 방식으로 추가한다."""
    inspector = inspect(db.engine)
    upgraded_tables = []

    with db.engine.begin() as connection:
        for table_name in CREATED_AT_TABLES:
            column_names = {
                column["name"] for column in inspector.get_columns(table_name)
            }
            if "created_at" in column_names:
                continue

            # table 이름은 사용자 입력이 아닌 위 allowlist 상수만 사용한다.
            connection.execute(
                text(f'ALTER TABLE "{table_name}" ADD COLUMN created_at DATETIME')
            )
            upgraded_tables.append(table_name)

    return upgraded_tables


def create_cli(app_factory=create_app):
    """실행용 app factory를 받아 테스트 가능한 BL-CLI command group을 만든다."""

    @click.group(invoke_without_command=True)
    @click.pass_context
    def cli(context):
        """BookLoop CLI (BL-CLI): local demo and development commands."""
        if context.invoked_subcommand is not None:
            return

        click.echo("BookLoop CLI (BL-CLI)")
        click.echo("Local BookLoop demo and development management.")
        click.echo()
        click.echo("Usage:")
        click.echo("  python3 bl_cli.py <command>")
        click.echo()
        click.echo("Available commands:")
        click.echo("  seed-demo            Prepare demo roles and four classic books.")
        click.echo("  reset-demo-requests  Remove requests for both demo books.")
        click.echo("  upgrade-created-at   Add safe created_at columns to an existing DB.")
        click.echo()
        click.echo("Run 'python3 bl_cli.py --help' for command details.")

    @cli.command("seed-demo")
    def seed_demo_command():
        """Tony·Mina·Alex의 역할과 네 demo listing을 준비한다."""
        password = os.getenv("BOOKLOOP_DEMO_PASSWORD")
        if not password:
            raise click.ClickException(
                "Set BOOKLOOP_DEMO_PASSWORD before running seed-demo."
            )

        app = app_factory()
        with app.app_context():
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

    @cli.command("reset-demo-requests")
    def reset_demo_requests_command():
        """네 demo listing의 BorrowRequest만 삭제한다."""
        app = app_factory()
        with app.app_context():
            db.create_all()
            result = reset_demo_requests()

        click.echo(
            "Demo BorrowRequest reset complete: "
            f"deleted={result['deleted_requests']}; "
            f"remaining BorrowRequests={result['remaining_requests']}."
        )

    @cli.command("upgrade-created-at")
    def upgrade_created_at_command():
        """기존 row를 삭제하지 않고 Inspector timestamp column을 준비한다."""
        app = app_factory()
        with app.app_context():
            db.create_all()
            upgraded_tables = upgrade_created_at_columns()

        if upgraded_tables:
            click.echo(
                "Created-at schema upgrade complete: "
                + ", ".join(upgraded_tables)
                + "."
            )
        else:
            click.echo("Created-at schema already current; no changes needed.")

    return cli
