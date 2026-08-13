# MVP v0.4 — Feature-Complete Beta Candidate

Official checkpoint: 🔗 Deliverable 4 — Feature-Complete Beta
Review date: August 12, 2026
Status: Beta v0.4.0-beta.2 feature-complete candidate — release review pending

Roadmap: [BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md)

## Goal

Turn the verified Flask/Jinja prototype into a small, reviewable Beta by closing
the remaining user book-management and operator-inspection gaps.

## Current Beta checkpoint

`BookLoop Beta v0.4.0-beta.2` is frozen in the private lab snapshot. The public
application source has been updated from that verified lab state; no code snapshot
is stored in the public repository.

## Completed at this checkpoint

- [x] User can submit a Report from an authorized borrowing request.
- [x] Admin can see received Reports and the reporter in the queue.
- [x] Admin can open Report detail and change its status.
- [x] Reporter can see their own Report status and detail.
- [x] Admin can use external email links for follow-up outside BookLoop.
- [x] User can add, view, edit, change availability, and safely delete their book listing.
- [x] DB Inspector shows the Report table with privacy-safe fields and status.
- [x] Backend regression suite: `157 passed`.
- [x] Private lab snapshot created for Beta v0.4.0-beta.2.
- [x] Public application source synchronized from the lab without a public code snapshot.

## Remaining Beta work

- [ ] Review browser evidence and decide whether this is feature-complete.

## Explicitly out of current Beta scope

- Automatic email notification service.
- Moderation audit log.
- Payment, card storage, deposits, refunds, or charging.
- React parity before the required Flask/Jinja evidence is stable.

## Snapshot and evidence

- Private lab Beta2 snapshot: created outside this public repository from source commit `b667edd9`
- Current journal: [August 12, 2026](../../docs/journal/2026-08-12.md)
- Current board: [Project weekly Kanban](../../docs/project-weekly-kanban-board.html)
- Application source: [`app/`](../../app/)

## Verification boundary

The `157 passed` result verifies the current internal Beta2 candidate. Browser
evidence and the release decision remain before calling it a public release.
