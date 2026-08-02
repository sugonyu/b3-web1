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

- `http://127.0.0.1:5000/` — Python/Jinja client
- `http://127.0.0.1:5000/vanilla/` — the same Vanilla source served by Flask
- `http://127.0.0.1:5000/api/health` — JSON health endpoint

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
BorrowRequest create/read behavior, protected request reads, privacy-safe JSON,
Jinja rendering, and the Vanilla API/CORS connection.

The reproducible demo seed command, real register/login/logout interface, shared
BorrowRequest service extraction, and Jinja product workflow remain Deliverable 2
work in progress.
