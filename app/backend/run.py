"""BookLoop Flask development-server entry point."""

from bookloop import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
