# BookLoop Web1 Roadmap

> Course: 582-32W-VA — Web Project 1
> Current milestone: Deliverable 2 · MVP v0.2
> Roadmap status: active and iterative

## Product Direction

BookLoop is a privacy-conscious platform for sharing Korean-language books in
Montreal. The project must demonstrate privacy through working system behavior,
not only through presentation language or visual design.

The core user journey remains narrow:

```text
discover a BookListing
→ create a BorrowRequest
→ protect access to that request
→ approve or reject it
→ share only the minimum information required
```

## Instructor Feedback Requirement

After Deliverable 1, Kamyar identified meaningful privacy implementation as the
project's central challenge. He recommended that the project consider:

- a user verification system;
- a report system;
- an Admin View that can review and control platform activity.

This feedback is treated as a continuing architecture requirement. It does not
mean that every feature must be built immediately or that unfinished features may
be presented as complete.

BookLoop interprets the Admin View as **role-based and accountable management**,
not unrestricted public access to private information. An admin interface should
show only the information required to review users, reports, listings and request
status, and admin actions should be explainable and testable.

## Privacy Principles

Every milestone should preserve these rules:

1. Exact contact information and addresses are not public listing fields.
2. Authentication answers who the current user is.
3. Authorization answers whether that user may perform one specific action.
4. API responses exclude private fields unless a verified workflow requires them.
5. Invalid, unrelated and logged-out access receives explicit server responses.
6. Reporting and admin tools must have their own role and permission checks.
7. Payment, card storage, deposits, refunds and charging remain outside Web1.

## Five-Week Delivery Roadmap

### Week 1 · MVP v0.1 — Definition and Design

Status: **Complete**

Delivered:

- target user, problem and BookLoop concept;
- privacy-first workflow and general-area boundary;
- interface direction and presentation design;
- proposed User, BookListing and BorrowRequest models;
- proposed API and five-week plan.

Feedback carried forward:

- prove privacy through implementation;
- consider verification, reporting and an Admin View;
- keep payment integration outside the course scope.

### Week 2 · MVP v0.2 — Backend and Database

Status: **In progress**

Primary vertical slice:

```text
login
→ open one seeded BookListing
→ create a BorrowRequest
→ save Pending in SQLite
→ read the same request again
```

Privacy and verification gates:

- real browser authentication identifies the current user;
- borrower and listing owner may read the related request;
- unrelated users receive `403 Forbidden`;
- logged-out users receive `401 Login Required`;
- missing requests receive `404 Not Found`;
- email and password-hash fields stay out of public JSON;
- valid and invalid behavior is covered by automated tests;
- SQLite persistence is demonstrated after refresh or restart.

Kamyar-feedback response in this week:

- establish the identity and authorization foundation required by future
  verification, report and Admin features;
- document the later moderation boundary without expanding the current slice.

### Week 3 · MVP v0.3 — Frontend and Backend Integration

Status: **Presentation delivered — closeout in progress**

Main integration:

- connect React to the verified Flask JSON API;
- reuse the same service, validation, authorization and model rules;
- show authenticated listing and BorrowRequest states in the product client;
- preserve visible loading, success, validation and access-error states.

Feedback feature entry point:

- define the smallest Report data contract;
- add a report action to the React workflow only after the D2 request flow works;
- keep report submission separate from admin resolution.

Week 3 gate:

> A user can submit a privacy-safe report through React, and the backend validates
> and stores it without exposing private user fields.

If this gate would destabilize the required D3 integration, preserve the contract
and move its UI implementation to Week 4 rather than presenting an incomplete
feature as finished.

### Week 4 · MVP v0.4 — Feature-Complete Beta

Status: **Next — Week 5 stabilization and final presentation**

Kamyar-feedback MVP:

- add a clear user verification state appropriate for a simulated course app;
- implement report review states such as `open`, `reviewing`, and `resolved`;
- add a role-protected Admin View for users, listings, requests and reports;
- allow only documented administrative actions;
- reject non-admin access to admin routes and APIs;
- test valid and invalid status transitions.

The verification MVP does not claim legal identity verification. It may use a
transparent simulated status such as `unverified` or `verified`, controlled only
through the protected admin workflow.

Week 4 gate:

```text
member submits report
→ report is stored
→ admin-only view reads it
→ admin records a valid resolution
→ ordinary user cannot access the admin boundary
```

### Week 5 · MVP v1.0 — Stable Release and Final Presentation

Status: **Next — stabilization and final presentation preparation**

Final privacy demonstration:

- show the complete borrowing-request flow;
- show private fields absent from public responses;
- show borrower/owner access and unrelated/guest rejection;
- show the implemented verification and report boundary;
- show the protected Admin View and one accountable admin action;
- run regression tests and document remaining limitations;
- present only features verified in the browser and database.

Final gate:

> The audience can see how BookLoop identifies users, protects request data,
> accepts a safety report, restricts admin access, and records the resulting state.

## Data and Module Direction

Current entities:

- `User`
- `BookListing`
- `BorrowRequest`

Planned entities or fields, added only when their milestone begins:

- `User.verification_status`
- `User.role`
- `Report`
- report status and administrative resolution metadata

Reusable backend modules:

```text
🔐 Authentication
→ 🛡️ Authorization
→ ✅ Validation
→ 🧩 Shared service
→ 🗄️ Database transaction
→ 📤 Safe response
```

Jinja, Vanilla and React must not create separate copies of these business rules.

## Scope Control

Must remain in Web1 scope:

- meaningful authentication and authorization;
- privacy-safe API responses;
- one database-backed BorrowRequest workflow;
- a bounded verification/report/Admin response to instructor feedback;
- reproducible tests and evidence.

Must remain outside Web1 scope:

- real payment processing;
- stored card information or deposits;
- legal identity verification claims;
- unrestricted admin access;
- production-scale moderation automation;
- features presented without browser and database verification.

## Roadmap Update Rule

At each weekly closeout:

1. record which privacy gate was actually verified;
2. move unfinished feedback work to the next realistic milestone;
3. update the current milestone README and weekly Kanban;
4. keep this roadmap aligned with implemented source and tests;
5. never mark verification, reporting or Admin View complete from a mockup alone.
