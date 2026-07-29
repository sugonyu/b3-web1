# MVP v0.1 — Project Definition

Official checkpoint: 🧩 Deliverable 1 — Definition and Design
Review date: July 30, 2026
Status: In progress — planning and API boundary complete; design evidence and presentation package pending

## Goal

Define a controlled project scope and present the design, data model and proposed
application architecture before implementation begins.

## Required Evidence

- [x] Project summary
- [x] Client quote interpretation
- [x] Client need
- [x] Target user
- [x] Problem statement
- [x] Must-have features
- [x] Optional features
- [x] Approved frontend and backend approach
- [ ] Refined design evidence
- [ ] Design rationale
- [x] Proposed database models and relationships
- [x] Proposed routes or data operations
- [ ] Project structure
- [x] Initial Git repository
- [ ] Five-week implementation schedule

## Evidence

- [Design](evidence/design/README.md)
- [Data Model](evidence/data-model/README.md)
- [Architecture](evidence/architecture/README.md)

## Current direction

- **Project:** BookLoop — privacy-conscious Korean-language book sharing in
  Montreal
- **Simulated client need:** make scarce Korean-language books easier to share
  locally without publishing precise personal contact or address information
- **Target user:** Korean-speaking Montreal residents who want to lend or borrow
  books within a general area
- **Problem:** useful books are difficult to discover locally, while direct
  public contact details create unnecessary privacy risk
- **Primary workflow:** discover a listing → request a borrow → owner approval
  → limited connection
- **Working stack:** React + Flask JSON API + Flask-SQLAlchemy + SQLite
- **Must-have:** listings, owner information boundary, borrow requests, request
  status changes, relational storage, and CRUD
- **Optional later feature:** completed-transaction trust history and rating

The instructor confirmed during class on July 28, 2026 that HTML/CSS may be used
to present the required design-system evidence. BookLoop is being prepared as
the Deliverable 1 proposal and will be reviewed during Thursday's presentation.

## Snapshot Status

The runnable implementation remains in the private lab. Its three models and
seven product endpoints were verified with 24 passing tests on July 28. Only
validated Deliverable 1 evidence will be transferred to this public milestone.

## Current Blocker

No blocker prevents preparation. Instructor review of the BookLoop quote and
scope remains scheduled for Thursday's Deliverable 1 presentation. Remaining
work is the HTML/CSS design-system evidence and rationale, model diagram,
project structure, five-week schedule, and presentation package.

## Next MVP

🗄️ Deliverable 2 — Backend and Database: MVP v0.2 Backend Foundation and First
Vertical Slice, including authentication implementation.
