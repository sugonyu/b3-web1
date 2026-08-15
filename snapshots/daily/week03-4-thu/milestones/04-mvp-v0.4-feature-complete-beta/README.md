# MVP v0.4 — Feature-Complete Beta Candidate

Official checkpoint: 🔗 Deliverable 4 — Feature-Complete Beta
Review date: August 13, 2026
Status: Beta v0.4.0-beta.3 presentation-ready candidate — release review pending

Roadmap: [BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md)

## Goal

Turn the verified Flask/Jinja prototype into a small, reviewable Beta by closing
the remaining user book-management and operator-inspection gaps.

## Current Beta checkpoint

`BookLoop Beta v0.4.0-beta.3` is the current private-lab presentation-ready
candidate. The public application source has been updated from that verified lab
state; no code snapshot is stored in the public repository.

## Completed at this checkpoint

- [x] User can submit a Report from an authorized borrowing request.
- [x] Admin can see received Reports and the reporter in the queue.
- [x] Admin can open Report detail and change its status.
- [x] Reporter can see their own Report status and detail.
- [x] Admin can use external email links for follow-up outside BookLoop.
- [x] User can add, view, edit, change availability, and safely delete their book listing.
- [x] DB Inspector shows the Report table with privacy-safe fields and status.
- [x] Backend regression suite: `159 passed`.
- [x] Private lab snapshot created for Beta v0.4.0-beta.3.
- [x] Public application source synchronized from the lab without a public code snapshot.
- [x] Deliverable 3 presentation delivered and public closeout recorded.
- [x] Unofficial post-presentation feedback recorded separately from official grading.

## Remaining Beta work

- [ ] Complete remaining browser evidence and decide whether Beta is feature-complete.
- [ ] Record the instructor's official grade and confirmed D4 scope.

## Explicitly out of current Beta scope

- Automatic email notification service.
- Moderation audit log.
- Payment, card storage, deposits, refunds, or charging.
- React parity before the required Flask/Jinja evidence is stable.

## Snapshot and evidence

- Private lab Beta3 snapshot: created outside this public repository from the presentation-ready lab state
- Current journal: [August 13, 2026](../../docs/journal/2026-08-13.md)
- Current board: [Project weekly Kanban](../../docs/project-weekly-kanban-board.html)
- Application source: [`app/`](../../app/)

## Verification boundary

The recorded backend suite and presentation verify the current internal Beta3
candidate. Browser evidence, official grading and the release decision remain
before calling it a feature-complete public release.
