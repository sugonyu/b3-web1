# BookLoop Application Source

This folder contains the minimum reproducible source used to verify the current
BookLoop backend and client progression.

```text
🟨 Vanilla JavaScript → Flask JSON API
🐍 Python/Jinja      → Flask service and database flow
⚛️ React             → planned Deliverable 3 client
```

The Vanilla client proves that an independent browser client can call the Flask
JSON API through CORS. The Python/Jinja client provides the smaller Deliverable 2
verification path. React will reuse the verified API in Deliverable 3.

## Structure

```text
app/
├── backend/          # Flask, SQLAlchemy, SQLite, Jinja and automated tests
└── frontend-vanilla/ # Independent HTML, CSS and JavaScript API client
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

The command creates Tony, Mina, Alex, and Mina's available Almond listing. It
does not create a BorrowRequest; that record remains part of the browser demo.

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

The current public source proves the backend foundation, relational models,
reproducible demo seed, register/login/logout session, protected request reads,
privacy-safe JSON, and a shared BorrowRequest create/read service. The complete
backend suite passes 52 tests.

The next Deliverable 2 step is the minimal Jinja product workflow: show Almond,
submit Tony's request through the shared service, display Pending, and reopen the
same saved request.
