# MVP v0.3 — Integrated Prototype

Official checkpoint: 🔗 Deliverable 3 — Frontend and Backend Integration
Review date: August 13, 2026
Status: In progress — public D3 presentation linked; browser evidence remains

## Goal

Present a substantially integrated BookLoop prototype whose primary workflow uses
the Flask backend and real SQLite data from beginning to end, with visible
validation, feedback, navigation, and responsive behavior.

## Required Evidence

- [x] Frontend and backend integration
- [x] Primary database-backed workflow implemented
- [x] Dynamic BookListing and BorrowRequest data displayed
- [x] Input validation implemented
- [x] Success and error states implemented
- [x] Functional navigation implemented
- [x] Responsive product layouts substantially implemented
- [ ] W3-14 two-step return workflow confirmed in Tony's browser
- [ ] Final D3 browser evidence organized
- [ ] Short reproducible presentation flow reviewed
- [ ] Substantial alignment with the approved design direction confirmed
- [ ] Frontend colour, typography, hierarchy and responsive decisions explained
- [ ] Privacy demonstrated as connected system behavior, not only a project value

## Implemented

The Python/Jinja product uses shared application services and SQLAlchemy-backed
SQLite data for borrower and owner request histories, request decisions,
cancellation, approved contact exchange, user profiles, protected Admin views,
user book management, Reports and the DB Inspector. JSON endpoints preserve the
same service and authorization contracts for later React parity.

The latest verified refactoring checkpoint aligns route and use-case names and
adds the `_service` suffix to shared service functions without changing public
URLs or explicit Flask endpoint names.

The Deliverable 2 feedback review fixes the D3 execution order: finish the
Flask/Jinja product evidence first, demonstrate privacy through working boundaries,
and explain how the frontend design supports trust, physical-book exchange and
public/private information separation. React remains optional.

## Evidence

- [August 7 route/service naming checkpoint](../../docs/journal/2026-08-07.md)
- [August 11 recovery and evidence restart](../../docs/journal/2026-08-11.md)
- [Current Week 3 Kanban](../../docs/project-weekly-kanban-board.html)
- [Deliverable 3 presentation](../../docs/presentations/deliverable-03/presentation.html)
- Application source: [`app/`](../../app/)

## Verification

Latest recorded backend regression result:

```text
PYTHONPATH=. .venv/bin/pytest -q -p no:cacheprovider
159 passed
```

This is the latest Beta3 verification recorded from the lab baseline. W3-14 and
the final D3 browser evidence still require Tony's confirmation.

## Known Issues

- The W3-14 browser review remains pending.
- D3 screenshots and the final presentation evidence sequence are not frozen.
- The public presentation is intentionally a limited HTML copy; the private script
  and presentation preparation notes remain in the lab archive.
- Monday, August 10 has no journal by explicit recovery decision.
- React parity is optional and must not delay the required D3 evidence.
- Each representative frontend screen still needs a concise design rationale.

## Git Checkpoint

The August 7 naming refactor was recorded as scoped commit `da1980e7` in the
private action tracker. Tony reviewed and approved the August 11 recovery
documentation for a scoped commit on August 12.

## Snapshot Status

Not frozen. Freeze only after the D3 browser and evidence gates pass.

## Next MVP

MVP v0.4 — Feature-Complete Beta for Deliverable 4.
