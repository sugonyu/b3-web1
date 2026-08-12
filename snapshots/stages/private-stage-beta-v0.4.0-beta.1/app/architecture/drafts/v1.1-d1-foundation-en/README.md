# BookLoop Model Diagram and Project Structure

> Version: Architecture v1.1 — English translation
> Week 1 · 🧩 Deliverable 1 — Definition and Design
> Evidence status: private presentation draft
> Verified against: `app/backend/bookloop/models.py` and the current `app/` tree

Browser document: [BookLoop Model Diagram and Project Structure HTML](index.html)

## Purpose

This document presents why BookLoop needs three data models, how they relate to
one another, and how the current code is organized for the Deliverable 1 presentation.

## Model relationship diagram

```text
User (owner)       1 ─────────── many BookListing
User (borrower)    1 ─────────── many BorrowRequest
BookListing        1 ─────────── many BorrowRequest
```

The relationships can be read as follows:

```text
One User can own many BookListings.
One User can create many BorrowRequests.
One BookListing can receive many BorrowRequests.
Each BorrowRequest connects one book listing with one borrower.
```

## Core model fields

### User

| Field | Role |
| --- | --- |
| `id` | Primary key that identifies the user |
| `username` | Unique public-facing member name |
| `email` | Private information used for login and contact |
| `password_hash` | Authentication value stored instead of a plain-text password |
| `general_area` | General location shared instead of a precise address |

### BookListing

| Field | Role |
| --- | --- |
| `id` | Primary key that identifies the listing |
| `title` | Book title |
| `author` | Book author |
| `availability` | Whether the listing currently accepts requests |
| `owner_id` | Foreign key that identifies the owner User |

### BorrowRequest

| Field | Role |
| --- | --- |
| `id` | Primary key that identifies the borrowing request |
| `status` | Records `pending`, `approved`, `rejected`, or `returned` |
| `listing_id` | Foreign key for the requested BookListing |
| `borrower_id` | Foreign key for the User who created the request |

## Why BorrowRequest is the supporting model

With only `User + BookListing`, BookLoop would be a directory where members find
a book and contact its owner outside the application. `BorrowRequest` records the
request, approval or rejection, and completed return inside the application. A
completed borrowing history can later support the optional trust-rating feature.

## Privacy boundary

Public listings expose only `username` and `general_area`. They do not expose
`email`, `password_hash`, a precise address, or a phone number. The project will
decide how and when to reveal contact information while implementing the
authentication and approval workflow.

## Current project structure

The following tree represents the current private experimental application.

```text
app/
├── README.md                         # Private application entry point
├── architecture/                     # Versioned model and technical evidence
│   ├── index.html                    # Architecture version index
│   └── drafts/
│       ├── v1.0-d1-foundation-ko/    # Korean baseline
│       └── v1.1-d1-foundation-en/    # English translation
├── backend/
│   ├── run.py                        # Flask entry point
│   ├── requirements.txt              # Python dependencies
│   ├── API_CONTRACT.md               # Seven core JSON endpoint contracts
│   ├── bookloop/
│   │   ├── __init__.py               # App factory and Blueprint registration
│   │   ├── database.py               # SQLAlchemy object
│   │   ├── models.py                 # User, BookListing, BorrowRequest
│   │   ├── api.py                    # Health and product JSON API
│   │   ├── client_jinja.py           # Flask/Jinja comparison client
│   │   ├── client_vanilla.py         # Shared Vanilla client route
│   │   ├── services/health.py        # Health response data
│   │   ├── templates/web/            # Jinja client template
│   │   └── static/web/               # Vanilla assets served by Flask
│   └── tests/                         # Model, API, and client tests
├── frontend-vanilla/                  # Independent browser client
└── design-system/
    ├── index.html                     # Draft comparison and Agile lifecycle
    └── drafts/
        ├── v1.0-d1-foundation/        # First design baseline
        └── v1.1-d1-uiux-bridge/       # Adopted D1 Design System MVP v0.1
```

The presentation tree excludes `.venv`, `instance`, caches, and generated files.

## Chosen frontend track and current boundary

The selected target stack is:

```text
React client
    ↓ JSON over HTTP
Flask JSON API
    ↓ SQLAlchemy ORM
SQLite relational database
```

The current application includes the Flask API, database models, Vanilla/Jinja
comparison clients, and the design system. The React client is not implemented
yet and will be added as an independent frontend after D1. The Jinja and Vanilla
clients are private learning evidence, not the claimed final React interface.

## Short presentation explanation

> BookLoop uses three related models. A user can own many book listings and can
> create many borrow requests. Each borrow request connects one borrower to one
> listing and records the borrowing status. The current Flask API and SQLAlchemy
> models are separated from the browser clients, so the future React client can
> consume the same JSON API without changing the database model.

## Source evidence

- [`models.py`](../../../backend/bookloop/models.py)
- [`API_CONTRACT.md`](../../../backend/API_CONTRACT.md)
- [Design System MVP v0.1](../../../design-system/drafts/v1.1-d1-uiux-bridge/README.md)
- [Authentication implementation roadmap](../../../../docs/planning/AUTHENTICATION_IMPLEMENTATION_ROADMAP.md)

## Next iterations

- D1: Use the diagram and current/target structure as presentation evidence.
- D2: Connect login and `current_user`, then update the authentication boundary.
- D3: Add the React folder and actual frontend/backend data flow to the tree.
- D4: Add deployment, testing, and accessibility to the architecture evidence.
