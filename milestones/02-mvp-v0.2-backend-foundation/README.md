# MVP v0.2 — Backend Foundation and First Vertical Slice

Official checkpoint: 🗄️ Deliverable 2 — Backend and Database
Review date: August 6, 2026
Status: Week 2 complete — W2-11 snapshot and Deliverable 2 presentation feedback recorded

Roadmap: [BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md)

## Goal

Demonstrate a reproducible Flask backend with relational persistence,
validation, and one complete database-backed create/read workflow.

## Required Evidence

- [x] Application starts correctly
- [x] Environment configuration works without committed secrets
- [x] Database can be created reproducibly
- [x] Core models exist
- [x] Model relationships function
- [x] Authentication functions where the selected workflow requires it
- [x] At least one create workflow works
- [x] At least one read workflow works
- [x] Validation success and failure are demonstrated
- [x] Data persists in the database
- [x] Git history shows meaningful progression

## Monday Execution Order

1. Create reproducible Tony, Mina, Alex, and The Odyssey seed data without creating a
   BorrowRequest.
2. Connect the real register, login, and logout browser session.
3. Extract shared BorrowRequest create/read, validation, and authorization rules.
4. Connect the minimal Python/Jinja flow: login → The Odyssey → request → Pending →
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
`http://localhost:8080/pub/b3-web1/app/frontend/js-vanilla/`. Together with the HTTP
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

## W2-05 Reproducible Demo Seed — August 3

The private application now provides a `seed-demo` Flask CLI command. It creates
Tony as the borrower, Mina as The Odyssey listing owner, Alex as an unrelated user,
and Mina's available The Odyssey BookListing. It deliberately creates no BorrowRequest,
because that record must be produced through the live browser workflow.

The password comes from the local `BOOKLOOP_DEMO_PASSWORD` environment variable
and only its hash is stored. The command does not delete or reset data. Focused
tests proved that running it twice creates no duplicate users or listing. The
three focused tests and the complete 40-test backend suite passed using isolated
test databases. The command was then applied to the local development database;
Raw SQLite inspection and the read-only `/dev/db/` screen confirmed 3 users,
1 The Odyssey listing, and 0 BorrowRequests.

## W2-06 Seeded Browser Login — August 3

The Python/Jinja client now provides `/login` and a POST `/logout` route. The login
checks the stored password hash, starts a Flask-Login session, and shows the seeded
Tony identity on the product home. Invalid credentials return one generic message,
and logging out restores the protected API's JSON 401 boundary.

Seven focused authentication tests and the complete 47-test backend suite passed.
The running Flask server also accepted the seeded Tony account and retained the
session on the next HTTP request. Registration adds required-field and duplicate
validation, stores only a password hash, and starts the new user's session. Tony
confirmed registration, login, refresh persistence, and logout in the browser.
This completes W2-06 and the milestone authentication evidence.

## W2-07 Shared BorrowRequest Service — August 3

BorrowRequest create/read, business validation, read authorization, and SQLAlchemy
transaction rules now live in `services/borrow_requests.py`. The JSON routes retain
only HTTP input parsing, error conversion, serialization, and response status.
The upcoming Python/Jinja product screen can therefore call the same service
without duplicating the backend rules.

Five direct service tests and the existing eleven BorrowRequest API tests passed
together. The complete backend suite passed 52 tests, preserving the existing API
response and privacy contract.

## W2-08 Python/Jinja Product Flow — August 3

The product home now reads real BookListing rows and lets an authenticated user
submit `Request this book`. The Jinja route calls the same shared service as the
JSON API, saves one pending BorrowRequest, redirects to its stable request URL,
and reads the same row again when that URL is reopened.

Unauthenticated browser actions redirect to login while protected API requests
retain their JSON 401 response. The service blocks the listing owner and duplicate
active requests, and the result page excludes private user fields. Tony verified
the complete login → The Odyssey → request → Pending → reopen flow in the running
browser. The full backend suite passed 59 tests.

The local DB Inspector was reordered for the verification workflow: Borrow
Requests, Book Listings, then Users. It confirmed four local development users,
one The Odyssey listing, and one persisted BorrowRequest. W2-08 is complete. At
this checkpoint, W2-09 evidence selection and W2-10 restart/presentation proof
were the next tasks.

## W2-09 Visible Identity and Access Evidence — August 3

The Jinja product UI now exposes only the identifiers needed to explain and test
the authorization boundary. The signed-in heading includes the current username
and User ID. A duplicate request response includes the existing BorrowRequest ID
and a protected `View Request #ID` link, allowing the same saved record to be
reopened instead of leaving the user at an error message.

Protected request error pages display the HTTP status beside the server message:

```text
403 · borrow request access forbidden
404 · borrow request not found
```

When a logged-out user opens a protected request URL, Flask redirects to
`/login?next=/requests/<id>`. A successful login returns the user to that same
request, where authorization is checked again. Only local application paths are
accepted as `next` values; external redirect targets are rejected. Protected API
requests continue to return JSON 401 responses, and protected POST actions are
not automatically replayed after login.

The focused authentication, service, API, and Jinja tests passed, and the complete
backend suite reached 62 passing tests. Direct HTTP checks confirmed the 403 and
404 messages, duplicate request ID/link, login redirect, and return-to-request
flow. Tony then confirmed the updated identity, duplicate-request link, access
errors, and login-return flow in the browser. W2-09 is complete.

## W2-10 Persistence and Presentation Evidence — August 4

The persisted BorrowRequest was reopened after a server restart and confirmed in
the read-only DB Inspector. The English `presentation-v1.0.html` was created from
the preserved v0.3 draft, with the verified D2 flow replacing the historical LAB
SLOT placeholders. Tony reviewed the persistence result and presentation state.

The full backend suite reached 67 passing tests. W2-10 is complete. W2-11
preserves this evidence in the Deliverable 2 snapshot and Thursday closeout bundle.

## D2 Presentation Feedback — August 6

The presentation was positively received, but the following feedback is carried
forward as the next milestone's design input:

- The database screen was not visible during screen sharing. Future presentation
  preflight must verify the browser, DB Inspector, and evidence window together.
- The presentation exceeded ten minutes. The next presentation should reserve a
  1–2 minute summary and verify the timing before the live session.
- The borrower and listing owner should eventually have request-history views
  scoped to their own records. This is next-milestone work, not a D2 scope change.
- Privacy remains the central project value. Verification, reporting and an Admin
  View are roadmap work that builds on this D2 authorization foundation.
- The current route was described as good, with positive comments including
  “Fantastic” and “Great work.”

Week 2 is now closed. The D2 create/read slice remains intentionally narrow and
frozen; feedback is recorded without reopening already verified implementation.

## Scope Boundary

The Week 2 slice supports BookLoop's privacy direction but does not attempt to
finish the whole moderation system.

The current authentication, authorization, privacy-safe response and automated
test boundaries are the D2 foundation for Kamyar's verification, report-system
and Admin View recommendations. Their bounded implementation order is preserved
in the project roadmap rather than added prematurely to this vertical slice.

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
