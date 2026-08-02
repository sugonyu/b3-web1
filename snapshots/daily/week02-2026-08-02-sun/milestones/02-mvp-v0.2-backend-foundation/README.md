# MVP v0.2 — Backend Foundation and First Vertical Slice

Official checkpoint: 🗄️ Deliverable 2 — Backend and Database
Review date: August 6, 2026
Status: Sunday verification complete; Week 2 browser vertical slice remains in progress

## Goal

Demonstrate a reproducible Flask backend with relational persistence,
validation, and one complete database-backed create/read workflow.

## Required Evidence

- [x] Application starts correctly
- [x] Environment configuration works without committed secrets
- [x] Database can be created reproducibly
- [x] Core models exist
- [x] Model relationships function
- [ ] Authentication functions where the selected workflow requires it
- [x] At least one create workflow works
- [x] At least one read workflow works
- [x] Validation success and failure are demonstrated
- [x] Data persists in the database
- [ ] Git history shows meaningful progression

## Monday Execution Order

1. Create reproducible Tony, Mina, Alex, and Almond seed data without creating a
   BorrowRequest.
2. Connect the real register, login, and logout browser session.
3. Extract shared BorrowRequest create/read, validation, and authorization rules.
4. Connect the minimal Python/Jinja flow: login → Almond → request → Pending →
   reopen the same request.

## Sunday Verification — August 2

The private backend baseline was rerun before Week 2 classroom development.

```text
Automated tests: 25 passed
Temporary SQLite: create → commit → reopen in a new app instance → read passed
```

This confirms the current database creation, core models, relationships, create
operations, validation behavior, and file-based persistence. It does not yet
confirm the development-server startup or browser behavior.

The Flask development server and Python/Jinja client were not newly implemented
for this Week 2 checkpoint. They had already been prepared together while building
the Deliverable 1 foundation. On August 2, W2-01 reverified that existing baseline:
the Jinja page at `/` and JSON endpoint at `/api/health` both returned HTTP 200.
The health payload reported BookLoop `status: ok`, and a request from the documented
`http://localhost:8080` origin returned the matching CORS header. This established
the command-line evidence before Tony's direct browser check.

Tony then confirmed both client paths in the browser: the Python/Jinja client at
`http://127.0.0.1:5000/` and the independent JavaScript/Vanilla client at
`http://localhost:8080/pub/b3-web1/app/frontend-vanilla/`. Together with the HTTP
and CORS checks, this completes the application startup and local environment
configuration evidence.

Therefore, W2-01 records verification of an existing foundation rather than a new
Flask or Python/Jinja implementation achievement.

## W2-03 Vertical Slice Decision — August 2

The selected slice is intentionally one resource from creation to retrieval:

```text
POST /api/listings/<listing_id>/requests
→ GET /api/requests/<request_id>
```

The POST route already creates and persists a pending BorrowRequest. Week 2 adds
the missing GET route for that same ID. Success means the created request can be
read back with the same ID, status, listing ID, and privacy-safe borrower fields;
an unknown ID returns 404. Request-list views and approval/return actions are not
part of this slice. W2-04 defines who may read it before implementation is treated
as complete.

The existing `owner_id` and `borrower_id` request fields are permission checks,
not real login authentication. Authentication remains unchecked until an actual
identity boundary is implemented and verified.

## W2-04 Read Authorization and API — August 2

`GET /api/requests/<request_id>` now uses Flask-Login's session `current_user`.
The borrower who created the request and the owner of the related listing receive
HTTP 200. An unrelated authenticated user receives 403, a logged-out user receives
a JSON 401, and an authenticated lookup of a missing request receives 404. The
response excludes email and password-hash fields.

The focused BorrowRequest suite passed 11 tests and the complete backend suite
passed 30 tests. This completes the protected read endpoint, but the milestone's
full authentication item remains unchecked because register/login/logout endpoints
and a real browser login session are not implemented yet.

## Scope Boundary

The Week 2 slice supports BookLoop's privacy direction but does not attempt to
finish the whole moderation system.

Client strategy for this milestone:

- use the existing Python/Jinja client as the D2 verification interface;
- keep Flask JSON API, service, model, validation, and authorization logic
  independent from the template;
- preserve the existing Vanilla client as a health/CORS reference without adding
  new product features;
- connect React to the verified JSON API during Deliverable 3.

This is a staged delivery decision, not a change from the final React frontend
direction.

Included:

- Flask application and configuration
- relational models and persistence
- server-side validation
- authorization boundary needed by the selected workflow
- one create/read workflow

Not included in Deliverable 2:

- payment integration, card storage, deposits, refunds, or charging
- a complete reporting and Admin View implementation
- social-media or donation integrations
- broad frontend redesign

## Evidence Plan

Add evidence only after it exists and is verified. Preserve reproducible commands,
test results, database schema evidence, and the selected workflow under this
milestone. Do not copy secrets, real user data, dependency folders, or an
unverified private-lab snapshot.

## Thursday Definition of Done

- The application and database start from documented steps.
- The selected create/read workflow persists valid data.
- Invalid or unauthorized input is rejected visibly.
- Model relationships and authentication requirements can be explained.
- Required evidence and meaningful Git progression are ready for review.
