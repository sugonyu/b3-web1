# MVP v0.1 — Project Definition

Official checkpoint: 🧩 Deliverable 1 — Definition and Design
Review date: July 30, 2026
Status: Deliverable 1 presented; instructor feedback recorded — Week 1 complete

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
- [x] Refined design evidence
- [x] Design rationale
- [x] Proposed database models and relationships
- [x] Proposed routes or data operations
- [x] Project structure
- [x] Initial Git repository
- [x] Five-week implementation schedule

## Evidence

- [Deliverable 1 Presentation](presentation.html)
- [Presentation v1.0 Snapshot](presentation-v1.0.html)
- [BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md)
- [Design](evidence/design/README.md)
- [Data Model](evidence/data-model/README.md)
- [Architecture](evidence/architecture/README.md)

## Presentation Format

Deliverable 1 does not use a separate presentation project or slide folder.
`presentation.html` lives inside this milestone and presents the same reviewed
content linked from this README and `evidence/`.

```text
milestones/01-mvp-v0.1-definition/
├── README.md          # checkpoint, status and evidence index
├── presentation.html  # browser-based Thursday presentation
└── evidence/          # reviewed supporting evidence
```

The HTML presentation is a view of the Deliverable 1 package, not a second
source of truth. Detailed evidence remains under `evidence/`; the presentation
summarizes and links to it. Future corrections must keep the README,
presentation and evidence consistent.

`presentation-v1.0.html` preserves the accepted July 29 baseline. Continue
refining the live `presentation.html` after instructor feedback and create a new
numbered snapshot only when another meaningful presentation baseline is accepted.
The current live v1.1 candidate restores the three low-fidelity workflow screens
that connect the design system to Browse, Detail/Request, and My Requests.

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
to present the required design-system evidence. BookLoop was presented for
Deliverable 1 on July 30, 2026.

## Instructor and Peer Feedback

- Muhamed proposed deposit or card-based trust protection, a donation area,
  Korean flag-inspired colors, and footer social links.
- Kamyar recommended a reporting workflow and an Admin View alongside ratings,
  with deeper focus on privacy, approval, and moderation boundaries.
- Kamyar strongly recommended excluding payment integration from the course
  implementation because of its complexity and risk.

Decision: payment, card storage, deposits, refunds, and charging remain outside
the Web1 scope. Deliverable 2 prioritizes the backend, relational persistence,
validation, authentication where required, and one complete vertical slice.
Kamyar's verification, reporting and Admin View recommendations are tracked as
weekly implementation gates in the
[BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md).

## Snapshot Status

The runnable implementation remains in the private lab. Its three models and
seven product endpoints were verified with 24 passing tests on July 28. Only
validated Deliverable 1 evidence will be transferred to this public milestone.

## Review Result

The presentation package and required evidence were presented, and the feedback
was recorded. Week 1 is complete. The design remains iterative; reporting and
Admin View are important product directions, but they are not presented as
implemented features.

## Next MVP

🗄️ Deliverable 2 — Backend and Database: MVP v0.2 Backend Foundation and First
Vertical Slice, including authentication implementation.
