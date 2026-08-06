"""`python3 bl_cli.py ...`를 위한 얇은 BookLoop CLI 실행 진입점."""

from bookloop.devtools.bl_cli.commands import create_cli


if __name__ == "__main__":
    create_cli()()
