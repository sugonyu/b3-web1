"""BookLoop 개발·데모 관리 명령을 조립한다."""

import os

import click

from bookloop import create_app
from bookloop.db import db
from bookloop.devtools.bl_cli.seed.commands import (
    reset_demo_requests,
    seed_demo_data,
)


def create_cli(app_factory=create_app):
    """실행용 app factory를 받아 테스트 가능한 BL-CLI command group을 만든다."""

    @click.group(invoke_without_command=True)
    @click.pass_context
    def cli(context):
        """BookLoop CLI (BL-CLI): local demo and development commands."""
        if context.invoked_subcommand is not None:
            return

        click.echo("BookLoop CLI (BL-CLI)")
        click.echo("Local development and Deliverable 2 demo management.")
        click.echo()
        click.echo("Usage:")
        click.echo("  python3 bl_cli.py <command>")
        click.echo()
        click.echo("Available commands:")
        click.echo("  seed-demo            Prepare Tony, Mina, Alex and The Odyssey.")
        click.echo("  reset-demo-requests  Remove only The Odyssey demo requests.")
        click.echo()
        click.echo("Run 'python3 bl_cli.py --help' for command details.")

    @cli.command("seed-demo")
    def seed_demo_command():
        """Tony, Mina, Alex와 The Odyssey demo listing을 준비한다."""
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
        """The Odyssey demo listing의 BorrowRequest만 삭제한다."""
        app = app_factory()
        with app.app_context():
            db.create_all()
            result = reset_demo_requests()

        click.echo(
            "Demo BorrowRequest reset complete: "
            f"deleted={result['deleted_requests']}; "
            f"remaining BorrowRequests={result['remaining_requests']}."
        )

    return cli
