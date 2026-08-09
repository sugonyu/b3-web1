# BookLoop Application Source

This folder contains the minimum reproducible source used to verify the current
BookLoop backend and client progression.

```text
🟨 Vanilla JavaScript → Flask JSON health boundary
🐍 Python/Jinja      → current integrated product workflow
⚛️ React             → planned parity client using the same JSON API
```

The Vanilla client proves that an independent browser client can call the Flask
JSON API through CORS. The Python/Jinja client currently provides the integrated
BorrowRequest, privacy, admin, and return workflow. React remains a documented
parity path that will reuse the verified API and shared service rules.

## Structure

```text
app/
├── backend/             # Flask, SQLAlchemy, SQLite, Jinja and tests
└── frontend/
    ├── js-vanilla/      # Independent HTML/CSS/JavaScript API check
    └── react/           # React parity plan and future client boundary
```

## Run the Backend

```bash
cd app/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open:

- `http://127.0.0.1:5000/` — Python/Jinja product home
- `http://127.0.0.1:5000/login` — seeded-user login
- `http://127.0.0.1:5000/register` — registration
- `http://127.0.0.1:5000/test/` — client, API and developer-tool index
- `http://127.0.0.1:5000/vanilla/` — the same Vanilla source served by Flask
- `http://127.0.0.1:5000/api/health` — JSON health endpoint

## Reproducible Demo Start

Create a local `.env` from `.env.example`, set a local-only
`BOOKLOOP_DEMO_PASSWORD`, and run:

```bash
cd app/backend
flask --app run seed-demo
```

The command creates Tony, Mina, and Alex plus four available demo listings:
Tony's *The Odyssey* and *The Iliad*, and Mina's *The Vegetarian* and
*Human Acts*. It does not create a BorrowRequest; that record remains part of
the browser demo.

## Test

```bash
cd app/backend
PYTHONPATH=. pytest -q -p no:cacheprovider
```

## Environment

Copy `.env.example` to `.env` only for local development. Never commit `.env`,
the virtual environment, cache files, generated SQLite databases, secrets, or real
user data.

## Current Boundary

The current public source proves the Flask application factory, relational
models, reproducible demo seed, register/login/logout session, protected request
reads, privacy-safe JSON, and shared services used by both Jinja routes and API
adapters. The Python/Jinja product includes request history, owner decisions,
approved-contact privacy, user profiles, a read-only Admin View, and the
two-step return flow.

The verified backend suite passes 124 tests. React is not presented as a finished
product client; it remains the next parity implementation after the current
Python/Jinja workflow.
